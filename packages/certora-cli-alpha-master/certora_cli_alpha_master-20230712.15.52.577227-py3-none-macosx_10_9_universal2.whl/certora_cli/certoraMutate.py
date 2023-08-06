#!/usr/bin/env python3
import argparse
import atexit
import dataclasses
import json
import multiprocessing
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any, List, Dict, Tuple

import json5
import requests
import urllib3.util
from strenum import StrEnum

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

from EVMVerifier.certoraContextValidator import KEY_ENV_VAR
from Shared.certoraUtils import safe_copy_folder, change_working_directory, CERTORA_INTERNAL_ROOT, \
    get_package_resource, CERTORA_BINS
from certoraRun import run_certora, CertoraRunResult

"""
some more todos:
- add argument checking
- test on a real project
- get original job from a link
- manual mutations
"""


def parse_args() -> argparse.Namespace:
    """
    Returns a Namespace object with the configuration of the mutation testing tool
    """
    parser = argparse.ArgumentParser()

    # submission related
    parser.add_argument("--prover_conf", type=Path, help="The Certora .conf file to use for running certora-cli.")
    parser.add_argument("--gambit_conf", help="The Gambit .conf file to use for Gambit runs.")
    parser.add_argument("--manual_mutations", help="The file containing manual mutations information.")
    parser.add_argument("--num_generated_mutants", type=int,
                        help="Target number of mutations to generate and submit.")
    parser.add_argument("--prover_version", help="The target version of the prover to use.")
    parser.add_argument("--server", help="The server environment to use. If not given, "
                                         "will run on the server given in the prover_conf file, if it exists.")
    parser.add_argument("--debug", action='store_true', help="Turn on verbose debug prints.")
    parser.add_argument("--gambit_out", default="gambit_out", help="The output directory for gambit.")
    parser.add_argument("--applied_mutants_dir", default="applied_mutants",
                        help="The output directory for applying the mutants.")
    # Sets a file that will store the object sent to mutation testing UI (useful for testing)
    parser.add_argument("--ui_out", help=argparse.SUPPRESS)

    # collection + submission related
    parser.add_argument("--collect_file", default="collect.json", help="The file containing the links holding"
                                                                       "certoraRun report outputs."
                                                                       "In async mode, run this tool with only"
                                                                       "this option.")
    parser.add_argument("--sync", action="store_true", help="Turn sync mode on.")

    # Web related config
    parser.add_argument("--max_timeout_attempts_count", default=3, type=int,
                        help="The maximum number of retries a web request is attempted")
    parser.add_argument("--request_timeout", default=10, help="The timeout in seconds for a web request")

    # Polling related
    parser.add_argument("--poll_timeout", default=30, type=int,
                        help="The max number of minutes to poll after submission was completed, "
                             "and before giving up on synchronously getting mutation testing results")

    args = parser.parse_args()

    return args


