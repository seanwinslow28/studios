# Capistrano's "current" link: one fixed name, swapped safely (2009 to now)

## What it is

Capistrano deploys web apps to servers. Since 2009 it has kept each release in its own dated folder and pointed everything that runs (servers, scheduled jobs) at one link named "current". A deploy builds the new folder, then moves the link. Made by the Capistrano maintainers; about 13,000 GitHub stars.

Rollback docs: https://capistranorb.com/documentation/getting-started/rollbacks/

**Best part to look at: the 3-line fix that made the swap safe** (linked under More details). Before 2014 the link was deleted and remade, leaving a moment with nothing there. The fix makes a temporary link and renames it over "current" in one step, so anything starting up sees the old release or the new one, never a gap.

## How it turned out

- **The pattern became the norm** for deploying to a single server without downtime, for over 15 years, and was copied by Deployer (about 11,100 stars) and many shell scripts.
- **Thin spot:** its own rollback page steers people toward fixing forward and redeploying, and the pattern says nothing about restarting programs that are already running the old release.

## What makes it good, measured

- **The core trick is two commands:** make a temporary link, rename it over "current". The fix that made it atomic was 3 lines added and 2 removed.
- **Tested end to end:** scenario tests deploy to a real machine and check that "current" is a link, that cleanup keeps the right number of releases, that cleanup after many failed deploys never removes the last good one, and that rollback lands on the previous release or one you name.
- **What it leaves in place:** the last 5 releases by default, never the one "current" points at.
- **How it's undone:** one command points "current" back at the previous release, then archives the bad one rather than deleting it.
- **Where it stops, said plainly:** the rollback page admits it does "nothing special" about database changes, and that a failure after the link moves may not be fixed by rolling back.
- **A Mac lesson:** Deployer's version uses a Linux-only option of the move command; on a Mac it quietly falls back to a swap that isn't atomic. Capistrano's rename-into-place form works everywhere.

### Why it's here

Added for Devcraft's first job, keeping scheduled jobs alive across updates. It's the best-tested example of the "one fixed name, moved by one quick swap" idea, with an honest note on where rollback stops.

## What Sean said about it

On the step 2 page of the first job, November 10, 2026, as one of the examples behind the four things he said yes to: nothing still in use gets deleted; one fixed name, moved by one quick swap; tested against the real failure, with a way back that's been tried; says plainly where it stops.

## More details

- The atomic swap: https://github.com/capistrano/capistrano/pull/1097
- Tasks: https://github.com/capistrano/capistrano/blob/master/lib/capistrano/tasks/deploy.rake ; default of 5 releases in `lib/capistrano/defaults.rb`
- Tests: https://github.com/capistrano/capistrano/blob/master/features/deploy.feature
- Deployer's fallback: https://github.com/deployphp/deployer/blob/master/recipe/deploy/symlink.php
- Star counts read November 10, 2026, from GitHub's API.
