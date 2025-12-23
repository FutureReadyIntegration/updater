#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------
# 🔱 The Veil — Docker Release Pipeline
# ---------------------------------------------
# Usage:
#   ./release.sh 1.0.6
#
# This will:
#   - Build updater:latest
#   - Tag updater:<version>
#   - Push both tags to Docker Hub
# ---------------------------------------------

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

VERSION="$1"
IMAGE="notchofhwend/updater"

echo "🔧 Building updater:latest ..."
docker build -t updater:latest .

echo "🏷  Tagging updater:latest as $IMAGE:$VERSION ..."
docker tag updater:latest "$IMAGE:$VERSION"

echo "📤 Pushing $IMAGE:$VERSION ..."
docker push "$IMAGE:$VERSION"

echo "📤 Pushing updater:latest ..."
docker tag updater:latest "$IMAGE:latest"
docker push "$IMAGE:latest"

echo "✅ Release complete for version $VERSION"