class WebUtils:
    def __init__(self, args: argparse.Namespace):
        self.server = self.config_server(args)
        self.max_timeout_attempts_count = args.max_timeout_attempts_count
        self.request_timeout = args.request_timeout
        if self.server == "staging":
            self.ui_submit_url = "https://vaas-stg.certora.com/mutationTesting/getUploadInfo?certoraKey="
            self.ui_url = "https://mutation-testing-beta.certora.com?id="
        elif self.server == "production":
            self.ui_submit_url = "https://prover.certora.com/mutationTesting/getUploadInfo?certoraKey="
            self.ui_url = "https://mutation-testing.certora.com?id="
        else:
            print(f"Invalid server name {self.server}")
            sys.exit(1)

    @staticmethod
    def config_server(args: argparse.Namespace) -> str:
        """
        If given a server, it is taken.
        Otherwise, computes from either the conf file
        """
        # default production
        default = "production"
        if args.server:
            return args.server
        elif args.prover_conf is not None:
            # read the conf and try to get server configuration
            with open(args.prover_conf, 'r') as conf_file:
                conf_obj = json5.load(conf_file)
            if "server" in conf_obj:
                return conf_obj["server"]
            else:
                return default
        else:
            return default

    def put_response_with_timeout(self, url: str, data: str) -> Optional[requests.Response]:
        """
        Executes a put request and returns the response, uses a timeout mechanism

        Args
        ----
            url (str): the URL to send a PUT request to
            data (str): the data to send

        Returns
        -------
            Optional[requests.Response]: if any of the attempt succeeded, returns the response
        """
        headers = {"Content-Type": "application/binary"}
        for i in range(self.max_timeout_attempts_count):
            try:
                resp = requests.put(url, data=data, timeout=self.request_timeout, headers=headers)
                return resp
            except Exception:
                print(f"attempt {i} failed to put url {url}.")

        return None

    def get_response_with_timeout(self, url: str,
                                  cookies: Dict[str, str] = {}) -> Optional[requests.Response]:
        """
        Executes a get request and returns the response, uses a timeout mechanism

        Args
        ----
            url (str): the URL to send a GET request to
            cookies (dict[str, str]): an optional set of cookies/request data

        Returns
        -------
            Optional[requests.Response]: if any of the attempt succeeded, returns the response
        """
        for i in range(self.max_timeout_attempts_count):
            try:
                resp = requests.get(url, timeout=self.request_timeout, cookies=cookies)
                return resp
            except Exception:
                print(f"attempt {i} failed to get url {url}.")

        return None


# SUBMIT PHASE FUNCTIONALITY

@dataclass
class GambitMutant:
    filename: str
    original_filename: str
    directory: str
    id: str
    diff: str
    description: str


@dataclass
class MutantRun:
    gambit_mutant: GambitMutant
    link: Optional[str]
    success: bool
    run_directory: Optional[str]


def gambit_entry_point() -> None:
    key = os.environ.get(KEY_ENV_VAR, "")
    if not key:
        print("Cannot run mutation testing without a Certora Key.")
        sys.exit(1)

    args = parse_args()

    # default mode is async. That is, we either _submit_ or _collect_, not both
    if not args.sync:
        # if the user did not supply a conf file, we will check whether there is a collect file and poll it
        if not args.prover_conf:
            ready = collect(args)
            if not ready:
                sys.exit(1)
        else:
            submit(args)
    else:
        # sync mode means we submit, then we poll for the specified amount of minutes
        if not args.prover_conf:
            # sync mode means we submit + collect. If the user just wants to collect, do not add --sync
            print("Must provide a conf file in sync mode. If you wish to poll on a previous submission,"
                  "omit `--sync`")
            sys.exit(1)
        submit(args)
        poll_collect(args)


