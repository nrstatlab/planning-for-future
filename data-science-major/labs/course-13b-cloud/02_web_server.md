# Experiment 2 -- install and configure Apache/XAMPP on the VM and host a page

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`01_vm_and_hosting.py`, which really does serve a page over TCP and fetch it back**.

---

## Linux (Apache directly)

```bash
sudo apt update && sudo apt install -y apache2
sudo systemctl enable --now apache2
systemctl status apache2

sudo tee /var/www/html/index.html >/dev/null <<'EOF'
<!doctype html>
<title>Sales dashboard</title>
<h1>Retail sales</h1>
EOF

curl -I http://localhost/          # 200, and check the Content-Type
```

From the HOST machine, using the guest's IP from experiment 1:

```
http://192.168.x.x/
```

**If that times out**, work through in this order:

1. `sudo ufw allow 80/tcp` — the guest firewall
2. the network mode: **NAT means the LAN cannot reach the guest** (see
   experiment 1). Switch to Bridged, or forward a port.
3. `sudo ss -tlnp | grep :80` — is Apache bound to `0.0.0.0` or only to
   `127.0.0.1`?

## Windows (XAMPP/WAMP)

Install XAMPP, start **Apache** from the control panel, put the page in
`C:\xampp\htdocs\`, browse to `http://localhost/`.

**Apache will not start** almost always because **port 80 is taken** — by IIS,
by Skype (historically), or by another web server. Change
`Listen 80` to `Listen 8080` in `httpd.conf` and browse to
`http://localhost:8080/`.

## The configuration worth understanding

| Directive | Where | What it does |
|---|---|---|
| `DocumentRoot` | `apache2.conf` / `httpd.conf` | which directory is served |
| `Listen` | `ports.conf` | which port |
| `<VirtualHost>` | `sites-available/` | several sites on one IP, by hostname |
| `DirectoryIndex` | `apache2.conf` | which file `/` serves |
| `AddType` | `mime.types` | the **Content-Type** header |

**`AddType` is the one that bites.** A browser renders your page because the
server *said* `text/html`. Serve it as `text/plain` and the browser shows
source; serve it as `application/octet-stream` and the browser downloads it.
The runnable half asserts this header for exactly that reason.

## Enabling TLS

```bash
sudo apt install -y certbot python3-certbot-apache
sudo certbot --apache -d example.com     # needs a real domain pointing here
```

**You cannot get a certificate for `192.168.1.50`.** Certificate authorities
issue for names they can validate, so a VM on your LAN gets a self-signed
certificate and a browser warning — which is the correct behaviour, not a bug.

## The comparison that ends the experiment

| | This VM | S3 + CloudFront |
|---|---|---|
| Patch Apache | **you, monthly** | not your problem |
| TLS certificate | certbot, and renewals | issued and rotated |
| Survives your laptop closing | **no** | yes |
| Handles a traffic spike | no | yes |
| Cost for a static page | a VM, hourly | **cents per GB** |

**A static site on a VM is a general-purpose computer doing an object store's
job.** That is the point the experiment makes by having you do it the hard way
once.
