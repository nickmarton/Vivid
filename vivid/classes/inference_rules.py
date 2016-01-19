# -*- coding: utf-8 -*-
"""This module provides the rules of diagrammatic inference."""

from formula import Formula
from assumption_base import AssumptionBase
from context import Context
from variable_assignment import VariableAssignment


def thinning(context, named_state, assumption_base=None,
             attribute_interpretation=None):
    """
    Verify that NamedState object in ``named_state`` parameter can be obtained
    by thinning from the NamedState object contained in Context object in
    ``context`` parameter w.r.t. the AssumptionBase object given by the
    ``assumption_base`` parameter, using the AttributeInterpretation object in
    the ``attribute_interpretation`` parameter to interpret truth values.

    By Corollary 26, if
    :math:`(\sigma;\\rho) \\Vvdash_{\{F_{1}, \ldots, F_{n}\}} \
    (\sigma^{\prime};\\rho^{\prime})`
    then
    :math:`(\{F_{1}, \ldots, F_{n}\}; (\sigma; \\rho)) \models \
    (\sigma^{\prime};\\rho^{\prime})`.

    Then, by weakening, :math:`(\\beta \cup \{F_{1}, \ldots, F_{n}\}; \
    (\sigma; \\rho)) \models (\sigma^{\prime};\\rho^{\prime})` and thinning
    holds, thus it suffices to show that a call to ``entails_named_state`` with
    context :math:`(\{F_{1}, \ldots, F_{n}\};(\sigma;\\rho))` and named state
    :math:`(\sigma^{\prime};\\rho^{\prime})`, that is
    :math:`(\sigma;\\rho) \\Vvdash_{\{F_{1}, \ldots, F_{n}\}} \
    (\sigma^{\prime};\\rho^{\prime})`, holds to show that thinning holds.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))`.
    :type  context: Context
    :param named_state: The NamedState object \
    :math:`(\sigma^{\prime};\\rho^{\prime})`
    :type  named_state: NamedState
    :param assumption_base: The set of Formula objects to thin with \
    :math:`\{F_{1},\ldots, F_{n}\}` if thinning is to be done with any \
    Formula (i.e., :math:`n > 0`), otherwise ``None``.
    :type  assumption_base: AssumptionBase | ``None``
    :param attribute_interpretation: The AttributeInterpretation object to \
    use to interpret truth values if :math:`n > 0`, otherwise ``None``.
    :type  attribute_interpretation: AttributeInterpretation | ``None``

    :return: Whether or not thinning holds, i.e., the result of \
    :math:`(\sigma;\\rho) \\Vvdash_{\{F_{1}, \ldots, F_{n}\}} \
    (\sigma^{\prime};\\rho^{\prime})`
    :rtype: ``bool``

    :raises TypeError: ``context`` parameter must be a Context object and \
    ``named_state`` parameter must be a NamedState object.
    """

    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(named_state, "_is_NamedState"):
        raise TypeError("named_state parameter must be a NamedState object.")

    # If no assumption_base are provided, just do thinning for Named States,
    # otherwise, we're doing the full thinning inference rule
    if not assumption_base:
        return named_state <= context._named_state
    else:
        proviso = context._named_state.is_named_entailment(
            assumption_base, attribute_interpretation, named_state)
        return proviso