def submit(args: argparse.Namespace) -> None:
    print("Generating mutants and submitting...")
    # ensure .certora_internal exists
    os.makedirs(CERTORA_INTERNAL_ROOT, exist_ok=True)
    # start by cleaning up any previous run remnants
    cleanup(args, forced=True)
    atexit.register(cleanup, args, False)

    print("First we submit the original Prover configuration, no source mutations...")

    # run original run. if it fails to compile, nothing to continue with
    msg_separator_for_certora_run_start = "********************** PROVER START *************************"
    msg_separator_for_certora_run_end = "**********************  PROVER END  *************************"
    print(msg_separator_for_certora_run_start)
    success, certora_run_result = run_certora_prover(args.prover_conf, args)

    original_link = None
    local = None
    sources_dir = None
    if certora_run_result:
        original_link = certora_run_result.link
        local = certora_run_result.is_local_link
        sources_dir_orig = certora_run_result.src_dir
        # resolve sources_dir with respect to the current working directory
        sources_dir = args.prover_conf.parent / sources_dir_orig

    if local:
        # we do not cleanup in local mode
        atexit.unregister(cleanup)

    if not success or not certora_run_result or not original_link or not sources_dir:
        print("Original run was not successful. Cannot run mutation testing.")
        sys.exit(1)

    if (not local and not validate_url(original_link)) or (local and not Path(original_link).is_dir()):
        print(f"Invalid certoraRun result {original_link}")
        sys.exit(1)

    print(msg_separator_for_certora_run_end)

    # call gambit
    generated_mutants = run_gambit(Path(args.gambit_conf), args)
    # todo generate manual mutants

    # match a generated mutant to a directory where we will apply the diff
    base_dir = Path(get_applied_mutants_dir(args))
    generated_mutants_with_target_dir = []
    for mutant in generated_mutants:
        generated_mutants_with_target_dir.append((mutant, base_dir / f"mutant{mutant.id}"))

    if args.debug:
        print("Associated each mutant to a target directory where the mutant will be applied to the source code")

    print("Submit mutations to Prover...")
    print(msg_separator_for_certora_run_start)
    # find out the number of processes. in local runs, we want just one! otherwise, use all CPUs available (set to None)
    if local:
        num_processes_for_mp = 1
        # otherwise, weird things happen locally. this forces us to refresh and get a new executable
        max_task_per_worker = 1
    else:
        num_processes_for_mp = None
        max_task_per_worker = None
    with multiprocessing.Pool(processes=num_processes_for_mp, maxtasksperchild=max_task_per_worker) as pool:
        mutant_runs = pool.starmap(run_mutant,
                                   [(mutant, sources_dir, trg_dir, args.prover_conf, args) for mutant, trg_dir in
                                    generated_mutants_with_target_dir])

    print(msg_separator_for_certora_run_end)

    if args.debug:
        print("Completed submitting all mutant runs")
        print(original_link)
        print([dataclasses.asdict(m) for m in mutant_runs])

    # wrap it all up and make the input for the 2nd step: the collector
    collect_file_path = Path(args.collect_file)
    with open(collect_file_path, 'w+') as collect_file:
        json.dump({Constants.ORIGINAL: original_link, Constants.MUTANTS: [dataclasses.asdict(m) for m in mutant_runs]},
                  collect_file)

    if not args.sync:
        print(f"... and that's a wrap! Check out later on {collect_file_path}")
    else:
        print(f"... completed submit phase! Now we poll on {args.collect_file}...")


def run_mutant(mutant: GambitMutant, src_dir: Path, trg_dir: Path, orig_conf: Path,
               args: argparse.Namespace) -> MutantRun:
    # first copy src_dir
    safe_copy_folder(src_dir, trg_dir, shutil.ignore_patterns())  # no ignored patterns

    # now apply diff.
    # 1. We wish to root the original file in trg_dir
    orig_file = mutant.original_filename
    # we were running locally from the conf's parent, so we must address that when copying
    orig_file_relative_to_conf_parent = Path(orig_file).relative_to(orig_conf.parent)
    file_path_to_mutate = trg_dir / orig_file_relative_to_conf_parent
    # 2. apply the mutated file in the newly rooted path
    shutil.copy(mutant.filename, file_path_to_mutate)

    with change_working_directory(trg_dir):
        # we have conf file in sources, let's run from it, it will have proper filepaths
        success, certora_run_result = run_certora_prover(Path(orig_conf.name), args)
        if not success or not certora_run_result:
            print(f"Failed to run mutant {mutant}")
            return MutantRun(gambit_mutant=mutant, success=success, link=None, run_directory=None)

        link = certora_run_result.link
        sources_dir = certora_run_result.src_dir

        return MutantRun(gambit_mutant=mutant, success=success, link=link, run_directory=str(sources_dir))


