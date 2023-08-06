rule equivalence_of_revert_conditions()
{
    bool <Fa>_revert;
    bool <Fb>_revert;
    // using this opposed to generating input parameters is experimental
    env e; calldataarg args;

    <Fa>@withrevert(e, args);
    <Fa>_revert = lastReverted;

    <Fb>@withrevert(e, args);
    <Fb>_revert = lastReverted;

    assert(<Fa>_revert == <Fb>_revert);
}

rule equivalence_of_return_value()
{
    OUTPUTS_DEC

    env e;
    calldataarg args;

    OUTPUTS_IN_A = <Fa>(e, args);
    OUTPUTS_IN_B = <Fb>(e, args);

    COMPARE_OUTPUTS
}