def widening(context, named_state, attribute_interpretation=None):
    """
    Verify that NamedState object in ``named_state`` parameter can be obtained
    from Context object in ``context`` parameter by widening, using the
    AttributeInterpretation object in the ``attribute_interpretation``
    parameter to interpret truth values.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))`.
    :type  context: Context
    :param named_state: The NamedState object \
    :math:`(\sigma^{\prime};\\rho^{\prime})`
    :type  named_state: NamedState
    :param attribute_interpretation: The AttributeInterpretation object to \
    use to interpret truth values if widening should consider the \
    AssumptionBase object of the ``context`` parameter, otherwise ``None``.
    :type  attribute_interpretation: AttributeInterpretation | ``None``

    :return: Whether or not NamedState object \
    :math:`(\sigma^{\prime};\\rho^{\prime})` in ``named_state`` parameter can \
    be obtained from Context object :math:`(\\beta;(\sigma;\\rho))` in \
    ``context`` parameter can be obtained by widening, i.e., \
    whether or not \
    :math:`(\\beta;(\sigma;\\rho)) \models (\sigma^{\prime};\\rho^{\prime})`
    :rtype: ``bool``

    :raises TypeError: ``context`` parameter must be a Context object and \
    ``named_state`` parameter must be a NamedState object.
    """

    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(named_state, "_is_NamedState"):
        raise TypeError("named_state parameter must be a NamedState object.")

    if attribute_interpretation:
        context.entails_named_state(named_state, attribute_interpretation)

    return context._named_state <= named_state


def observe(context, formula, attribute_interpretation):
    """
    Determine if a Formula object *F* given by ``formula`` parameter can be
    observed in a Context object :math:`(\\beta;(\sigma;\\rho))` given by
    ``context`` parameter, using the AttributeInterpretation object in the
    ``attribute_interpretation`` parameter to interpret truth values, i.e.,
    determine if **observe** *F* holds in :math:`(\\beta;(\sigma;\\rho))`.

    :param context: The Context object in which the Formula object can \
    potentially be observed.
    :type  context: Context
    :param formula: The (potentially) observable Formula object.
    :type  formula: Formula
    :param attribute_interpretation: The AttributeInterpretation object to \
    use to interpet truth values in the ``context`` and ``formula`` parameters.
    :type  attribute_interpretation: AttributeInterpretation

    :return: Whether or not **observe** *F* holds in \
    :math:`(\\beta;(\sigma;\\rho))`, that is, whether or not \
    :math:`(\\beta;(\sigma;\\rho)) \models F`.
    :rtype: ``bool``
    """

    return context.entails_formula(formula, attribute_interpretation)


def diagrammatic_absurdity(context, named_state, attribute_interpretation):
    """
    Verify that the NamedState object in the ``named_state`` parameter can be
    obtained from the Context object in the ``context`` parameter by absurdity,
    using the AttributeInterpretation object provided in the
    ``attribute_interpretation`` parameter to interpet truth values.

    To show :math:`(\sigma^{\prime};\\rho^{\prime})` **by absurdity**, we must
    show :math:`(\\beta \cup \{\\textbf{false}\}; (\sigma;\\rho)) \
    \models (\sigma^{\prime};\\rho^{\prime})`.

    By lemma 20, :math:`(\\beta \cup \{\\textbf{false}\}; (\sigma;\\rho)) \
    \models (\sigma^{\prime};\\rho^{\prime})`, thus it suffices to show that
    a call to ``entails_named_state`` with context
    :math:`(\\beta;(\sigma;\\rho))` and named state
    :math:`(\sigma^{\prime};\\rho^{\prime})`, that is,
    :math:`(\\beta;(\sigma;\\rho)) \models (\sigma^{\prime};\\rho^{\prime})`
    holds, implicitly assuming that some :math:`F \in \\beta` evaulates
    to **false** (as then no world can satisify the context, i.e., for any
    world :math:`(w; \widehat{\\rho})` derivable from the context
    :math:`(\\beta;(\sigma;\\rho))`,
    :math:`(w; \widehat{\\rho}) \\not\models_{\chi} (\\beta;(\sigma;\\rho))`
    and thus ``entails_named_state`` will always hold yielding
    :math:`(\sigma^{\prime};\\rho^{\prime})` **by absurdity** regardless of
    the NamedState object :math:`(\sigma^{\prime};\\rho^{\prime})` provided in
    the ``named_state`` parameter)

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))`.
    :type  context: Context
    :param named_state: The NamedState object \
    :math:`(\sigma^{\prime};\\rho^{\prime})`.
    :type  named_state: NamedState
    :param attribute_interpretation:
    :type  attribute_interpretation: AttributeInterpretation

    :return: Whether or not :math:`(\sigma^{\prime};\\rho^{\prime})` \
    **by absurdity**, that is, whether or not :math:`(\\beta;(\sigma;\\rho)) \
    \models (\sigma^{\prime};\\rho^{\prime})` holds.
    :rtype: ``bool``

    :raises TypeError: ``context`` parameter must be a Context object and \
    ``named_state`` parameter must be a NamedState object.
    """

    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(named_state, "_is_NamedState"):
        raise TypeError("named_state parameter must be a NamedState object.")

    return context.entails_named_state(named_state, attribute_interpretation)


