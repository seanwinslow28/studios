# Tart.

Tart runs a throwaway copy of macOS inside a window on the Mac: a virtual machine, or VM, which is a whole computer simulated in software. Changes that touch the system, like a Homebrew upgrade, a new launchd job or an installer, can be tried there first and wiped afterwards, so Sean's real Mac never takes the risk. Read this before testing anything that changes the machine rather than a project folder.

## What it's best at.

- **A fresh Mac per test, in seconds.** Download one base image once, then make a fresh copy for each test. The copy shares disk space with the original until it changes something, so making one is quick and nearly free.
- **Scriptable from the terminal.** Clone, start, run a script inside, read the result, delete. An agent can drive the whole loop without clicking.
- **Reproducing a system failure on purpose.** Devcraft's first job is the clearest case: install Homebrew's Python inside the VM, build a venv (a project's private Python folder) and a scheduled job on it, run `brew upgrade`, and watch the job break. Then apply the fix and run the same upgrade again. That's proof Sean can see, and it never touched his Mac.

Where something else beats it:

- **Ordinary Python or shell logic** belongs in pytest or Bats, in seconds instead of minutes. Use the VM only when the test needs a real system.
- **UTM**, free, runs VMs too, but is harder to script.
- **A second user account** on the real Mac shares Homebrew with the first, so it isn't a safe test bed.

## Setup.

- **Needs** an Apple silicon Mac on macOS 13 or later. The newest macOS images need a host on macOS 26 or later; the laptop runs 27.0.1.
- **Install:** `brew install openai/tools/tart`. Since Homebrew 6.0, packages from outside Homebrew's own collection must be trusted before they install; naming the full path like this trusts that one package and nothing else from the same source. Tart's own quick-start page still shows the older `cirruslabs/cli/tart`; a November 2026 guide reports that source stopped updating at 2.32.1 in April, so use OpenAI's.
- **Proof it works:** `tart --version` should print 2.41.1 (October 15, 2026).
- **Licence:** Functional Source License 1.1. Free for any use except selling a product that competes with it, so free for Sean. Each version becomes Apache 2.0, a plain open-source licence, two years after release.
- **Who keeps it:** Cirrus Labs made it; OpenAI now keeps it. The images still come from Cirrus Labs on GitHub's container registry (a download service for images like these).

## Disk: the real cost.

Tart's docs say a macOS image is about 25 GB. Newer images are bigger: a November 2026 guide measured the macOS 27 base image at 34.1 GB to download. The laptop had 57 GB free on November 10, 2026. One image fits, but leaves little room for anything else.

**The Mac Mini may be the better home.** It already runs the overnight jobs, so a VM there tests in the same place the jobs live. Before choosing it, check its free space (`df -h /`), that it's Apple silicon, and its macOS version. That still needs checking.

Clones look bigger than they are. `tart list` may show a clone at 35 GB, but it shares blocks with the image, thanks to the Mac's file system copying only what changes. Measure real use with `df -h /`.

Images and clones live in `~/.tart/`: local VMs in `~/.tart/vms/`, downloaded images in `~/.tart/cache/OCIs/`. When space runs short, `tart clone` and `tart pull` delete the least recently used downloaded images on their own, up to 100 GB by default. Set `TART_NO_AUTO_PRUNE` to stop that.

## Getting the best out of it.

**Pick the image.** Names follow `ghcr.io/cirruslabs/macos-<release>-<variant>:latest`. The macOS 27 images are named `golden-gate`; macOS 26 is `tahoe`. Variants: `vanilla` (plain macOS, signed in automatically), `base` (adds Homebrew, a few developer tools and the Tart Guest Agent, a helper that lets the host run commands inside) and `xcode` (adds Apple's developer app, far bigger). For Devcraft, `base` is right. Test on the same major macOS as the real Mac where you can.

**One golden copy, a fresh clone per test.**

```bash
# once, after Sean's yes: the big download
tart clone ghcr.io/cirruslabs/macos-golden-gate-base:latest golden

# every test
tart clone golden test-1
tart run --no-graphics test-1 &
tart ip test-1 --wait 60 >/dev/null   # wait for it to boot
tart exec -i test-1 bash -s < test-brew-upgrade.sh
tart stop test-1
tart delete test-1
```

`--no-graphics` runs it without a window. `tart exec` runs a command inside a running VM through the Guest Agent, with no network login needed; `-i` passes the script in. `tart exec` needs macOS 14 or later on the host.

**Or SSH in.** The images sign in as `admin`, password `admin`:

```bash
ssh admin@"$(tart ip test-1 --wait 60)"
```

`--wait 60` keeps trying for up to a minute while the VM boots. For scripted SSH, copy a key in once with `tart exec` rather than typing the password each time.

**Build the state you want to test, then keep it.** A fresh image has none of Sean's setup. Start from `golden`, install what the test needs (Homebrew's Python, a venv, a launchd job), stop it, and keep that as `golden-brew`. Every test clones `golden-brew`, so each run starts from exactly the same broken-in state.

**Share a folder read-only.** `tart run --dir=job:~/Code/job:ro test-1` shows the job's folder inside the VM at `/Volumes/My Shared Files/job`. `:ro` means the VM can read it but never change Sean's real files.

**Run the real thing.** The `base` image's Homebrew is as old as the image. Run `brew update` inside before the upgrade test, or the test isn't the upgrade Sean's Mac would get.

## Where it goes wrong.

- **A third VM won't start.** Apple's licence allows at most two macOS VMs running at once on one Mac, and its software enforces it. Stop one before starting another.
- **The disk fills.** Clones left behind, an old image never deleted. Delete each clone when its test ends, and check `df -h /`, not `tart list`.
- **Automatic pruning deletes a downloaded image** to make room, and the next clone starts a 30 GB download nobody asked for. Keep the golden copy as a local VM, which pruning doesn't touch, and know that `TART_NO_AUTO_PRUNE` exists.
- **The VM won't start overnight.** On macOS 15 and later, the host needs a signed-in session or an unlocked login keychain to start VMs. A Mac Mini sitting at the login screen after a restart can't run them.
- **`latest` moves.** Images are rebuilt, so last month's `latest` isn't this month's. Keep your own golden copy and note the date it was made, rather than cloning `latest` again for each test.
- **A VM is not Sean's Mac.** No personal files, different history, maybe a different macOS. A pass in the VM says the mechanism works on a clean Mac; say so plainly, and check the few things that differ.
- **Old Homebrew inside.** Covered above: update first.

## Safety.

- **The first download is big.** About 30 to 35 GB from GitHub's container registry onto a disk with 57 GB free. Ask Sean before it, say which Mac it will land on and how much space it will take.
- **Nothing leaves the VM unless you share it.** The default network setting lets the VM reach the internet but hides it from other devices on the home network. Leave it there; don't switch to bridged networking with the default `admin` password.
- **Delete clones when done.** They're throwaway by design; a forgotten one is just lost disk.
- **Share folders read-only,** so a test can't change Sean's real files.

## More details

- Tart docs: https://tart.run/quick-start/ and https://tart.run/faq/ (storage, pruning, networking).
- Repository, install command and licence: https://github.com/openai/tart, https://github.com/openai/tart/blob/main/LICENSE. Releases: https://github.com/openai/tart/releases. `run`, `exec`, `clone` and `ip` options read from the command sources in the repository, November 10, 2026.
- Image variants: https://github.com/cirruslabs/macos-image-templates. The `macos-golden-gate-base` package exists on GitHub's registry (published November 2026).
- macOS 27 image names, sizes and the old install source stopping at 2.32.1: a third-party guide, https://www.starryhope.com/mac/tart-macos-linux-vms/ (November 4, 2026). Not confirmed on Tart's own pages.
- Homebrew trust for outside packages: https://docs.brew.sh/Tap-Trust
- The two-VM limit: Apple's macOS licence, enforced by its Virtualization framework; explained at https://eclecticlight.co/2022/08/04/virtualisation-on-apple-silicon-macs-8-how-apple-limits-vms/
