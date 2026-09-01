"""The IAM policy evaluation algorithm, implemented.

AWS's evaluation logic is three rules and it is the single most examinable
thing about cloud security:

    1. An EXPLICIT DENY anywhere wins. Always. Nothing overrides it.
    2. Otherwise, an ALLOW that matches grants access.
    3. Otherwise, the request is denied -- the IMPLICIT DENY, which is why a
       brand-new principal can do nothing at all.

Everything confusing about IAM -- why adding a policy did not help, why a
wildcard in one policy did not beat a deny in another -- follows from rule 1.
"""
import fnmatch


def matches(pattern, value):
    """IAM wildcards are glob-like: * for any run, ? for one character."""
    return fnmatch.fnmatchcase(value, pattern)


def evaluate(policies, action, resource, trace=None):
    """Return 'Allow' or 'Deny', and record WHY in trace."""
    allow_reason = None
    for policy in policies:
        for stmt in policy["statements"]:
            act_hit = any(matches(a, action) for a in stmt["Action"])
            res_hit = any(matches(r, resource) for r in stmt["Resource"])
            if not (act_hit and res_hit):
                continue
            if stmt["Effect"] == "Deny":
                if trace is not None:
                    trace["decision"] = "Deny"
                    trace["reason"] = f"EXPLICIT DENY in {policy['name']}"
                return "Deny"            # rule 1 -- immediate, unconditional
            if allow_reason is None:
                allow_reason = f"Allow in {policy['name']}"
    if allow_reason:
        if trace is not None:
            trace["decision"] = "Allow"
            trace["reason"] = allow_reason
        return "Allow"                   # rule 2
    if trace is not None:
        trace["decision"] = "Deny"
        trace["reason"] = "IMPLICIT DENY -- no statement matched"
    return "Deny"                        # rule 3