def run_gambit(gambit_conf_file: Path, args: argparse.Namespace) -> List[GambitMutant]:
    print_output = args.debug
    if print_output:
        stdout_stream = None
    else:
        stdout_stream = subprocess.DEVNULL

    gambit_exec = get_gambit_exec()
    gambit_args = [gambit_exec, "mutate", "--json", str(gambit_conf_file),
                   "-o", str(get_gambit_out_dir(args)),
                   "--skip_validate"]
    print(f"Running gambit: {gambit_args}")
    run_result = \
        subprocess.run(gambit_args, shell=False, universal_newlines=True, stderr=subprocess.PIPE, stdout=stdout_stream)

    return_code = run_result.returncode
    if return_code:
        print("Gambit run failed")
        stderr_lines = run_result.stderr.splitlines()
        for line in stderr_lines:
            print(line)
        sys.exit(1)

    if args.debug:
        print("Completed gambit run successfully")

    # read gambit_results.json
    ret_mutants = []
    out_folder = Path(get_gambit_out_dir(args))
    with open(out_folder / "gambit_results.json", "r") as gambit_output_json:
        gambit_output = json.load(gambit_output_json)
        for gambit_mutant_data in gambit_output:
            ret_mutants.append(
                GambitMutant(
                    filename=str(out_folder / Path(gambit_mutant_data[Constants.NAME])),
                    original_filename=gambit_mutant_data[Constants.ORIGINAL],
                    # should be relative to re-root in target dir
                    directory=str(out_folder / Constants.MUTANTS / gambit_mutant_data[Constants.ID]),
                    id=gambit_mutant_data[Constants.ID],
                    diff=gambit_mutant_data[Constants.DIFF],
                    description=gambit_mutant_data[Constants.DESCRIPTION]
                )
            )

    if args.debug:
        print("Got mutant information")
    return ret_mutants


