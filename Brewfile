# Brewfile — system dependencies for a wedops dev machine.
#
# Consumed by `./mac` via `brew bundle`. Idempotent: running it again just
# verifies everything is present. Every entry has a reason noted next to it —
# keep this list honest, it's the source of truth for what a machine needs.

# --- CLIs / daemons -------------------------------------------------------

brew "mise"        # runtime version manager — provisions Node per ~/.config/mise/config.toml
brew "direnv"      # loads gitignored .envrc files (e.g. the GitHub Packages PAT)
brew "gh"          # GitHub CLI — auth, repo creation, `gh api`, PR/release workflows
brew "starship"    # shell prompt (wired into ~/.zshrc)
brew "redis"       # local Redis for @wedops/zeus-redis + dependents
brew "libpq"       # Postgres client libs/CLIs (psql, pg_dump) for athena/db work; keg-only
brew "netlify-cli" # deploys the static marketing site
brew "ffmpeg"      # media transcoding — also yt-dlp's mux/encode backend
brew "yt-dlp"      # video/audio downloader
brew "imagemagick" # image processing for brand assets — peer to ffmpeg
brew "jq"          # JSON on the CLI (op / gh api / curl pipelines)
brew "ripgrep"     # fast recursive code search across the monorepos
brew "cloudflared" # tunnel localhost for OAuth redirects + email-webhook testing

# --- GUI apps / casks -----------------------------------------------------

cask "orbstack"      # lightweight Docker engine — provides the `docker` CLI
cask "1password"     # desktop app (bundles the Safari extension); CLI integration unlocks `op`
cask "1password-cli" # `op` — repos' .envrc files read secrets from 1Password, no paste
cask "zed"           # editor
cask "zoom"          # video calls / client meetings
cask "vlc"           # media player
cask "transmission"  # BitTorrent client
cask "tableplus"     # Postgres GUI for the athena/stability DBs (psql has no GUI)
cask "ghostty"       # terminal emulator
cask "linear-linear" # Linear desktop app (INT issues live in the Linear API)
cask "rectangle"     # window tiling / management
