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
      {kind: "push", repo: $repo, full_repo: $full_repo, created_at: .created_at}
    elif .type == "PullRequestEvent" then
      {kind: "pr", repo: $repo, full_repo: $full_repo, action: .payload.action, number: .payload.number, created_at: .created_at}
    elif .type == "IssuesEvent" then
      {kind: "issue", repo: $repo, full_repo: $full_repo, action: .payload.action, title: .payload.issue.title, url: .payload.issue.html_url, comments: .payload.issue.comments, created_at: .created_at}
    elif .type == "ReleaseEvent" then
      {kind: "release", repo: $repo, full_repo: $full_repo, tag: .payload.release.tag_name, url: .payload.release.html_url, created_at: .created_at}
    elif .type == "CreateEvent" and .payload.ref_type == "repository" then
      {kind: "new_repo", repo: $repo, full_repo: $full_repo, created_at: .created_at}
    else empty end
  ][:30]
')

action_label() {
  case "$1" in
    opened) printf "abrió" ;;
    closed) printf "cerró" ;;
    merged) printf "integró" ;;
    labeled) printf "etiquetó" ;;
    unlabeled) printf "quitó una etiqueta de" ;;
    *) printf "%s" "$1" ;;
  esac
}

format_date() {
  date -u -d "$1" +%Y-%m-%d
}

activity_lines=()
declare -A seen
emitted=0
while IFS= read -r item; do
  [ "$emitted" -ge "$MAX_ITEMS" ] && break
  kind=$(echo "$item" | jq -r '.kind')
  repo=$(echo "$item" | jq -r '.repo')
  full_repo=$(echo "$item" | jq -r '.full_repo // empty')
  created_at=$(echo "$item" | jq -r '.created_at // empty')
  date_label=$(format_date "$created_at")
  repo_link="[${repo}](https://github.com/${full_repo})"
  case "$kind" in
    push)
      key="push|${repo}"
      [ -n "${seen[$key]:-}" ] && continue
      seen[$key]=1
      activity_lines+=("**Push** · ${repo_link} · ${date_label}")
      ;;
    pr)
      action=$(echo "$item" | jq -r '.action')
      number=$(echo "$item" | jq -r '.number')
      pr_json=$(api "https://api.github.com/repos/${full_repo}/pulls/${number}" || echo '{}')
      title=$(echo "$pr_json" | jq -r '.title // "(sin título disponible)"')
      url=$(echo "$pr_json" | jq -r '.html_url // empty')
      comments=$(echo "$pr_json" | jq -r '((.comments // 0) + (.review_comments // 0))')
      key="pr|${full_repo}|${title}|${action}"
      [ -n "${seen[$key]:-}" ] && continue
      seen[$key]=1
      suffix=""
      if [ "$comments" -gt 0 ] 2>/dev/null; then
        [ "$comments" -eq 1 ] && suffix=" · 1 comentario" || suffix=" · ${comments} comentarios"
      fi
      [ -n "$url" ] && title_link="[${title}](${url})" || title_link="$title"
      activity_lines+=("**PR $(action_label "$action")** · ${repo_link} — ${title_link}${suffix} · ${date_label}")
      ;;
    issue)
      title=$(echo "$item" | jq -r '.title')
      comments=$(echo "$item" | jq -r '.comments // 0')
      action=$(echo "$item" | jq -r '.action')
      url=$(echo "$item" | jq -r '.url // empty')
      key="issue|${full_repo}|${title}|${action}"
      [ -n "${seen[$key]:-}" ] && continue
      seen[$key]=1
      suffix=""
      if [ "$comments" -gt 0 ] 2>/dev/null; then
        [ "$comments" -eq 1 ] && suffix=" · 1 comentario" || suffix=" · ${comments} comentarios"
      fi
      [ -n "$url" ] && title_link="[${title}](${url})" || title_link="$title"
      activity_lines+=("**Issue $(action_label "$action")** · ${repo_link} — ${title_link}${suffix} · ${date_label}")
      ;;
    release)
      tag=$(echo "$item" | jq -r '.tag')
      url=$(echo "$item" | jq -r '.url // empty')
      key="release|${full_repo}|${tag}"
      [ -n "${seen[$key]:-}" ] && continue
      seen[$key]=1
      [ -n "$url" ] && title_link="[${tag}](${url})" || title_link="$tag"
      activity_lines+=("**Release** · ${repo_link} — ${title_link} · ${date_label}")
      ;;
    new_repo)
      key="new_repo|${full_repo}"
      [ -n "${seen[$key]:-}" ] && continue
      seen[$key]=1
      activity_lines+=("**Nuevo repositorio** · ${repo_link} · ${date_label}")
      ;;
  esac
  emitted=$((emitted + 1))
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
