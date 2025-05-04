#!/bin/bash

git add subs.json

if git diff --cached --quiet; then
    echo "변경 사항 없음. 커밋 건너뜀."
    exit 0
fi

DATE=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "자동 커밋: $DATE"

git push origin main