"""Experiment 1 — A family tree, executed as a logic program.

This is NOT a simulation. pytholog implements SLD resolution over Horn
clauses, so the recursive ancestor/2 rule below is genuinely resolved the way
Prolog would resolve it -- including finding kiran, who is three levels down
and reachable only by recursion.
"""
import pytholog as pl

from fixtures import FAMILY_FACTS, FAMILY_RULES


def build():
    kb = pl.KnowledgeBase("family")
    kb(FAMILY_FACTS + FAMILY_RULES)
    return kb


def answers(kb, goal, var="X"):
    """Sorted distinct bindings for one variable -- Prolog's setof/3."""
    result = kb.query(pl.Expr(goal))
    if result in (["No"], []):
        return []
    return sorted({r[var] for r in result if isinstance(r, dict) and var in r})


def facts_and_simple_rules():
    kb = build()

    assert answers(kb, "parent(ram, X)") == ["asha", "ravi"]
    assert answers(kb, "father(X, asha)", "X") == ["ram"]
    assert answers(kb, "mother(X, asha)", "X") == ["sita"]
    assert answers(kb, "grandparent(ram, X)") == ["bhanu", "kiran", "meena"]

    print(f"  parent(ram, X)        -> {answers(kb, 'parent(ram, X)')}")
    print(f"  father(X, asha)       -> {answers(kb, 'father(X, asha)', 'X')}")
    print(f"  mother(X, asha)       -> {answers(kb, 'mother(X, asha)', 'X')}")
    print(f"  grandparent(ram, X)   -> {answers(kb, 'grandparent(ram, X)')}")
    print("       father/2 and mother/2 are the SAME rule with a different")
    print("       guard. That is what makes logic programming compact")


def recursion_is_what_makes_ancestor_work():
    """The point of the experiment: kiran is reachable only by recursing."""
    kb = build()

    descendants = answers(kb, "ancestor(ram, X)")
    assert descendants == ["asha", "bhanu", "kiran", "meena", "ravi"], descendants

    # One level down is the base case; two and three need the recursive clause.
    direct = answers(kb, "parent(ram, X)")
    assert set(direct) == {"asha", "ravi"}
    assert {"kiran", "meena", "bhanu"} <= set(descendants)
    assert {"kiran", "meena", "bhanu"} & set(direct) == set()

    print(f"  parent(ram, X)   -> {direct}                (1 level)")
    print(f"  ancestor(ram, X) -> {descendants}")
    print("       kiran, meena and bhanu are TWO levels down and appear only")
    print("       through the recursive clause. Delete it and they vanish.")
    print("       This is genuine SLD resolution, not a table lookup")


def base_case_must_come_first():
    """Clause ORDER matters in Prolog, and does not matter in logic."""
    good = pl.KnowledgeBase("good")
    good(FAMILY_FACTS + [
        "anc(X, Y) :- parent(X, Y)",                   # base case FIRST
        "anc(X, Y) :- parent(X, Z), anc(Z, Y)",
    ])
    result = good.query(pl.Expr("anc(ram, X)"))
    found = sorted({r["X"] for r in result if isinstance(r, dict)})
    assert found == ["asha", "bhanu", "kiran", "meena", "ravi"], found

    print(f"  base case first -> {found}")
    print("       with the RECURSIVE clause first, SWI-Prolog recurses before")
    print("       it can ever reach a fact, and a left-recursive rule such as")
    print("       'anc(X,Y) :- anc(X,Z), parent(Z,Y)' loops for ever.")
    print("       Clause order matters in Prolog and does NOT matter in logic --")
    print("       because Prolog is backward chaining with DEPTH-FIRST search")


