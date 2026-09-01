# Experiment 4 — batch against event-driven ingestion with Kafka or RabbitMQ

## *** NOT EXECUTED ***

**Both Kafka and RabbitMQ need a broker process**, and neither can be
installed here: this environment's egress policy blocks the Debian
repositories, and neither ships as a pip-installable server. **Nothing in this
file has been run**, and nothing in the notes claims an output for it.

**The runnable half is `04_batch_vs_event.py`**, which
implements both ingestion modes over a real in-process queue and measures the
latency difference: **batch p50 of ~354 ms against event-driven ~2 ms, a
factor of about 160**, on 300 records with a 250 ms batch interval.

What that cannot show is broker durability, consumer groups, replay from an
offset, or network partitions. **Those four are exactly what this file is
for.**

---

## Kafka

```bash
# docker compose up -d, with a single-broker KRaft setup
docker run -d --name kafka -p 9092:9092 apache/kafka:3.9.0
pip install kafka-python
```

### Producer

```python
from kafka import KafkaProducer
import json, time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode(),
    key_serializer=lambda k: k.encode(),
    acks="all",              # wait for ALL in-sync replicas -- see below
    retries=5,
    linger_ms=5,             # batch for 5ms before sending
)

for record in applications:
    producer.send("loan-applications",
                  key=record["region"],      # partition key -- see below
                  value=record)
producer.flush()
```

### Consumer

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "loan-applications",
    bootstrap_servers="localhost:9092",
    group_id="scorer",             # the consumer GROUP
    auto_offset_reset="earliest",
    enable_auto_commit=False,      # commit AFTER processing -- see below
    value_deserializer=lambda v: json.loads(v.decode()),
)

for message in consumer:
    try:
        score(message.value)
        consumer.commit()          # only now
    except Exception:
        send_to_dead_letter(message)
        consumer.commit()          # do not block the partition for ever
```

---

## The four things only a real broker shows you

### 1. Durability, and what `acks` costs

| `acks` | Waits for | Loses data when |
|---|---|---|
| `0` | nothing | **always possible** — fire and forget |
| `1` | the leader | the leader dies before replicating |
| **`all`** | **every in-sync replica** | **only if all replicas die** |

**`acks="all"` is slower and is what you want** for anything financial. The
trade is throughput against durability, and it is a one-line decision most
people never make deliberately.

### 2. Consumer groups and partitions

**A partition is consumed by exactly one consumer in a group.** So:

- **Parallelism is capped by the partition count.** Ten consumers on a
  three-partition topic leaves seven idle. This surprises everyone once.
- **Ordering is guaranteed within a partition, not across the topic.** If all
  events for one applicant must be ordered, they must share a **key** — which
  is why the producer above sets `key=`.
- Adding or removing a consumer triggers a **rebalance**, during which
  consumption pauses.

### 3. Replay from an offset — Kafka's real advantage

**A Kafka topic is a log, not a queue.** Messages are not deleted when
consumed; they are retained for a configured period, and each consumer group
keeps its own **offset**.

```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group scorer --topic loan-applications --reset-offsets --to-earliest --execute
```

> **This is the property that makes Kafka an architectural choice rather than
> a transport.** Deploy a broken model, notice a day later, fix it, and
> **replay yesterday's events through the corrected consumer.** RabbitMQ
> cannot do this — once a message is acknowledged it is gone.

### 4. Delivery semantics

| Guarantee | How | Cost |
|---|---|---|
| At most once | commit before processing | **messages lost on a crash** |
| **At least once** | commit after processing | **duplicates on a crash** — the usual choice |
| Exactly once | transactions + idempotent producer | complex, slower |

> **"At least once" means your consumer must be idempotent.** Scoring the same
> application twice must not create two loan records. That requirement
> propagates all the way into your database schema — a unique constraint on
> the application id — and it is the same idempotency requirement that
> `01_environment_etl.py` puts in the warehouse's
> `PRIMARY KEY`.

---

## RabbitMQ, and how it differs

```bash
docker run -d --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
pip install pika
```

```python
import pika, json

conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
ch = conn.channel()
ch.queue_declare(queue="loan-applications", durable=True)

ch.basic_publish(
    exchange="", routing_key="loan-applications",
    body=json.dumps(record),
    properties=pika.BasicProperties(delivery_mode=2))   # persist to disk


def callback(ch, method, props, body):
    score(json.loads(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)      # ack AFTER


ch.basic_qos(prefetch_count=1)        # do not hand a consumer 100 messages
ch.basic_consume(queue="loan-applications", on_message_callback=callback)
ch.start_consuming()
```

| | **Kafka** | **RabbitMQ** |
|---|---|---|
| Model | **a distributed log** | **a message broker** |
| After consumption | **retained** — replayable | **deleted** |
| Routing | by partition key | **exchanges: direct, topic, fanout** |
| Ordering | per partition | per queue |
| Throughput | very high | high |
| Best for | **event streaming, replay, analytics** | **task queues, complex routing, RPC** |

**Choose Kafka when the events are a record of what happened and you may want
to reprocess them. Choose RabbitMQ when the messages are work to be done and
routing is complicated.** That sentence is the exam answer.

---

## What goes in the lab record

| Item | Value |
|---|---|
| Broker and version | |
| Records sent, partition count, consumer count | |
| **p50 / p95 / max latency, batch vs streaming** | |
| Throughput, records per second, both modes | |
| What happened when you killed a consumer mid-run | |
| What happened when you added a second consumer | |
| Offset after a replay | |
| Same figures from `04_batch_vs_event.py`, for comparison | |

Two experiments worth running, because they cannot be reasoned about:

1. **Start 4 consumers on a 2-partition topic.** How many do work?
2. **Kill a consumer mid-batch with `enable_auto_commit=True`, then with
   `False`.** Count the messages lost or duplicated in each case.
