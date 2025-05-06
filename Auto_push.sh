#!/bin/bash
cd /home/oihope13/Bot || exit 1

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$TIMESTAMP] Git 자동 커밋 실행 중..." >> gitlog.txt

echo "[$TIMESTAMP] git pull origin main --rebase 실행" >> gitlog.txt
git pull origin main --rebase >> gitlog.txt 2>&1

if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "[$TIMESTAMP] git add 및 임시 커밋 실행" >> "$LOG_FILE"
    git add -A >> "$LOG_FILE" 2>&1
    git commit -m "임시 커밋: $TIMESTAMP" >> "$LOG_FILE" 2>&1
fi

echo "[$TIMESTAMP] git pull origin main --rebase 실행" >> "$LOG_FILE"
git pull origin main --rebase >> "$LOG_FILE" 2>&1

if ! git diff --quiet; then
    echo "[$TIMESTAMP] 변경 사항 감지됨" >> "$LOG_FILE"
    git add -A >> "$LOG_FILE" 2>&1
    git commit -m "자동 커밋: $TIMESTAMP" >> "$LOG_FILE" 2>&1
    git push origin main >> "$LOG_FILE" 2>&1
    echo "[$TIMESTAMP] 변경 사항 푸시 완료" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] 변경 사항 없음" >> "$LOG_FILE"
fi
