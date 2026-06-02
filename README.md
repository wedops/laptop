# laptop

Set up a fresh Mac for [wedops](https://github.com/wedops) development in one command — inspired by [thoughtbot's `laptop`](https://github.com/thoughtbot/laptop).

## Install

Paste this into Terminal:

```bash
curl -fsSL https://weddingoperatingsystems.com/install.sh | bash
```

You'll be asked for your macOS password once. It's safe to run more than once — every step checks before it acts, so re-running on a configured machine is close to a no-op. Open a new terminal afterward (or `source ~/.zshrc`).

## What it does

- Installs **Homebrew** and the Xcode Command Line Tools
- Installs the system dependencies in [`Brewfile`](Brewfile):
  - `mise` — runtime version manager (provisions Node)
  - `direnv` — loads gitignored `.envrc` files (per-repo secrets)
  - `starship` — shell prompt
  - `redis` — local Redis for `@wedops/zeus-redis` and dependents
  - `libpq` — Postgres client tools (`psql`, `pg_dump`)
  - `netlify-cli`, `supabase` — deploy + managed Postgres CLIs
  - `orbstack` — Docker engine (provides the `docker` CLI)
  - `1password-cli`, `zed`
- Wires `mise`, `starship`, and `direnv` into `~/.zshrc` (only if not already there)
- Provisions **Node** via mise (latest LTS — Node 24+, what the repos require)
- Installs **Claude Code** via Anthropic's native installer (into `~/.local/bin`)

It does **not** touch any individual repo. Cloning a repo and authing to GitHub Packages is repo-specific — the script prints those next steps when it finishes.

## Customizing

The `Brewfile` is the source of truth for what a machine needs. Add a line, re-run the install command, done. Keep each entry's trailing comment honest about why it's there.
