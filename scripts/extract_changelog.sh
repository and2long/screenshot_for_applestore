#!/bin/bash
# 设置错误时退出
set -e

CHANGELOG_FILE="CHANGELOG.md"

# 检查文件是否存在
if [ ! -f "$CHANGELOG_FILE" ]; then
    echo ""
    exit 0
fi

# 提取最新版本的内容
CHANGELOG=$(awk '
    BEGIN { found = 0; content = "" }
    /^## \[[0-9]+\.[0-9]+\.[0-9]+\+[0-9]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}/ {
        if (found) exit
        found = 1
        next
    }
    found {
        if (/^## \[/) exit
        content = content $0 "\n"
    }
    END {
        if (!found) {
            print ""
            exit 0
        }
        # 移除末尾的换行符
        gsub(/\n$/, "", content)
        print content
    }
' "$CHANGELOG_FILE")

echo "$CHANGELOG"