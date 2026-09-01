# Experiment 7 -- set up Jupyter Notebook / Colab on a cloud VM

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`01_vm_and_hosting.py`, which executes notebook cells and asserts every output**.

---

## On the VM

```bash
sudo apt install -y python3-pip
pip install jupyterlab pandas scikit-learn matplotlib
jupyter lab --generate-config
jupyter lab password                      # set one, do not skip this
```

Then, **do not** open it to the internet. Use an SSH tunnel:

```bash
# on the VM
jupyter lab --no-browser --port=8888 --ip=127.0.0.1

# on your machine
ssh -N -L 8888:localhost:8888 ubuntu@<vm-ip>
# then browse to http://localhost:8888
```

## ⚠ The mistake that matters

```bash
jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.token=''
```

**That publishes a root shell on the internet.** A Jupyter notebook executes
arbitrary code by design, so an unauthenticated notebook is not "an insecure
notebook" — it is a remote code execution endpoint. Scanners find these in
minutes; it is a standard way cloud accounts get used for cryptomining.

**Always: an SSH tunnel, or a managed notebook behind IAM.**

## SageMaker Studio / Vertex Workbench instead

```bash
aws sagemaker create-notebook-instance \
  --notebook-instance-name lab7 --instance-type ml.t3.medium \
  --role-arn arn:aws:iam::<acct>:role/SageMakerExecutionRole
```

You get the tunnel, the authentication and the IAM role for free — **and no
access key is ever written to disk**, which is the real argument for it.

## The lifecycle configuration that saves the money

```bash
#!/bin/bash
# attach as an OnStart lifecycle config
IDLE_TIME=3600
pip install -q jupyter-autoshutdown-extension || true
echo "auto-shutdown after ${IDLE_TIME}s idle" >> /var/log/lifecycle.log
```

**Colab disconnects after about 90 minutes idle and that is an annoyance. A
cloud notebook does not disconnect, and that is a bill.** An idle-shutdown
policy is the single most useful thing to configure on day one.

## Colab against a cloud notebook

| | Colab | Cloud notebook |
|---|---|---|
| Cost | free tier, then paid | the **instance**, hourly |
| Data | upload, or mount Drive | IAM role, no keys |
| Stops when | idle ~90 min | **never — you stop it** |
| State on stop | **lost** | kept on the volume |
| GPU | when available | the one you pay for |
| Private data | a policy question | inside your VPC |

**Colab is excellent for learning and wrong for anything confidential.** The
deciding question is whose infrastructure the data may sit on.
