"""Experiment 4's runnable half -- batch against event-driven ingestion.

⚠ THE SYLLABUS NAMES APACHE KAFKA OR RABBITMQ. Neither is installed here and
neither can be: both need a broker process, and this environment's egress
policy blocks the Debian repositories that would provide one.
`04_kafka_rabbitmq.md` carries the real Kafka and RabbitMQ code and is marked
NOT EXECUTED.

What runs here is the COMPARISON the experiment exists to make, with both
modes implemented over a real in-process queue. The numbers below are
genuinely measured; what they cannot show is broker overhead, network
partitions or consumer-group rebalancing, and the markdown file says so.
"""
import queue
import statistics
import threading
import time

import numpy as np

import fixtures as f

WORK_MS = 2.0          # processing cost per record
N_RECORDS = 300
BATCH_INTERVAL = 0.25  # a batch job wakes every 250 ms


def process(record):
    time.sleep(WORK_MS / 1000.0)
    return record["income"] * 2


def main():
    print("  Experiment 4 -- batch against event-driven ingestion")
    print("""
    ⚠ Apache Kafka and RabbitMQ both need a broker process, which cannot
      be installed here. 04_kafka_rabbitmq.md holds that code, marked
      NOT EXECUTED. What runs below is the same comparison over a real
      in-process queue, with latency measured per record.""")

    df = f.applicants(N_RECORDS, seed=f.SEED)
    records = df.to_dict("records")

    # ---------------------------------------------------------------- batch
    print("\n    --- batch ingestion: wake on a timer, process what arrived")
    produced_at = []
    q = queue.Queue()

    def producer(interval_ms=3.0):
        for r in records:
            t = time.perf_counter()
            produced_at.append(t)
            q.put((t, r))
            time.sleep(interval_ms / 1000.0)

    t0 = time.perf_counter()
    p = threading.Thread(target=producer, daemon=True)
    p.start()
    batch_latencies = []
    processed = 0
    while processed < N_RECORDS:
        time.sleep(BATCH_INTERVAL)
        drained = []
        while not q.empty():
            drained.append(q.get())
        for created, r in drained:
            process(r)
            batch_latencies.append(time.perf_counter() - created)
            processed += 1
    batch_wall = time.perf_counter() - t0

    # ------------------------------------------------------- event-driven
    print("    --- event-driven ingestion: process on arrival")
    q2 = queue.Queue()
    event_latencies = []

    def producer2(interval_ms=3.0):
        for r in records:
            q2.put((time.perf_counter(), r))
            time.sleep(interval_ms / 1000.0)
        q2.put(None)

    t0 = time.perf_counter()
    p2 = threading.Thread(target=producer2, daemon=True)
    p2.start()
    while True:
        item = q2.get()
        if item is None:
            break
        created, r = item
        process(r)
        event_latencies.append(time.perf_counter() - created)
    event_wall = time.perf_counter() - t0

    # ------------------------------------------------------------- results
    def pct(v, p):
        return float(np.percentile(v, p))

    print(f"\n      {N_RECORDS} records, {WORK_MS:.0f} ms of work each, "
          f"arriving every 3 ms")
    print(f"\n      {'mode':<16}{'wall clock':>12}{'p50 latency':>14}"
          f"{'p95 latency':>14}{'max latency':>14}")
    for name, lat, wall in (("batch", batch_latencies, batch_wall),
                            ("event-driven", event_latencies, event_wall)):
        print(f"      {name:<16}{wall:>11.2f}s{pct(lat, 50) * 1000:>13.1f}ms"
              f"{pct(lat, 95) * 1000:>13.1f}ms"
              f"{max(lat) * 1000:>13.1f}ms")

    ratio = pct(batch_latencies, 50) / pct(event_latencies, 50)
    print(f"\n      batch median latency is {ratio:.1f}x the event-driven one")
    print(f"""         LOOK AT THE LATENCY COLUMNS FIRST -- {ratio:.0f}x.
         A batch record waits for the next tick, so its latency is
         dominated by the {BATCH_INTERVAL * 1000:.0f} ms interval
         rather than by the {WORK_MS:.0f} ms of processing. The
         event-driven consumer's p50 of
         {pct(event_latencies, 50) * 1000:.1f} ms is essentially the
         processing time and nothing else.
         THE WALL CLOCK ALSO DIFFERS -- {batch_wall:.2f}s against
         {event_wall:.2f}s -- and that is an artefact of polling, not
         a throughput result: the batch loop sleeps a full interval
         before checking, so it pays up to one extra tick at the start
         and one at the end. Real batch systems amortise setup across
         the batch and usually beat streaming on per-record COST; this
         toy does not model that, and claiming it did would be
         dishonest.
         THAT IS THE WHOLE TRADE-OFF and it is worth stating as a
         rule: batching does not make you faster, it makes you
         EFFICIENT PER RECORD at the cost of latency per record.
         Raise the interval and per-record cost falls further while
         latency rises linearly""")

    print(f"\n      {'':<20}{'batch':<30}{'event-driven'}")
    for a, b, c in [
        ("triggered by", "a schedule", "an arrival"),
        ("latency", "up to the interval", "milliseconds"),
        ("per-record cost", "LOW -- amortised setup", "higher"),
        ("failure", "retry the whole batch", "retry one message"),
        ("backpressure", "the queue grows", "the consumer must keep up"),
        ("ordering", "trivial", "needs partition keys"),
        ("right for", "reports, ETL, billing", "fraud, alerts, personalisation"),
    ]:
        print(f"      {a:<20}{b:<30}{c}")

    print("""         'FAILURE' IS THE ROW THAT DECIDES REAL ARCHITECTURES.
         A batch job that fails at record 9,000 of 10,000 usually
         re-runs the whole batch, which requires every step to be
         IDEMPOTENT -- and making an ETL job idempotent is most of the
         work in writing one.
         A stream consumer retries a single message, but must then
         handle a message that fails for ever: that is what a
         dead-letter queue is for, and it is the first thing missing
         from a student Kafka project""")

    print("""
      what an in-process queue CANNOT show you, and Kafka would:
        * broker durability -- messages survive a consumer crash
        * consumer groups and partition rebalancing
        * replay from an offset, which is Kafka's real advantage
        * network latency and partitions
      04_kafka_rabbitmq.md covers all four, with the code, unrun.""")

    assert pct(batch_latencies, 50) > pct(event_latencies, 50)
    assert abs(batch_wall - event_wall) < max(batch_wall, event_wall) * 0.6
    print("\n    all assertions passed")
    return batch_latencies, event_latencies


if __name__ == "__main__":
    main()
