#!/usr/bin/env bash
# Deploy the presentation to Vercel (webdev-8785s-projects/ishwara).
#
# Deploys from a clean temp dir containing ONLY the two public pages, so the
# private chats/ and transcripts/ can never be bundled into the upload or the
# CDN — regardless of .vercelignore quirks. The site needs nothing but these:
#   index.html      — the one-idea presentation (home)
#   companion.html  — the full study companion (219 teachings, EN/RU)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DIST="$(mktemp -d)/ishwara-dist"
mkdir -p "$DIST"
cp "$ROOT/index.html"     "$DIST/index.html"
cp "$ROOT/companion.html" "$DIST/companion.html"

echo "Deploying $(du -sh "$DIST" | cut -f1) from $DIST"
cd "$DIST"
npx --yes vercel@latest link --yes --scope webdev-8785s-projects --project ishwara
npx --yes vercel@latest deploy --prod --yes
