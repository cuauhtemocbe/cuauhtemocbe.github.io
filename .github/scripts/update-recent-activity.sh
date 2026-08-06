#!/usr/bin/env bash
# Refreshes the "Actividad reciente" block in README.md from public GitHub events.
# Only touches content between the RECENT_ACTIVITY markers.
set -euo pipefail

USERNAME="${GH_USERNAME:?GH_USERNAME is required}"
README="README.md"
START_MARKER="<!--RECENT_ACTIVITY:start-->"
END_MARKER="<!--RECENT_ACTIVITY:end-->"
MAX_ITEMS=5

AUTH_HEADER=()
if [ -n "${GH_TOKEN:-}" ]; then
  AUTH_HEADER=(-H "Authorization: Bearer ${GH_TOKEN}")
fi

api() {
  curl -sf "${AUTH_HEADER[@]}" -H "Accept: application/vnd.github+json" "$1"
}

events_json=$(api "https://api.github.com/users/${USERNAME}/events/public?per_page=30")

# First pass: pick the candidate events (still raw — PR titles are null in
# this feed, GitHub's public Events API truncates them) and cap at MAX_ITEMS
# before doing any extra per-PR API calls.
candidates_json=$(echo "$events_json" | jq -c '
  [.[] |
    (.repo.name) as $full_repo |
    (.repo.name | split("/")[1]) as $repo |
    if .type == "PushEvent" then
      {kind: "push", repo: $repo}
    elif .type == "PullRequestEvent" then
      {kind: "pr", repo: $repo, full_repo: $full_repo, action: .payload.action, number: .payload.number}
    elif .type == "IssuesEvent" then
      {kind: "issue", repo: $repo, action: .payload.action, title: .payload.issue.title, comments: .payload.issue.comments}
    elif .type == "ReleaseEvent" then
      {kind: "release", repo: $repo, tag: .payload.release.tag_name}
    elif .type == "CreateEvent" and .payload.ref_type == "repository" then
      {kind: "new_repo", repo: $repo}
    else empty end
  ][:'"$MAX_ITEMS"']
')

activity_lines=()
while IFS= read -r item; do
  kind=$(echo "$item" | jq -r '.kind')
  repo=$(echo "$item" | jq -r '.repo')
  case "$kind" in
    push)
      activity_lines+=("🔨 Push a **${repo}**")
      ;;
    pr)
      full_repo=$(echo "$item" | jq -r '.full_repo')
      action=$(echo "$item" | jq -r '.action')
      number=$(echo "$item" | jq -r '.number')
      pr_json=$(api "https://api.github.com/repos/${full_repo}/pulls/${number}" || echo '{}')
      title=$(echo "$pr_json" | jq -r '.title // "(sin título disponible)"')
      comments=$(echo "$pr_json" | jq -r '((.comments // 0) + (.review_comments // 0))')
      suffix=""
      [ "$comments" -gt 0 ] 2>/dev/null && suffix=" · ${comments} comentario(s)"
      activity_lines+=("🔀 PR ${action} en **${repo}**: ${title}${suffix}")
      ;;
    issue)
      title=$(echo "$item" | jq -r '.title')
      comments=$(echo "$item" | jq -r '.comments // 0')
      action=$(echo "$item" | jq -r '.action')
      suffix=""
      [ "$comments" -gt 0 ] 2>/dev/null && suffix=" · ${comments} comentario(s)"
      activity_lines+=("📝 Issue ${action} en **${repo}**: ${title}${suffix}")
      ;;
    release)
      tag=$(echo "$item" | jq -r '.tag')
      activity_lines+=("🚀 Release en **${repo}**: ${tag}")
      ;;
    new_repo)
      activity_lines+=("✨ Nuevo repo **${repo}**")
      ;;
  esac
done < <(echo "$candidates_json" | jq -c '.[]')

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
