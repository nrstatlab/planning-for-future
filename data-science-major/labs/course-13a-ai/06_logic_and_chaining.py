"""Experiments 15, 16 and 17 — Logic, chaining, and an expert system.

Experiments 16 and 17 are executed as REAL LOGIC PROGRAMS through pytholog:
the rule base is resolved, not simulated. Experiment 15's propositional
truth tables are computed exhaustively.
"""
import itertools

import pytholog as pl


# --- experiment 15: propositional logic --------------------------------------

def truth_tables():
    """Every connective, over every model. unit-4.md section 4.3's table."""
    rows = []
    for p, q in itertools.product([False, True], repeat=2):
        rows.append((p, q, not p, p and q, p or q, (not p) or q, p == q))

    assert len(rows) == 4
    # P => Q is FALSE only when P is true and Q is false.
    implications = {(p, q): imp for p, q, _, _, _, imp, _ in rows}
    assert implications[(True, False)] is False
    assert implications[(False, False)] is True, "vacuously true"
    assert implications[(False, True)] is True, "vacuously true"
    assert implications[(True, True)] is True

    print("     P      Q     ¬P    P∧Q   P∨Q   P⇒Q   P⇔Q")
    for p, q, np_, pq, poq, imp, iff in rows:
        f = lambda b: " T " if b else " F "
        print(f"    {f(p)}   {f(q)}   {f(np_)}  {f(pq)}  {f(poq)}  "
              f"{f(imp)}  {f(iff)}")
    print("       P⇒Q is TRUE whenever P is false. It is not causation --")
    print("       it says only 'there is no case where P holds and Q fails',")
    print("       which is exactly ¬P ∨ Q")


def implication_equals_not_p_or_q():
    """The equivalence every CNF conversion starts with."""
    for p, q in itertools.product([False, True], repeat=2):
        assert ((not p) or q) == (not (p and not q))
    print("  P⇒Q ≡ ¬P ∨ Q, checked over all 4 models")
    print("       this is step 2 of the CNF procedure, and everything in")
    print("       resolution depends on it")


def validity_satisfiability_entailment():
    """The three notions, computed over all models of three symbols."""
    symbols = ["P", "Q", "R"]
    models = [dict(zip(symbols, vals))
              for vals in itertools.product([False, True], repeat=3)]
    assert len(models) == 8

    def tautology(m):
        return m["P"] or not m["P"]

    def contradiction(m):
        return m["P"] and not m["P"]

    def satisfiable_only(m):
        return m["P"] and m["Q"]

    assert all(tautology(m) for m in models), "VALID -- true in every model"
    assert not any(contradiction(m) for m in models), "UNSATISFIABLE"
    assert sum(satisfiable_only(m) for m in models) == 2, "SATISFIABLE"

    # Entailment: {P, P⇒Q} ⊨ Q. Check every model where the KB holds.
    kb_models = [m for m in models if m["P"] and ((not m["P"]) or m["Q"])]
    assert len(kb_models) == 2
    assert all(m["Q"] for m in kb_models), "Q is true in EVERY model of the KB"

    # And the equivalent formulation: KB ∧ ¬Q is unsatisfiable.
    assert not any(m["P"] and ((not m["P"]) or m["Q"]) and not m["Q"]
                   for m in models)

    print(f"  over {len(models)} models of P, Q, R:")
    print(f"    P ∨ ¬P     true in 8/8  -> VALID (a tautology)")
    print(f"    P ∧ ¬P     true in 0/8  -> UNSATISFIABLE")
    print(f"    P ∧ Q      true in 2/8  -> SATISFIABLE")
    print(f"  entailment: {{P, P⇒Q}} has {len(kb_models)} models, and Q holds in")
    print(f"    all of them, so {{P, P⇒Q}} ⊨ Q")
    print("       and equivalently KB ∧ ¬Q has ZERO models -- unsatisfiable.")
    print("       THAT second form is what resolution mechanises")


def modus_ponens_and_tollens():
    for p, q in itertools.product([False, True], repeat=2):
        implies = (not p) or q
        if implies and p:
            assert q, "modus ponens"
        if implies and not q:
            assert not p, "modus tollens"
    print("  modus ponens  (P⇒Q, P  ⊢ Q) and")
    print("  modus tollens (P⇒Q, ¬Q ⊢ ¬P) verified over all 4 models")
    print("       affirming the consequent (P⇒Q, Q ⊢ P) is NOT valid, and")
    print("       the truth table shows why: row (F, T) has P false and Q true")


# --- experiments 16 and 17: chaining, as a real logic program ----------------

# pytholog needs predicates WITH ARGUMENTS -- a 0-arity proposition such as
# a bare "a" raises IndexError inside its parser. So the same propositional
# rule base is written with a dummy argument, which changes nothing logically.
CHAIN_RULES = [
    "a(x)", "b(x)",
    "c(X) :- a(X), b(X)",
    "d(X) :- c(X)",
    "e(X) :- d(X), a(X)",
]


def forward_chaining():
    """Data-driven: start from facts, apply every rule, repeat."""
    facts = {"a", "b"}
    rules = [(("a", "b"), "c"), (("c",), "d"), (("d", "a"), "e")]

    passes = []
    changed = True
    while changed:
        changed = False
        for premises, conclusion in rules:
            if all(p in facts for p in premises) and conclusion not in facts:
                facts.add(conclusion)
                passes.append(conclusion)
                changed = True

    assert facts == {"a", "b", "c", "d", "e"}
    assert passes == ["c", "d", "e"], passes

    print(f"  facts {{a, b}} + 3 rules")
    print(f"  derived, in order: {passes}")
    print(f"  final knowledge base: {sorted(facts)}")
    print("       forward chaining derives EVERYTHING derivable, whether or")
    print("       not it was wanted. Data-driven")


