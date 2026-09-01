# Experiment 1 -- create a virtual machine in VMware Workstation

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`01_vm_and_hosting.py`, which models overcommit and measures where it breaks**.

---

## The wizard, and what each choice actually means

| Step | Choice | Why it matters |
|---|---|---|
| New Virtual Machine | **Custom (advanced)** | Typical hides the disk and network options you need |
| Hardware compatibility | Workstation 17.x | older only if you must move the VM to an older host |
| Guest OS install | **Install later** | attach the ISO after, so the wizard does not run an unattended install |
| Guest OS | Linux → Ubuntu 64-bit | picks sensible defaults for the virtual chipset |
| Processors | 2 cores | more than the host has *physical* cores makes it slower, not faster |
| Memory | 4096 MB | see the overcommit note below |
| Network | **NAT** | the guest shares the host's IP; Bridged gives it one on your LAN |
| Disk controller | NVMe (or SCSI) | IDE is slow and there is no reason for it |
| Disk | 40 GB, **split**, **not** pre-allocated | see the disk note below |

## The three choices that get people

**1. Memory.** The host must keep enough for itself. Giving a 16 GB laptop's
VM 12 GB leaves 4 GB for Windows, the hypervisor and your browser, and the
whole machine swaps. **Type 2 hypervisors do not balloon aggressively**, so
the overcommit that works in a datacentre does not work here.

**2. Disk: "Allocate all disk space now" vs "split into multiple files".**
Pre-allocating writes 40 GB immediately and is faster afterwards. Not
pre-allocating grows on demand and is what you want on a laptop. Splitting
into 2 GB files matters only for filesystems that cannot hold a 40 GB file
(FAT32) — and for copying the VM to a USB stick.

**3. NAT vs Bridged vs Host-only.**

| Mode | The guest gets | Reachable from the LAN? |
|---|---|---|
| **NAT** | a private IP behind the host | **no**, unless you forward a port |
| **Bridged** | an IP from your router's DHCP | **yes** |
| Host-only | a private IP, no internet | no |

**Choose NAT and then wonder why nobody can reach your web server** — that is
experiment 2's most common failure, and the fix is either Bridged or a port
forward in `Edit → Virtual Network Editor`.

## After the install

```bash
sudo apt update && sudo apt install -y open-vm-tools open-vm-tools-desktop
# ^ shared clipboard, drag-and-drop, correct screen resolution
ip addr show          # note the guest's IP -- you need it for experiment 2
free -h ; nproc ; df -h
```

**Take a snapshot before you install anything else.** `VM → Snapshot → Take
Snapshot`. A snapshot is the only reason experimenting in a VM is safe, and
it is the feature that has no cheap equivalent on physical hardware.

## The link forward

Every EC2 instance, Azure VM and GCE instance is a guest on a **type 1**
hypervisor — ESXi, Hyper-V, KVM or AWS's Nitro. **The cloud is this
experiment at rack scale**, with the wizard replaced by an API call. Knowing
what the wizard was choosing is what makes an instance type comprehensible.
