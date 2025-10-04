#!/bin/bash
set -e

CHANGELOG_FILE="CHANGELOG.md"

if [ ! -f "$CHANGELOG_FILE" ]; then
    echo ""
    exit 0
fi

CHANGELOG=$(awk '
    BEGIN { found = 0; content = "" }
    /^## \[[0-9]+\.[0-9]+\.[0-9]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}/ {
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
        gsub(/\n$/, "", content)
        print content
    }
' "$CHANGELOG_FILE")

echo "$CHANGELOG"