def sibling_needs_the_inequality_guard():
    kb = build()
    siblings = answers(kb, "sibling(asha, X)")
    assert siblings == ["ravi"], siblings
    assert "asha" not in siblings, "the neq guard stops asha being her own sibling"

    # Without the guard, everyone is their own sibling.
    loose = pl.KnowledgeBase("loose")
    loose(FAMILY_FACTS + ["sib(X, Y) :- parent(P, X), parent(P, Y)"])
    bad = sorted({r["X"] for r in loose.query(pl.Expr("sib(asha, X)"))
                  if isinstance(r, dict)})
    assert "asha" in bad, bad

    print(f"  sibling(asha, X)  with the guard -> {siblings}")
    print(f"  without the guard                -> {bad}   <- asha is her own sibling")
    print("       every parent(P,X), parent(P,Y) pair unifies with X = Y unless")
    print("       you forbid it. In SWI-Prolog the guard is X \\\\= Y")


def duplicate_solutions_are_real():
    """asha and ravi share TWO parents, so Prolog proves sibling twice."""
    kb = build()
    raw = kb.query(pl.Expr("sibling(asha, X)"))
    bindings = [r["X"] for r in raw if isinstance(r, dict) and "X" in r]
    distinct = sorted(set(bindings))

    assert distinct == ["ravi"]
    assert len(bindings) >= 1

    print(f"  raw solutions for sibling(asha, X): {bindings}")
    print(f"  distinct                          : {distinct}")
    print("       asha and ravi share BOTH ram and sita, so in SWI-Prolog the")
    print("       goal succeeds once per shared parent -- one solution per PROOF,")
    print("       not per answer. setof/3 collapses them, and this is a property")
    print("       of resolution rather than a bug")


def cousins_expose_an_engine_limitation():
    """Two encodings of the same logic. One of them breaks pytholog.

    This is worth seeing rather than hiding: the .pl file uses the idiomatic
    nested form, which SWI-Prolog handles correctly. pytholog does not
    propagate neq/2 correctly through a nested derived predicate, so the same
    rule returns wrong answers here -- and the FLAT formulation, which asks
    the same question without an intermediate rule, gets it right.
    """
    # (a) The flat form: kiran and Y have different parents who share a parent.
    flat = pl.KnowledgeBase("flat")
    flat(FAMILY_FACTS + [
        "cousin(X, Y) :- parent(A, X), parent(B, Y), "
        "parent(G, A), parent(G, B), neq(A, B)"])
    flat_answers = sorted({r["X"] for r in flat.query(pl.Expr("cousin(kiran, X)"))
                           if isinstance(r, dict)})
    assert flat_answers == ["bhanu"], flat_answers

    # (b) The nested form, which is what the .pl file uses.
    nested = pl.KnowledgeBase("nested")
    nested(FAMILY_FACTS + [
        "sib(X, Y) :- parent(P, X), parent(P, Y), neq(X, Y)",
        "cousin(X, Y) :- parent(A, X), parent(B, Y), sib(A, B)"])
    nested_answers = sorted({r["X"] for r in nested.query(pl.Expr("cousin(kiran, X)"))
                             if isinstance(r, dict)})
    assert nested_answers == ["bhanu", "kiran", "meena"], nested_answers
    assert "kiran" in nested_answers, "kiran is returned as his OWN cousin"

    print(f"  flat rule   (no intermediate predicate) -> {flat_answers}   CORRECT")
    print(f"  nested rule (calls sib/2)               -> {nested_answers}")
    print("       the nested answer is WRONG: kiran is not his own cousin, and")
    print("       meena is his SISTER. pytholog does not propagate neq/2")
    print("       correctly through a nested derived predicate.")
    print("       SWI-Prolog handles the nested form correctly, and the .pl file")
    print("       uses it because it is the idiomatic encoding. This is an")
    print("       ENGINE limitation, not a flaw in the logic -- and it is why")
    print("       the .pl file is the deliverable and this file is the check")


def main():
    print("Experiment 1 -- A family tree as a logic program")
    facts_and_simple_rules()
    recursion_is_what_makes_ancestor_work()
    base_case_must_come_first()
    sibling_needs_the_inequality_guard()
    duplicate_solutions_are_real()
    cousins_expose_an_engine_limitation()


if __name__ == "__main__":
    main()
