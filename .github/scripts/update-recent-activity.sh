#!/usr/bin/env bash
# Refreshes the "Actividad reciente" block in README.md from public GitHub events.
# Only touches content between the RECENT_ACTIVITY markers.
set -euo pipefail

USERNAME="${GH_USERNAME:?GH_USERNAME is required}"
README="README.md"
START_MARKER="<!--RECENT_ACTIVITY:start-->"
END_MARKER="<!--RECENT_ACTIVITY:end-->"
MAX_ITEMS=5

events_json=$(curl -sf -H "Accept: application/vnd.github+json" \
  "https://api.github.com/users/${USERNAME}/events/public?per_page=30")

mapfile -t activity_lines < <(echo "$events_json" | jq -r '
  .[] |
  (.repo.name | split("/")[1]) as $repo |
  if .type == "PushEvent" then
    "🔨 Push a **\($repo)**"
  elif .type == "PullRequestEvent" then
    "🔀 PR \(.payload.action) en **\($repo)**: \(.payload.pull_request.title)"
  elif .type == "IssuesEvent" then
    "📝 Issue \(.payload.action) en **\($repo)**: \(.payload.issue.title)"
  elif .type == "ReleaseEvent" then
    "🚀 Release en **\($repo)**: \(.payload.release.tag_name)"
  elif .type == "CreateEvent" and .payload.ref_type == "repository" then
    "✨ Nuevo repo **\($repo)**"
  else empty end
' | head -n "$MAX_ITEMS")

{
  echo "$START_MARKER"
  if [ "${#activity_lines[@]}" -eq 0 ]; then
    echo "_Sin actividad pública reciente._"
  else
    for line in "${activity_lines[@]}"; do
      echo "- $line"
    done
  fi
  echo "$END_MARKER"
} > /tmp/activity_block.md

awk -v start="$START_MARKER" -v end="$END_MARKER" -v blockfile=/tmp/activity_block.md '
  BEGIN { while ((getline line < blockfile) > 0) block = block line "\n" }
  $0 == start { printf "%s", block; skipping = 1; next }
  $0 == end { skipping = 0; next }
  !skipping { print }
' "$README" > /tmp/readme_new.md && mv /tmp/readme_new.md "$README"