def diagram_reiteration(context):
    """
    Perform Diagram Reiteration to retrieve the current diagram, i.e., from
    lemma 19: :math:`(\\beta;(\sigma;\\rho)) \models (\sigma;\\rho)`.

    :param context: The Context object :math:`(\\beta;(\sigma;\\rho))` from \
    which to retrieve the current NamedState object :math:`(\sigma;\\rho)`.
    :type  context: Context

    :return: The NamedState object :math:`(\sigma;\\rho)` of the Context \
    object :math:`(\\beta;(\sigma;\\rho))` in ``context`` parameter.
    :rtype: NamedState
    """

    return context._named_state


def sentential_to_sentential(context, F1, F2, G, attribute_interpretation,
                             variable_assignment=None):
    """
    Verify that in the case of a disjunction :math:`F_{1} \lor F_{2}` holding a Context entails
    Formula G either way w.r.t. and AttributeInterpretation.
    """

    if not variable_assignment:
        variable_assignment = VariableAssignment(
            context._named_state._p._vocabulary,
            context._named_state._attribute_system, {}, dummy=True)

    F1_holds = F1.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    F2_holds = F2.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    if F1_holds is not True and F2_holds is not True:
        raise ValueError("disjunction F1 OR F2 does not hold")

    G_holds = G.assign_truth_value(attribute_interpretation,
                                   context._named_state,
                                   variable_assignment)

    if F1_holds and not G_holds:
        return False

    if F2_holds and not G_holds:
        return False

    return True


def diagrammatic_to_diagrammatic(context, inferred_named_state, named_states,
                                 attribute_interpretation, variable_assignment,
                                 *formulae):
    """
    Verify that on the basis of the present diagram and some formulas :math:`F_{1}, \ldots, F_{k}`
    contained in formulae, k >= 0, that for each named_state
    :math:`(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n})`, n > 0, contained in named_states, a named state
    (\sigma^{\prime}; \\rho^{\prime}) can be derived in every one of these n cases.

    This is rule [C1].
    """

    if formulae:
        constant_assignment = context._named_state._p
        basis = Formula.get_basis(constant_assignment, variable_assignment,
                                  attribute_interpretation, *formulae)

        if not context._named_state.is_exhaustive(basis, *named_states):
            raise ValueError(
                "named states are not exahustive on basis of formulae.")

        assumption_base = AssumptionBase(*formulae)
    else:
        assumption_base = AssumptionBase(context._assumption_base._vocabulary)

    proviso = context._named_state.is_named_entailment(
        assumption_base, attribute_interpretation, *named_states)

    if not proviso:
        raise ValueError("[C1] proviso does not hold")

    formulae_union = context._assumption_base._formulae + list(formulae)
    if formulae_union:
        assumption_base_union = AssumptionBase(*formulae_union)
    else:
        assumption_base_union = AssumptionBase(
            context._assumption_base._vocabulary)

    # Determine if (β ∪ {F1,...,Fk}; (σ; ρ)) |= (σ'; ρ'); proviso holds at this
    # point
    extended_context = Context(assumption_base_union, context._named_state)
    if extended_context.entails_named_state(inferred_named_state,
                                            attribute_interpretation):
        return True
    else:
        return False


