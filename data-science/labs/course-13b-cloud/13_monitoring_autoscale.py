"""Experiment 13 -- CloudWatch/Stackdriver: monitor an endpoint, set alarms,
and configure auto-scaling rules.

The console steps are in `13_monitoring.md`, NOT EXECUTED.

What runs here is the CONTROL LOOP, which is the part that actually behaves
in ways people do not expect: scaling lags demand, aggressive thresholds
oscillate, cooldowns trade responsiveness for stability, and an alarm on an
average hides the tail. Every one of those is measured below rather than
asserted.
"""
import fixtures as f

CAPACITY_PER_INSTANCE = 150      # requests/sec one instance can serve
MIN_INSTANCES = 2
MAX_INSTANCES = 12


def simulate(traffic, scale_out_at, scale_in_at, cooldown,
             start=MIN_INSTANCES, step=1):
    """A target-tracking autoscaler, one tick per hour.

    The key realism: a scaling decision made at tick t only takes effect at
    tick t+1. Real instances take minutes to boot, so the group is ALWAYS
    sized for the PREVIOUS observation.
    """
    instances = start
    cool = 0
    history = []
    for demand in traffic:
        capacity = instances * CAPACITY_PER_INSTANCE
        util = demand / capacity
        served = min(demand, capacity)
        dropped = demand - served
        history.append({"demand": demand, "instances": instances,
                        "util": util, "dropped": dropped})
        if cool > 0:
            cool -= 1
        elif util > scale_out_at and instances < MAX_INSTANCES:
            instances = min(MAX_INSTANCES, instances + step)
            cool = cooldown
        elif util < scale_in_at and instances > MIN_INSTANCES:
            instances = max(MIN_INSTANCES, instances - step)
            cool = cooldown
    return history


def summarise(history):
    hours = len(history)
    return {
        "instance_hours": sum(h["instances"] for h in history),
        "dropped": sum(h["dropped"] for h in history),
        "peak_instances": max(h["instances"] for h in history),
        "hours_over_90": sum(1 for h in history if h["util"] > 0.90),
        "mean_util": sum(h["util"] for h in history) / hours,
        "changes": sum(1 for a, b in zip(history, history[1:])
                       if a["instances"] != b["instances"]),
    }


