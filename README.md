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
  - `direnv` — loads each repo's `.envrc` (which pulls secrets from 1Password)
  - `starship` — shell prompt
  - `redis` — local Redis for `@wedops/zeus-redis` and dependents
  - `libpq` — Postgres client tools (`psql`, `pg_dump`)
  - `netlify-cli`, `supabase` — deploy + managed Postgres CLIs
  - `orbstack` — Docker engine (provides the `docker` CLI)
  - `ffmpeg`, `yt-dlp` — media transcoding / downloads
  - `1password` + `1password-cli` — secrets & SSH via `op` (see below); the app also bundles the Safari extension
  - `zed`, `zoom`
- Wires `mise`, `starship`, and `direnv` into `~/.zshrc` (only if not already there)
- Provisions **Node** via mise (latest LTS — Node 24+, what the repos require)
- Installs **Claude Code** via Anthropic's native installer (into `~/.local/bin`)
- Points `~/.ssh/config` at the **1Password SSH agent** (so `git` uses your vault-stored key)

It does **not** touch any individual repo. Cloning a repo and authing is repo-specific — the script prints those next steps when it finishes.

## Secrets & SSH

Both secrets and SSH keys come from **1Password** rather than living on disk:

- Each repo's committed `.envrc` holds an `op://…` *reference* (not the value); direnv resolves it through the 1Password CLI.
- `mac` points `~/.ssh/config` at the 1Password SSH agent, so `git` over SSH uses your vault-stored key with a biometric tap — no private key on disk.

After the install finishes:

1. 1Password app → **Settings → Developer** → enable **"Integrate with 1Password CLI"**, **"Use the SSH agent"**, and Touch ID unlock. For browser autofill, also enable the bundled extension in **Safari → Settings → Extensions → "1Password"**.
2. Make sure you can access the shared **`wedops`** vault — it holds the SSH key (already trusted by GitHub) and the `op://` tokens.
3. Sign in and pull the workspace (cloning over SSH with your vault key):

   ```bash
   op signin
   op document get workspace --vault wedops | bash
   ```

   Clones into `~/code` — the gods monorepo at `~/code/wedops`, the client repos namespaced alongside. Scope to one group with `… | bash -s -- wedops`, or set `WORKSPACE_ROOT=~/path` to clone elsewhere.

> The SSH key was generated inside the `wedops` vault (`op item create --category "SSH Key" --ssh-generate-key Ed25519`) and its public key added to GitHub — the private key never touches a disk. The vault is shared with developers, who inherit it automatically (no per-dev key).

## Customizing

The `Brewfile` is the source of truth for what a machine needs. Add a line, re-run the install command, done. Keep each entry's trailing comment honest about why it's there.
