"""Run a Course 13 A Prolog file as a student does at the swipl prompt.

    python3 prolog_lab.py 01_family_tree.pl

SWI-Prolog consults the file, which prints any warning it has about it, and then each query
the file shows in a comment -- a line "% ?- Goal." -- is asked in turn, in file order. The
transcript has the query, anything the goal prints, and every answer as the toplevel writes
it: "X = asha ;" for each solution and a full stop after the last, "true." or "false.", or the
error. The toplevel cannot be driven from a pipe (it waits for a keypress between answers), so
this asks for all the answers at once; the answers are SWI-Prolog's own, written with the
toplevel's answer_write_options.

Needs SWI-Prolog: tools/data-science/setup_prolog.sh.
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

QUERY = re.compile(r"^%\s*\?-\s*(.+?\.)(?:\s+%.*)?\s*$")
LIMIT = 100           # answers per query, so a query with endless answers still ends
SHOWN = 8             # answers shown in full; past that, the first and the count
SECONDS = 10          # and time, so a query that loops (left recursion) still ends

ASK = r"""
:- set_stream(user_output, alias(user_error)).    % warnings and errors in order, inline
:- set_prolog_flag(on_error, print).              % an error a query shows is not a failed run
:- use_module(library(solution_sequences)).
:- use_module(library(time)).

ask(Text) :-
    format("~n?- ~w~n", [Text]),
    (   catch(term_string(Goal, Text, [variable_names(Names)]), E, (print_message(error, E), fail))
    ->  include([N=_]>>(\+ sub_atom(N, 0, 1, _, '_')), Names, Shown),
        (   catch(call_with_time_limit(%(seconds)d, findall(Shown, limit(%(limit)d, Goal), Answers)),
                  error(E2, _),          % shown without this runner's context, as the toplevel does
                  (print_message(error, error(E2, _)), fail))
        ->  show(Answers)
        ;   true
        )
    ;   true
    ).

show([]) :- !, writeln('false.').
show(Answers) :-                   % as a student presses ; for each, up to %(shown)d of them
    length(Answers, N), N =< %(shown)d, !,
    answers(Answers).
show([First|More]) :-              % more than that: the first, Enter, and how many there are
    answer(First), writeln('.'),
    length([First|More], N),
    (   N >= %(limit)d
    ->  format("% the first of at least ~w answers~n", [N])
    ;   format("% the first of ~w answers~n", [N])
    ).

answers([A]) :- !, answer(A), writeln('.').
answers([A|As]) :- answer(A), writeln(' ;'), answers(As).

answer(All) :-                     % a variable the answer leaves unbound is not shown
    exclude([_=V]>>var(V), All, Bindings),
    (   Bindings == []
    ->  write(true)
    ;   current_prolog_flag(answer_write_options, Options),
        bindings(Bindings, Options)
    ).

bindings([Name=Value], Options) :- !, format("~w = ", [Name]), write_term(Value, Options).
bindings([Name=Value|Rest], Options) :-
    format("~w = ", [Name]), write_term(Value, Options), writeln(','), bindings(Rest, Options).
"""


def queries(text):
    return [m.group(1) for m in map(QUERY.match, text.split("\n")) if m]


def program(path, text):
    goals = ",\n".join(f"    ask({quote(q)})" for q in queries(text)) or "    true"
    return (ASK.replace("%(seconds)d", str(SECONDS)).replace("%(limit)d", str(LIMIT))
            .replace("%(shown)d", str(SHOWN))
            + f"\nmain :-\n    consult({quote(str(path))}),\n{goals}.\n"
            + ":- initialization(main, main).\n")


def quote(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def run(path):
    path = pathlib.Path(path).resolve()
    if not shutil.which("swipl"):
        sys.exit("swipl not found: run tools/data-science/setup_prolog.sh")
    with tempfile.TemporaryDirectory() as tmp:          # the asking program, outside the labs
        runner = pathlib.Path(tmp) / "ask.pl"
        runner.write_text(program(path, path.read_text()))
        res = subprocess.run(["swipl", "--on-error=print", "-q", str(runner)], cwd=path.parent,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=300)
    # the runner's own path is not the student's: name the file as they would see it
    return res.returncode, res.stdout.replace(str(path.parent) + "/", "")


if __name__ == "__main__":
    code, out = run(sys.argv[1])
    sys.stdout.write(out.lstrip("\n"))
    sys.exit(code)
