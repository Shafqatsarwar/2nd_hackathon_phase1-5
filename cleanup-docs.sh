#!/bin/bash

# Cleanup Script - Auto-Clean Temporary Files
# Purpose: Remove temporary recovery/test files to clean up the project root.
# Protected Files: README.md, guide.md, instructions.md

echo "🧹 Starting cleanup... Removing temporary files..."
echo ""

# Defined list of files to DELETE
TEMP_FILES=(
    "DOCKER_DEPLOYMENT.md"
    "ALL_FIXED.md"
    "API_KEYS_REMOVED.md"
    "API_KEY_FIX.md"
    "API_KEY_FIXED.md"
    "CHATBOT_FIXED.md"
    "CHATBOT_FULLY_FIXED.md"
    "CLEANUP_PLAN.md"
    "DEMO_MODE_ENABLED.md"
    "FINAL_FIX.md"
    "OPENAI_FIX.md"
    "PROJECT_FINALIZED.md"
    "QUICK_START.md"
    "READY_FOR_GIT.md"
    "RECOVERY_REPORT.md"
    "SUCCESS.md"
    "TASK_CREATION_FIXED.md"
    "update_and_deploy.sh"
)

# Counter
count=0

# Delete loop
for file in "${TEMP_FILES[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "🗑️  Deleted: $file"
        ((count++))
    fi
done

echo ""
echo "✨ Cleanup complete! Removed $count temporary files."
echo ""
echo "📂 Your project root is now clean."
echo "✅ Essential docs kept: README.md, guide.md, instructions.md"
