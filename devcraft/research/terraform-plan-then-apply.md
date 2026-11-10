# Terraform's "plan, then apply": show every change before making it (2014 to now)

## What it is

Terraform is a tool companies use to set up their servers, databases and networks from written settings instead of by clicking around. What earns it a place here is one habit built into its design. Before it changes anything, it shows you a plan: a list of exactly what it will create, change and delete, with a one-line total at the bottom. Nothing happens until you say yes. If you save the plan to a file, Terraform will carry out that plan and nothing else, and it refuses if the world has changed since you made it.

Made by HashiCorp, first released July 28, 2014. In 2023 HashiCorp changed its license, and a group of companies started an open copy called OpenTofu. It kept the same plan-then-apply flow.

Docs: https://developer.hashicorp.com/terraform/cli/commands/plan and https://developer.hashicorp.com/terraform/cli/commands/apply

**Best part to look at: the "Understand plan output" section of the plan page.** Four symbols (create, delete, change in place, delete and recreate) and a total line like "2 to add, 1 to change, 2 to destroy". You can judge a change at a glance without reading code.

## How it turned out

- **Very widely used.** About 50,200 stars on GitHub (a star is a public bookmark). Homebrew, the main Mac installer, counted about 354,000 Terraform installs in the past year across its two listings.
- **The pattern outlived the license fight.** When OpenTofu split off in 2023, it kept plan-then-apply exactly. It has about 30,800 stars and about 93,000 Homebrew installs in a year. People valued the preview habit enough to carry it into the copy.
- **Plan output became the thing reviewers read.** Common team tooling posts the plan into the code review, so a reviewer approves the effect, not just the settings file. I didn't count how often; this is a widely known practice, not a measured one.
- **Why it's believable:** the install and star counts come straight from GitHub and Homebrew, and the behaviour described here is from HashiCorp's own documentation.

## What makes it good, measured

I read HashiCorp's plan and apply pages and HashiCorp's community forum on stale plans. I didn't run Terraform.

- **Preview changes nothing.** The plan page says outright that plan alone doesn't carry out the proposed changes. It only reads the current state of things.
- **Four symbols and one total line.** The whole effect of a change fits on one line before you read any detail.
- **Approval is built in twice.** Run apply on its own and it makes a fresh plan, shows it, and asks you to type yes. Pass it a saved plan instead and passing the file counts as the approval, so the plan you reviewed is the plan that runs.
- **A stale plan is refused.** Before applying a saved plan, Terraform compares the record it planned against with the latest one. If anything moved in between, it stops with "Saved plan is stale" instead of guessing. You make a fresh plan.
- **A machine-readable answer for scripts.** With one extra switch, plan returns 0 for "no changes", 2 for "changes waiting" and 1 for "error". A scheduled check can tell drift (things changed outside Terraform) from failure without reading any text.
- **The skip-the-question switch comes with a warning.** The apply page notes that auto-approve also skips approval of deletions, and recommends reviewing a plan first.
- **The limit, honestly:** plan-then-apply is a preview, not an undo. If an apply fails halfway, Terraform doesn't roll back what it already did. You fix the cause and plan again.

### Why it's here

It's the clearest everyday example of "show me before you do it". For Devcraft's first job, a fix that rewrites scheduled jobs could do the same: a preview mode that lists what would change in a one-line summary, an apply that does only what was shown, and an exit code a script can read. Undo still needs its own plan.

## What Sean said about it

On the shelf Sean saw on November 10, 2026. He didn't single this one out; his pick was uv's design.

## More details

- Terraform plan command: https://developer.hashicorp.com/terraform/cli/commands/plan (sections on saved plans with `-out`, `-detailed-exitcode`, planning modes, and plan output)
- Terraform apply command: https://developer.hashicorp.com/terraform/cli/commands/apply (automatic versus saved plan mode, `-auto-approve`)
- Stale plan behaviour, HashiCorp community forum: https://discuss.hashicorp.com/t/question-on-error-saved-plan-is-stale/52912
- Repositories: https://github.com/hashicorp/terraform and https://github.com/opentofu/opentofu
- Homebrew counts: `hashicorp/tap/terraform` about 313,000 and `terraform` about 41,000, plus `opentofu` about 93,000, 365-day figures read November 10, 2026. Stars read from GitHub's API the same day.
- First release date from the `v0.1.0` tag in the Terraform repository.
- The "no automatic rollback" point is from my reading of how apply works and community guidance on recovering from partial applies. HashiCorp's command pages don't address it directly.
