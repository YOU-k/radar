#!/usr/bin/env bash
# 定时任务统一的提交步骤：只提交内容文件 → 拉取（autostash）→ 在最新代码上重建站点 → 推送，失败重试。
# docs/index.html 是生成物，不和内容一起提交，冲突时在拉取之后重建即可，避免 1.2 MB 文件的 rebase 冲突。
# 用法：scripts/commit_push.sh "<commit message>" <path> [<path> ...]
set -uo pipefail
msg="$1"; shift
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
paths=()
for p in "$@"; do [ -e "$p" ] && paths+=("$p"); done
if [ ${#paths[@]} -gt 0 ]; then git add -A -- "${paths[@]}"; fi
git diff --cached --quiet || git commit -q -m "$msg"
for i in 1 2 3; do
  if git pull -q --rebase --autostash origin main; then
    python -m radar.run site
    git add docs/
    git diff --cached --quiet || git commit -q -m "site: rebuild ($msg)"
    if git push -q; then echo "[commit_push] pushed: $msg"; exit 0; fi
  else
    git rebase --abort 2>/dev/null || true
  fi
  echo "::warning::[commit_push] attempt $i failed, retrying"
  sleep $((i * 20))
done
echo "::error::[commit_push] push failed after 3 attempts: $msg"
exit 1
