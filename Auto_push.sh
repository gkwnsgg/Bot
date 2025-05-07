#!/bin/bash
cd /home/oihope13/Bot || exit 1

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$TIMESTAMP] Git 자동 커밋 실행 중..." >> gitlog.txt

echo "[$TIMESTAMP] git pull origin main --rebase 실행" >> gitlog.txt
git pull origin main --rebase >> gitlog.txt 2>&1

if ! git diff --quiet; then
    echo "[$TIMESTAMP] 변경 사항 감지됨" >> gitlog.txt
    echo "[$TIMESTAMP] 변경된 내용: " >> gitlog.txt
    git diff >> gitlog.txt

    git add subs.json >> gitlog.txt 2>&1
    git commit -m "자동 커밋: $TIMESTAMP" >> gitlog.txt 2>&1
    git push origin main >> gitlog.txt 2>&1
    echo "[$TIMESTAMP] 변경 사항 푸시 완료" >> gitlog.txt
else
    echo "[$TIMESTAMP] 변경 사항 없음" >> gitlog.txt
fi