def get_gambit_exec() -> str:
    exec = get_package_resource(CERTORA_BINS / "gambit")
    # try executing it
    try:
        rc = subprocess.run([exec, "--help"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if rc.returncode == 0:
            return str(exec)
        else:
            print(f"Failed to execute {exec}")
            stderr_lines = rc.stderr.splitlines()
            for line in stderr_lines:
                print(line)
            # try just "gambit" - note this may hide some issues with the underlying process
            return "gambit"
    except Exception:
        # could not run the specialized name, just run gambit
        return "gambit"

def run_certora_prover(conf_file: Path, args: argparse.Namespace) -> Tuple[bool, Optional[CertoraRunResult]]:
    og_cwd = Path.cwd()

    with change_working_directory(og_cwd / conf_file.parent):
        with open(conf_file.name, 'r') as conf_file_handle:
            conf_file_obj = json5.load(conf_file_handle)
            if "run_source" in conf_file_obj:
                print(
                    f"Conf object already has a run source: {conf_file_obj['run_source']}")  # is that of significance?

        certora_args = [conf_file.name, "--send_only", "--run_source", "MUTATION"]
        if args.server is not None and "server" not in conf_file_obj:
            # note that if "server" option already exists in conf, the runs will run on the already specified
            # server in conf, but mutation testing results will be sent to whatever server the user provided to
            # certoraMutate
            certora_args.append("--server")
            certora_args.append(args.server)
        if args.prover_version is not None:
            # prover_version is definitely a prover property, so if it's given already, it's a mistake
            if "prover_version" in conf_file_obj:
                print(f"Mutation testing asked to run on Prover version {args.prover_version} but Prover conf already"
                      f"specifies {conf_file_obj['prover_version']}")
                return False, None
            certora_args.append("--prover_version")
            certora_args.append(args.prover_version)

        print(f"Running the Prover: {certora_args}")
        try:
            certora_run_result = run_certora(certora_args, True)
        except Exception as e:
            print(f"Failed to run with {e}")
            return False, None

        return True, certora_run_result


def cleanup(args: argparse.Namespace, forced: bool = False) -> None:
    """
    First cleanup will be forced
    """
    if not args.debug or forced:
        shutil.rmtree(str(get_applied_mutants_dir(args)), ignore_errors=True)
        shutil.rmtree(str(get_gambit_out_dir(args)), ignore_errors=True)


def get_applied_mutants_dir(args: argparse.Namespace) -> Path:
    return Path(CERTORA_INTERNAL_ROOT) / args.applied_mutants_dir


def get_gambit_out_dir(args: argparse.Namespace) -> Path:
    # return CERTORA_INTERNAL / args.gambit_out - waiting for a gambit bug to be introduced :)
    # (Gambit in json mode ignores -o. Luckily, it did not ignore skip_validate.
    # Chandra says it's a feature, but I (SG) asked to "introduce this bug" allowing to -o in json mode.)
    return args.gambit_out


# COLLECT PHASE FUNCTIONALITY


def collect(args: argparse.Namespace) -> bool:
    """
    Returns true if finished collecting.
    Returns false if not, but there's still a chance something will return.
    Will exit with exitcode 1 if something is broken in the collect file.
    """
    if not Path(args.collect_file).exists():
        print(f"Cannot collect results, as file to collect from {args.collect_file} does not exist")
        sys.exit(1)

    with open(args.collect_file, 'r') as collect_handle:
        results_work = json.load(collect_handle)

    if Constants.ORIGINAL not in results_work:
        print(f"Could not find original url in {args.collect_file}")
        sys.exit(1)

    if Constants.MUTANTS not in results_work:
        print(f"Could not find mutants in {args.collect_file}")
        sys.exit(1)

    print(f"Collecting results from {args.collect_file}...")

    original_url = results_work[Constants.ORIGINAL]
    if original_url is None or (not valid_link(original_url)):
        print("There is no original URL - nothing to collect")
        sys.exit(1)

    web_utils = WebUtils(args)

    # if we got a proper URL, we'll use a WebFetcher, otherwise we'll use a FileFetcher
    if validate_url(original_url):
        fetcher: ReportFetcher = WebFetcher(web_utils)
    else:
        fetcher = FileFetcher()
    original_results = get_results(original_url, fetcher)
    if original_results is None:
        print("Failed to get original results")
        return False

    original_results_as_map = {res.name: res.status for res in original_results}
    # check the mutant URLs
    mutants_objs = results_work[Constants.MUTANTS]
    if not all([Constants.LINK in mutant and valid_link(mutant[Constants.LINK]) for mutant in mutants_objs]):
        print("There is a missing mutant URL - nothing to collect:")
        print([mutant[Constants.LINK] for mutant in mutants_objs])
        sys.exit(1)

    # build mutants object with the rule results
    mutants_results = [(mutant, get_results(mutant[Constants.LINK], fetcher)) for mutant in mutants_objs]

    # structure of results.json to send to UI is Original -> UIData, and mutantFileName -> UIData

    ui_elements: List[UIData] = []

    # add original
    ui_elements.append(UIData("", "", "Original", "Original", original_url, original_results))
    # add mutants
    for mutant, mutant_result_list in mutants_results:
        if not mutant_result_list:
            print("Failed to get mutant results")
            return False
        filtered_mutant_result: List[RuleResult] = list(
            filter(lambda r: r.name in original_results_as_map, mutant_result_list))
        ui_elements.append(UIData(mutant[Constants.GAMBIT_MUTANT][Constants.DESCRIPTION],
                                  mutant[Constants.GAMBIT_MUTANT][Constants.DIFF],
                                  mutant[Constants.GAMBIT_MUTANT][Constants.ID],
                                  mutant[Constants.GAMBIT_MUTANT][Constants.FILENAME],
                                  mutant[Constants.LINK],
                                  filtered_mutant_result))

    print("Done collecting results!")
    if args.debug:
        print(json.dumps([dataclasses.asdict(e) for e in ui_elements]))

    submit_to_ui(ui_elements, web_utils, args)
    return True


def valid_link(link: str) -> bool:
    """
    Returns true if the provided link string is either a valid URL or a valid directory path
    """
    return validate_url(link) or Path(link).is_dir()


def validate_url(url: str) -> bool:
    """
    Thanks stackoverflow. This returns true if the given URL string is a valid URL, and false otherwise.
    """
    try:
        result = urllib3.util.parse_url(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def submit_to_ui(elems: List[Any], web_utils: WebUtils, args: argparse.Namespace) -> None:
    resp = web_utils.get_response_with_timeout(web_utils.ui_submit_url + default_cookies[Constants.CERTORA_KEY])
    if resp is None:
        print("Failed to get a presigned URL for sending to the mutation testing UI")
        sys.exit(1)

    resp_obj = resp.json()
    if Constants.ID not in resp_obj \
            or Constants.ANONYMOUS_KEY not in resp_obj or Constants.PRE_SIGNED_URL not in resp_obj:
        print(f"Response is invalid {resp_obj}")
        sys.exit(1)

    mutation_id = resp_obj[Constants.ID]
    anonymous_key = resp_obj[Constants.ANONYMOUS_KEY]
    presigned_url = resp_obj[Constants.PRE_SIGNED_URL]

    to_json = [dataclasses.asdict(e) for e in elems]
    put_resp = web_utils.put_response_with_timeout(presigned_url, json.dumps(to_json))
    if put_resp is None:
        print("Failed to submit to presigned URL")
        sys.exit(1)
    if put_resp.status_code != 200:
        print(f"Failed to submit to presigned URL, stauts code {put_resp.status_code}")
        sys.exit(1)

    final_url = f"{web_utils.ui_url}{mutation_id}&{Constants.ANONYMOUS_KEY}={anonymous_key}"
    print(f"Mutation testing report is available at {final_url}")

    if args.ui_out is not None:
        try:
            with open(args.ui_out, 'w+') as ui_out_json:
                json.dump(to_json, ui_out_json)
        except Exception:
            print(f"Failed to output to {args.ui_out}")


class ReportFetcher:
    def get_output_json(self, link: str) -> Optional[Dict[str, Any]]:
        pass

    def get_treeview_json(self, link: str) -> Optional[Dict[str, Any]]:
        pass


class TreeViewStatus(StrEnum):
    RUNNING = "RUNNING"
    VERIFIED = "VERIFIED"
    SKIPPED = "SKIPPED"
    TIMEOUT = "TIMEOUT"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"
    SANITY_FAILED = "SANITY_FAILED"
    VIOLATED = "VIOLATED"


class MutationTestRuleStatus(StrEnum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    TIMEOUT = "TIMEOUT"
    SANITY_FAIL = "SANITY_FAIL"
    UNKNOWN = "UNKNOWN"


def convert_to_mutation_testing_status(treeview_status: TreeViewStatus) -> str:
    if treeview_status is TreeViewStatus.VERIFIED or treeview_status is TreeViewStatus.SKIPPED:
        return MutationTestRuleStatus.SUCCESS
    elif treeview_status in TreeViewStatus.VIOLATED:
        return MutationTestRuleStatus.FAIL
    elif treeview_status in TreeViewStatus.TIMEOUT:
        return MutationTestRuleStatus.TIMEOUT
    elif treeview_status in TreeViewStatus.SANITY_FAILED:
        return MutationTestRuleStatus.SANITY_FAIL
    else:
        return MutationTestRuleStatus.UNKNOWN


@dataclass
class RuleResult:
    name: str
    status: str

    def __init__(self, _name: str, _status: str):
        self.name = _name
        self.status = _status


@dataclass
class UIData:
    description: str
    diff: str
    link: str
    name: str
    id: str
    rules: List[Dict[str, Any]]
    # no real need to fill this
    SANITY_FAIL: List[str]
    UNKNOWN: List[str]
    TIMEOUT: List[str]

    def __init__(self, _description: str, _diff: str, _id: str, _name: str, _link: str, _rules: List[RuleResult]):
        # build for a mutant
        self.description = _description
        self.diff = _diff
        self.id = _id
        self.name = _name
        self.link = _link

        self.populate_rules(_rules)

    def populate_rules(self, _rules: List[RuleResult]) -> None:
        x = [dataclasses.asdict(e) for e in  # effing linter
             list(
                 filter(
                     lambda r: r.status == MutationTestRuleStatus.SUCCESS or r.status == MutationTestRuleStatus.FAIL,
                     _rules))]
        self.rules = x
        self.SANITY_FAIL = [r.name for r in _rules if r.status == MutationTestRuleStatus.SANITY_FAIL]
        self.UNKNOWN = [r.name for r in _rules if r.status == MutationTestRuleStatus.UNKNOWN]
        self.TIMEOUT = [r.name for r in _rules if r.status == MutationTestRuleStatus.TIMEOUT]


# food for thought - different outputs if the result is not available, and if it is corrupt
def get_results(link: str, fetcher: ReportFetcher) -> Optional[List[RuleResult]]:
    output_json = fetcher.get_output_json(link)
    if output_json is None:
        print(f"failed to get results for {link}")
        return None

    if Constants.RULES not in output_json:
        print("Bad format for output.json")
        return None

    # now we no longer use output_json

    progress_json = fetcher.get_treeview_json(link)
    if progress_json is None:
        print("Could not get progress object")
        return None
    top_level_rules = get_top_level_rules(progress_json)
    if top_level_rules is None:
        print("Could not get tree view object")
        return None
    rule_results = []

    for rule in top_level_rules:
        # as long as we have children, we need to keep looking.
        # we prioritize failures, then unknown, then timeout, then sanity_fail, and only all success is a success
        if Constants.CHILDREN not in rule:
            print(f"Bad format for a rule {rule}")
            return None

        if Constants.NAME not in rule:
            print(f"Bad format for a rule {rule}")
            return None

        leaf_statuses: List[str] = []
        rec_collect_statuses_children(rule, leaf_statuses)

        name = rule[Constants.NAME]
        if len(leaf_statuses) == 0:
            print("Got no rule results")
            return None
        elif any([s is MutationTestRuleStatus.FAIL for s in leaf_statuses]):
            rule_results.append(RuleResult(name, MutationTestRuleStatus.FAIL))
        elif any([s is MutationTestRuleStatus.UNKNOWN for s in leaf_statuses]):
            rule_results.append(RuleResult(name, MutationTestRuleStatus.UNKNOWN))
        elif any([s is MutationTestRuleStatus.TIMEOUT for s in leaf_statuses]):
            rule_results.append(RuleResult(name, MutationTestRuleStatus.TIMEOUT))
        elif any([s is MutationTestRuleStatus.SANITY_FAIL for s in leaf_statuses]):
            rule_results.append(RuleResult(name, MutationTestRuleStatus.SANITY_FAIL))
        elif not all([s == MutationTestRuleStatus.SUCCESS for s in leaf_statuses]):
            print("Encountered a new unknown status which isn't FAIL, UNKNOWN, TIMEOUT, SANITY_FAIL, or SUCCESS")
            return None
        else:
            rule_results.append(RuleResult(name, MutationTestRuleStatus.SUCCESS))

    return rule_results


def rec_collect_statuses_children(rule: Dict[str, Any], statuses: List[str]) -> None:
    children = rule[Constants.CHILDREN]
    if len(children) == 0:
        statuses.append(convert_to_mutation_testing_status(rule[Constants.STATUS]))
    else:
        for child in children:
            rec_collect_statuses_children(child, statuses)


def get_file_url_from_orig_url(url: str, file: str) -> str:
    return url.replace(Constants.JOB_STATUS, Constants.OUTPUT).replace(f"?{Constants.ANONYMOUS_KEY}",
                                                                       f"/{file}?{Constants.ANONYMOUS_KEY}")


def get_top_level_rules(progress_json: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    if Constants.VERIFICATION_PROGRESS not in progress_json:
        print(f"Could not find {Constants.VERIFICATION_PROGRESS} in progress {progress_json}")
        return None
    # verification progress holds a string which is a json encoding of the latest tree view file
    tree_view_json = json.loads(progress_json[Constants.VERIFICATION_PROGRESS])
    if Constants.RULES not in tree_view_json:
        print(f"Could not find rules in tree view file {tree_view_json}")
        return None

    return tree_view_json[Constants.RULES]


def poll_collect(args: argparse.Namespace) -> None:
    SECONDS_IN_MINUTE = 60
    poll_timeout_seconds = args.poll_timeout * SECONDS_IN_MINUTE
    start = time.time()
    duration = 0  # seconds
    attempt_number = 1
    retry = 15
    ready = False
    while duration < poll_timeout_seconds:
        print(f"-------> Trying to poll results... attempt #{attempt_number}")
        ready = collect(args)
        if not ready:
            print(f"-------> Results are still not ready, trying in {retry} seconds")
            attempt_number += 1
            time.sleep(retry)
        else:
            return
        duration = int(time.time() - start)

    if not ready:
        print(f"Could not get results after {attempt_number} attempts. Exiting")
        sys.exit(1)

class Constants(StrEnum):
    VERIFICATION_PROGRESS = "verificationProgress"
    RULES = "rules"
    JOB_STATUS = "jobStatus"
    PROGRESS = "progress"
    OUTPUT = "output"
    NAME = "name"
    ID = "id"
    DIFF = "diff"
    DESCRIPTION = "description"
    ORIGINAL = "original"
    MUTANTS = "mutants"
    GAMBIT_MUTANT = "gambit_mutant"
    FILENAME = "filename"
    LINK = "link"
    CERTORA_KEY = "certoraKey"
    ANONYMOUS_KEY = "anonymousKey"
    PRE_SIGNED_URL = "preSignedUrl"
    STATUS = "status"
    CHILDREN = "children"


default_cookies = {str(Constants.CERTORA_KEY): os.getenv(KEY_ENV_VAR, '')}


class FileFetcher(ReportFetcher):

    # in the file fetcher, all links are to the main emv directory
    def get_output_json(self, link: str) -> Optional[Dict[str, Any]]:
        output_path = Path(link) / "Reports" / "output.json"
        if not output_path.is_file():
            print("Got no output.json file")
            return None

        with open(output_path, 'r') as output_handle:
            output_json = json.load(output_handle)

        return output_json

    def get_treeview_json(self, link: str) -> Optional[Dict[str, Any]]:
        # it's a hack, but in web we need to go through the verificationProgress and locally we don't.
        treeview_path = Path(link) / "Reports" / "treeView"

        # look out for the "latest" tree view file
        candidates = list(treeview_path.glob(r"treeViewStatus_*.json"))
        max = None
        max_no = -1
        for candidate in candidates:
            if candidate.is_file():
                index = int(str(candidate.stem).split("_")[1])
                if index > max_no:
                    max = candidate
                    max_no = index
        # max should contain the latest tree view file
        if max is None:
            print("No matching treeview files found")
            return None

        treeview_file = max
        with open(treeview_file, 'r') as treeview_handle:
            treeview_str = json.load(treeview_handle)

        # wrap the json as a string inside another json mimicking progress URL
        return {Constants.VERIFICATION_PROGRESS: json.dumps(treeview_str)}

        # we engineer this to give us what `get_top_level_rules` expected
        # resp = self.web_utils.get_response_with_timeout(url.replace(Constants.JOB_STATUS, Constants.PROGRESS),
        #                                              default_cookies)
        # if resp is None:
        #     return None
        # if resp.status_code != 200:
        #     print(f"Got bad response code {resp.status_code}")
        #     return None
        # return resp.json()


class WebFetcher(ReportFetcher):
    def __init__(self, _web_utils: WebUtils):
        self.web_utils = _web_utils

    def get_output_json(self, url: str) -> Optional[Dict[str, Any]]:
        resp = self.web_utils.get_response_with_timeout(get_file_url_from_orig_url(url, "output.json"), default_cookies)
        if resp is None:
            return None
        if resp.status_code != 200:
            print(f"Got bad response code {resp.status_code}")
            return None
        return resp.json()

    def get_treeview_json(self, url: str) -> Optional[Dict[str, Any]]:
        resp = self.web_utils.get_response_with_timeout(url.replace(Constants.JOB_STATUS, Constants.PROGRESS),
                                                        default_cookies)
        if resp is None:
            return None
        if resp.status_code != 200:
            print(f"Got bad response code {resp.status_code}")
            return None
        return resp.json()


if __name__ == '__main__':
    gambit_entry_point()
