#!/bin/bash

# Push script for Flask Notes API
echo "🚀 Pushing Flask Notes API to GitHub..."
echo ""
echo "If prompted for credentials:"
echo "  Username: kidanuadalia-oss"
echo "  Password: Use a GitHub Personal Access Token (not your password)"
echo ""
echo "Get a token at: https://github.com/settings/tokens"
echo ""

cd "$(dirname "$0")"
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "📦 Repository: https://github.com/kidanuadalia-oss/flask-notes-api"
else
    echo ""
    echo "❌ Push failed. Please authenticate and try again."
    echo ""
    echo "Quick setup:"
    echo "1. Create token: https://github.com/settings/tokens"
    echo "2. Run: git push -u origin main"
    echo "3. Username: kidanuadalia-oss"
    echo "4. Password: [paste your token]"
fi