def backward_chaining_through_resolution():
    """Goal-driven -- and this one is a REAL logic program."""
    kb = pl.KnowledgeBase("chain")
    kb(CHAIN_RULES)

    for goal in ("c(x)", "d(x)", "e(x)"):
        result = kb.query(pl.Expr(goal))
        assert result == ["Yes"], (goal, result)

    # A goal whose predicate is not in the KB at all raises rather than
    # answering "No" -- another engine limitation, asserted not hidden.
    try:
        kb.query(pl.Expr("z(x)"))
        raise SystemExit("expected pytholog to raise on an unknown predicate")
    except TypeError:
        pass

    print("  the same rule base, queried backwards through SLD resolution:")
    for goal in ("c(x)", "d(x)", "e(x)"):
        print(f"    ?- {goal}.   -> Yes")
    print("    ?- z(x).     -> TypeError (pytholog raises on an unknown")
    print("                    predicate where SWI-Prolog answers 'false')")
    print("       backward chaining proves ONLY what was asked. To prove e it")
    print("       needs d, which needs c, which needs a and b -- and it never")
    print("       derives anything outside that chain. Goal-driven")


def which_chaining_to_use():
    scenarios = [
        ("A sensor reading arrives; what does it imply?",
         "FORWARD", "few facts, many possible conclusions"),
        ("Does this patient have malaria?",
         "BACKWARD", "many facts, ONE question"),
        ("Monitoring a plant for alarm conditions",
         "FORWARD", "you want every consequence, continuously"),
        ("Diagnosing why a car will not start",
         "BACKWARD", "test only the hypotheses that matter"),
    ]
    assert sum(1 for _, d, _ in scenarios if d == "FORWARD") == 2

    print("    scenario                                  use        because")
    for scenario, direction, why in scenarios:
        print(f"    {scenario:41} {direction:10} {why}")
    print("       the deciding question is: how many possible conclusions, and")
    print("       how many facts? Prolog is BACKWARD chaining with depth-first")
    print("       search, which is why a left-recursive rule loops for ever")


# --- experiment 17: a rule-based expert system -------------------------------

MEDICAL_KB = [
    # facts about one patient, in working memory
    "fever(patient)",
    "cough(patient)",
    "fatigue(patient)",
    # rules -- the knowledge base proper
    "viral(X) :- fever(X), cough(X)",
    "flu(X) :- viral(X), fatigue(X)",
    "bacterial(X) :- fever(X), rash(X)",
    "rest_advised(X) :- flu(X)",
]


def expert_system():
    """A small diagnostic system, resolved rather than simulated."""
    kb = pl.KnowledgeBase("medical")
    kb(MEDICAL_KB)

    assert kb.query(pl.Expr("viral(patient)")) == ["Yes"]
    assert kb.query(pl.Expr("flu(patient)")) == ["Yes"]
    assert kb.query(pl.Expr("rest_advised(patient)")) == ["Yes"]
    # No rash was recorded, so bacterial cannot be derived.
    assert kb.query(pl.Expr("bacterial(patient)")) != ["Yes"]

    print("  working memory: fever, cough, fatigue")
    for goal in ("viral(patient)", "flu(patient)", "rest_advised(patient)"):
        print(f"    ?- {goal:22} -> Yes")
    print(f"    ?- bacterial(patient)     -> not derivable (no rash recorded)")
    print()
    print("  the EXPLANATION FACILITY, reconstructed from the derivation:")
    print("    HOW did you conclude rest_advised(patient)?")
    print("      by rule  rest_advised(X) :- flu(X)")
    print("      flu(patient)     by  flu(X) :- viral(X), fatigue(X)")
    print("        viral(patient) by  viral(X) :- fever(X), cough(X)")
    print("          fever(patient)   -- a fact in working memory")
    print("          cough(patient)   -- a fact in working memory")
    print("        fatigue(patient)   -- a fact in working memory")
    print("       THAT is what an expert system has and a neural network does")
    print("       not. The chain IS the explanation, and it falls out of the")
    print("       proof for free")


def the_closed_world_assumption_shows_here():
    """'Not derivable' is not the same as 'false'."""
    kb = pl.KnowledgeBase("medical2")
    kb(MEDICAL_KB)

    result = kb.query(pl.Expr("bacterial(patient)"))
    assert result != ["Yes"]

    # Add the missing symptom and the conclusion appears.
    kb2 = pl.KnowledgeBase("medical3")
    kb2(MEDICAL_KB + ["rash(patient)"])
    assert kb2.query(pl.Expr("bacterial(patient)")) == ["Yes"]

    print(f"  without rash: bacterial(patient) -> {result}")
    print(f"  add rash(patient): bacterial(patient) -> ['Yes']")
    print("       the first answer means 'I cannot prove it', NOT 'it is false'.")
    print("       An expert system under the closed world assumption reports")
    print("       the same thing for 'definitely not' and 'I was never told' --")
    print("       which is exactly the BRITTLENESS of unit-5.md section 5.1")


def main():
    print("Experiments 15-17 -- Logic, chaining and an expert system")
    print("  experiment 15 -- propositional logic:")
    truth_tables()
    implication_equals_not_p_or_q()
    validity_satisfiability_entailment()
    modus_ponens_and_tollens()
    print("  experiment 16 -- forward chaining:")
    forward_chaining()
    print("  experiment 16 -- backward chaining (real resolution):")
    backward_chaining_through_resolution()
    which_chaining_to_use()
    print("  experiment 17 -- a rule-based expert system:")
    expert_system()
    the_closed_world_assumption_shows_here()


if __name__ == "__main__":
    main()
