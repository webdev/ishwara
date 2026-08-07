#!/usr/bin/env bash
# Deploy the presentation to Vercel (webdev-8785s-projects/ishwara).
#
# Deploys from a clean temp dir containing ONLY index.html, so the private
# chats/ and transcripts/ can never be bundled into the upload or the CDN —
# regardless of .vercelignore quirks. The site needs nothing but index.html.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/index.html"
DIST="$(mktemp -d)/ishwara-dist"
mkdir -p "$DIST"
cp "$SRC" "$DIST/index.html"

echo "Deploying $(du -h "$DIST/index.html" | cut -f1) from $DIST"
cd "$DIST"
npx --yes vercel@latest link --yes --scope webdev-8785s-projects --project ishwara
npx --yes vercel@latest deploy --prod --yes
