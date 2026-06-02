# Brewfile — system dependencies for a wedops dev machine.
#
# Consumed by `./mac` via `brew bundle`. Idempotent: running it again just
# verifies everything is present. Every entry has a reason noted next to it —
# keep this list honest, it's the source of truth for what a machine needs.

# Supabase CLI lives in its own tap.
tap "supabase/tap"

# --- CLIs / daemons -------------------------------------------------------

brew "mise"        # runtime version manager — provisions Node per ~/.config/mise/config.toml
brew "direnv"      # loads gitignored .envrc files (e.g. the GitHub Packages PAT)
brew "starship"    # shell prompt (wired into ~/.zshrc)
brew "redis"       # local Redis for @wedops/zeus-redis + dependents
brew "libpq"       # Postgres client libs/CLIs (psql, pg_dump) for athena/db work; keg-only
brew "netlify-cli" # deploys the static marketing site
brew "supabase/tap/supabase" # Supabase CLI for managed Postgres
brew "ffmpeg"      # media transcoding — also yt-dlp's mux/encode backend
brew "yt-dlp"      # video/audio downloader

# --- GUI apps / casks -----------------------------------------------------

cask "orbstack"      # lightweight Docker engine — provides the `docker` CLI
cask "1password"     # desktop app — its CLI integration unlocks `op` with Touch ID
cask "1password-cli" # `op` — repos' .envrc files read secrets from 1Password, no paste
cask "zed"           # editor