def sentential_to_diagrammatic(context, F1, F2, named_state,
                               attribute_interpretation,
                               variable_assignment=None):
    """
    Verify that in the case of a disjunction :math:`F_{1} \lor F_{2}` holding a Context entails
    NamedState named_state either way w.r.t. and AttributeInterpretation.

    This is rule [C2].
    """

    if not variable_assignment:
        variable_assignment = VariableAssignment(
            context._named_state._p._vocabulary,
            context._named_state._attribute_system, {}, dummy=True)

    F1_holds = F1.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    F2_holds = F2.assign_truth_value(attribute_interpretation,
                                     context._named_state,
                                     variable_assignment)

    if F1_holds is not True and F2_holds is not True:
        raise ValueError("disjunction F1 OR F2 does not hold")

    if F1 not in context._assumption_base:
        f1_assumption_base = F1 + context._assumption_base
    else:
        f1_assumption_base = context._assumption_base

    if F2 not in context._assumption_base:
        f2_assumption_base = F2 + context._assumption_base
    else:
        f2_assumption_base = context._assumption_base

    f1_context = Context(f1_assumption_base, context._named_state)
    f2_context = Context(f2_assumption_base, context._named_state)

    # get all possible worlds and variable assignments of given named state;
    # because the worlds come from the entailed named state but the contexts
    # use the original context's named state, we're showing that
    # (β ∪ {F1 ∨ F2}; (σ; ρ)) |= (σ'; ρ') by showing that in the case of either
    # F1 or F2, all worlds of the entailed state satisify both contexts and
    # thus (σ'; ρ') follows either way
    possible_worlds = named_state.get_worlds()

    for world in possible_worlds:
        for X in world._generate_variable_assignments():
            satisfies_f1_context = world.satisfies_context(
                f1_context, X, attribute_interpretation)
            satisfies_f2_context = world.satisfies_context(
                f2_context, X, attribute_interpretation)

            if not satisfies_f1_context or not satisfies_f2_context:
                return False
    return True


def diagrammatic_to_sentential(context, F, named_states,
                               attribute_interpretation, variable_assignment,
                               *formulae):
    """
    Verify that on the basis of the present diagram and some formulas :math:`F_{1}, \ldots, F_{k}`
    contained in formulae, k >= 0, that for each named_state
    :math:`(\sigma_{1}; \\rho_{1}), \ldots,(\sigma_{n}; \\rho_{n})`, n > 0, contained in named_states, a formula
    F can be derived in every one of these n cases.

    This is rule [C3].
    """

    if formulae:
        constant_assignment = context._named_state._p
        basis = Formula.get_basis(constant_assignment, variable_assignment,
                                  attribute_interpretation, *formulae)

        if not context._named_state.is_exhaustive(basis, *named_states):
            raise ValueError(
                "named states are not exahustive on basis of formulae.")

        assumption_base = AssumptionBase(*formulae)
    else:
        assumption_base = AssumptionBase(context._assumption_base._vocabulary)

    proviso = context._named_state.is_named_entailment(
        assumption_base, attribute_interpretation, *named_states)

    if not proviso:
        raise ValueError("[C3] proviso does not hold")

    formulae_union = context._assumption_base._formulae + list(formulae)
    if formulae_union:
        assumption_base_union = AssumptionBase(*formulae_union)
    else:
        assumption_base_union = AssumptionBase(
            context._assumption_base._vocabulary)

    # Determine if (β ∪ {F1,...,Fk}; (σ; ρ)) |= F; proviso holds at this point
    extended_context = Context(assumption_base_union, context._named_state)
    if extended_context.entails_formula(F, attribute_interpretation):
        return True
    else:
        return False


def main():
    """dev tests."""
    pass


if __name__ == "__main__":
    main()
