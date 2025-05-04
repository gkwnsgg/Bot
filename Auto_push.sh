LOGFILE="/home/ubuntu/Bot/gitlog.txt"
cd /home/ubuntu/Bot || exit 1   # 저장소 경로로 이동

# 타임스탬프 표시
echo "========== $(date '+%Y-%m-%d %H:%M:%S') ==========" >> "$LOGFILE"
# Git 사용자 정보 기록
echo "Git user: $(git config user.name) <$(git config user.email)>" >> "$LOGFILE"

# 변경사항이 있으면 커밋 및 푸시
if git diff-index --quiet HEAD --; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] No changes to commit." >> "$LOGFILE"
else
    git add . >> "$LOGFILE" 2>&1
    COMMIT_MSG="Auto commit on $(date '+%Y-%m-%d %H:%M:%S')"
    if git commit -m "$COMMIT_MSG" >> "$LOGFILE" 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Commit succeeded: \"$COMMIT_MSG\"" >> "$LOGFILE"
        if git push origin main >> "$LOGFILE" 2>&1; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push succeeded." >> "$LOGFILE"
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push FAILED." >> "$LOGFILE"
        fi
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Commit FAILED or no changes." >> "$LOGFILE"
    fi
fi
