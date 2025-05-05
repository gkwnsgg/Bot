#!/bin/bash
cd /home/oihope13/Bot

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$TIMESTAMP] Git 자동 커밋 실행 중..." >> gitlog.txt

git pull origin main --rebase >> gitlog.txt 2>&1
git rebase origin/main >> gitlog.txt 2>&1

if ! git diff --quit; then
    git add subs.json >> gitlog.txt 2>&1
    git commit -m "자동 커밋: $TIMESTAMP" >> gitlog.txt 2>&1
    git push origin main >> gitlog.txt 2>&1
    echo "[$TIMESTAMP] 변경 사항 없음" >> gitlog.txt
else
    echo "[$TIMESTAMP] Git 자동 커밋 완료" >> gitlog.txt
fi