def percentile(values, p):
    s = sorted(values)
    k = (len(s) - 1) * p / 100
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def main():
    print("  Experiment 13 -- monitoring, alarms and auto-scaling")

    traffic = f.daily_traffic()
    print(f"\n    a day of traffic: peak {max(traffic)} req/s, "
          f"trough {min(traffic)} req/s, {sum(traffic):,} req/s-hours")
    print(f"    one instance serves {CAPACITY_PER_INSTANCE} req/s; "
          f"group is {MIN_INSTANCES}..{MAX_INSTANCES}")

    # ---- fixed capacity, the baseline -----------------------------------
    print("\n    OPTION 1 -- fixed capacity, sized for peak:")
    need = -(-max(traffic) // CAPACITY_PER_INSTANCE)
    fixed = [{"demand": d, "instances": need,
              "util": d / (need * CAPACITY_PER_INSTANCE),
              "dropped": 0} for d in traffic]
    fs = summarise(fixed)
    print(f"      {need} instances all day = {fs['instance_hours']} "
          f"instance-hours, 0 dropped")
    print(f"      mean utilisation {fs['mean_util'] * 100:.1f}%")
    assert fs["dropped"] == 0
    print("""         nothing is dropped and most of the fleet is idle most of
         the day. That is the pre-cloud bargain: you buy the peak and
         pay for it at 3 a.m.""")

    # ---- autoscaling ----------------------------------------------------
    print("\n    OPTION 2 -- target tracking, scale out above 70%, "
          "in below 40%, cooldown 1:")
    auto = simulate(traffic, 0.70, 0.40, cooldown=1)
    a = summarise(auto)
    print(f"      {'hour':>5}{'demand':>8}{'inst':>6}{'util':>8}{'dropped':>9}")
    for h, row in enumerate(auto):
        flag = "  <-- shortfall" if row["dropped"] else ""
        print(f"      {h:>5}{row['demand']:>8}{row['instances']:>6}"
              f"{row['util'] * 100:>7.0f}%{row['dropped']:>9}{flag}")
    saved = fs["instance_hours"] - a["instance_hours"]
    pct = 100 * saved / fs["instance_hours"]
    print(f"\n      instance-hours {a['instance_hours']} against "
          f"{fs['instance_hours']} fixed -- {pct:.0f}% fewer")
    print(f"      requests dropped: {a['dropped']:,}")
    print(f"      scaling changes : {a['changes']}")
    assert a["instance_hours"] < fs["instance_hours"]
    assert a["dropped"] > 0

    # ---- the honest reading ---------------------------------------------
    worst = max(auto, key=lambda r: r["dropped"])
    hour = auto.index(worst)
    print(f"""
         AUTOSCALING DROPPED {a['dropped']:,} REQUESTS AND FIXED CAPACITY DROPPED
         NONE. The worst hour is {hour}, where demand jumped to {worst['demand']}
         against {worst['instances']} instances -- the group was sized for the
         PREVIOUS hour, because a scaling decision takes effect one
         tick late.
         Autoscaling does not track demand. It CHASES demand, and it
         is always one observation behind. That lag is the cost of the
         {pct:.0f}% saving, and pretending otherwise is how a launch goes
         badly""")

    # ---- tuning the thresholds ------------------------------------------
    print("\n    the same day at different thresholds:")
    print(f"      {'out/in':<12}{'cool':>5}{'inst-hrs':>10}{'dropped':>9}"
          f"{'changes':>9}{'mean util':>11}")
    configs = [(0.70, 0.40, 1), (0.50, 0.30, 1), (0.85, 0.60, 1),
               (0.70, 0.40, 3), (0.50, 0.30, 0)]
    results = {}
    for out, inn, cd in configs:
        r = summarise(simulate(traffic, out, inn, cd))
        results[(out, inn, cd)] = r
        print(f"      {f'{out:.0%}/{inn:.0%}':<12}{cd:>5}"
              f"{r['instance_hours']:>10}{r['dropped']:>9}"
              f"{r['changes']:>9}{r['mean_util'] * 100:>10.0f}%")

    aggressive = results[(0.50, 0.30, 1)]
    lazy = results[(0.85, 0.60, 1)]
    assert aggressive["dropped"] < lazy["dropped"]
    assert aggressive["instance_hours"] > lazy["instance_hours"]
    print(f"""         THE TABLE IS A TRADE-OFF CURVE, NOT A LEADERBOARD.
         Scaling out at 50% drops {aggressive['dropped']:,} requests for {aggressive['instance_hours']} instance-hours;
         scaling out at 85% drops {lazy['dropped']:,} for {lazy['instance_hours']}. You are choosing
         between spare capacity and dropped requests, and only a
         business can say which is worse""")

    no_cool = results[(0.50, 0.30, 0)]
    assert no_cool["dropped"] == 0
    assert no_cool["instance_hours"] > fs["instance_hours"]
    print(f"""
         AND READ THE LAST ROW AGAINST FIXED CAPACITY. Scaling out at
         50% with NO cooldown drops nothing -- and costs {no_cool['instance_hours']}
         instance-hours against fixed capacity's {fs['instance_hours']}.
         AUTOSCALING MADE IT MORE EXPENSIVE. Chase demand hard enough
         and the group overshoots on the way up and lingers on the way
         down, so you buy more than the peak. 'Autoscaling saves
         money' is a claim about a TUNED autoscaler, not about
         autoscaling""")

    long_cool = results[(0.70, 0.40, 3)]
    short_cool = results[(0.70, 0.40, 1)]
    print(f"""
         and the cooldown: 3 ticks gives {long_cool['changes']} scaling changes against
         {short_cool['changes']}, at {long_cool['dropped'] - short_cool['dropped']:+,} dropped requests. A long cooldown
         stops FLAPPING -- scaling out and back in repeatedly around a
         threshold, which costs boot time and stabilises nothing""")

    # ---- what to alarm on -----------------------------------------------
    print("\n    alarms: what to measure, and the trap in each")
    lat = [40, 42, 41, 45, 43, 40, 44, 42, 41, 43,
           41, 42, 40, 44, 43, 41, 42, 45, 40, 900]
    mean = sum(lat) / len(lat)
    p50, p95, p99 = (percentile(lat, p) for p in (50, 95, 99))
    print(f"      20 request latencies, one of them 900 ms:")
    print(f"        mean {mean:.1f} ms   p50 {p50:.1f} ms   "
          f"p95 {p95:.1f} ms   p99 {p99:.1f} ms")
    assert mean < 100 and p99 > 400
    print(f"""         AN ALARM ON THE MEAN ({mean:.0f} ms) NEVER FIRES. One request
         in twenty took 900 ms and the average absorbed it. Alarm on
         p95 or p99, because the tail is where users live -- and note
         that 5% of requests is a lot of users""")

    print(f"\n      {'metric':<22}{'alarm when':<26}{'the trap'}")
    for m, when, trap in (
            ("CPUUtilization", "> 70% for 5 min", "an I/O-bound app never hits it"),
            ("ModelLatency p99", "> 500 ms for 3 min", "the mean hides it"),
            ("Invocation4XXErrors", "> 1% of requests", "a rate, never a raw count"),
            ("Invocation5XXErrors", "> 0 for 1 min", "these are YOUR fault"),
            ("EstimatedCharges", "> your monthly budget", "billing metrics lag ~6 h"),
            ("no invocations at all", "== 0 for 1 hour", "a dead endpoint still bills")):
        print(f"      {m:<22}{when:<26}{trap}")
    print("""         THE LAST ROW IS THE ONE PEOPLE MISS. An endpoint serving
         nothing looks perfect on every performance metric and costs
         the same as a busy one. Alarm on ABSENCE of traffic, and
         alarm on spend -- those two catch the failures that
         monitoring dashboards are blind to""")

    # ---- the cost of the whole day --------------------------------------
    print("\n    what the day cost, at m5.large on-demand:")
    rate = f.EC2["m5.large"]
    for label, hours in (("fixed at peak", fs["instance_hours"]),
                         ("autoscaled", a["instance_hours"])):
        print(f"      {label:<18}{hours:>5} instance-hours  "
              f"${hours * rate:>7.2f}/day   ${hours * rate * 30:>8.2f}/month")
    fixed_month = fs["instance_hours"] * rate * 30
    auto_month = a["instance_hours"] * rate * 30
    spot_month = auto_month * (1 - f.SPOT_DISCOUNT)
    res_month = fixed_month * (1 - f.RESERVED_DISCOUNT)
    print(f"\n      autoscaled on SPOT (-{f.SPOT_DISCOUNT:.0%}, interruptible): "
          f"${spot_month:,.2f}/month")
    print(f"      fixed on RESERVED (-{f.RESERVED_DISCOUNT:.0%}, 1-yr commit): "
          f"${res_month:,.2f}/month")
    assert spot_month < auto_month < fixed_month
    print(f"""         the real answer is usually BOTH: a reserved baseline for
         the floor you always need, autoscaled on-demand or spot for
         the peak. Here that is {MIN_INSTANCES} reserved instances plus the rest
         elastic -- and it beats either pure strategy, which is why
         every cost-optimisation review starts by asking what your
         floor is""")


if __name__ == "__main__":
    main()
