#!/bin/bash

echo "🚀 Final Push to GitHub"
echo "======================"
echo ""
echo "This will push your Flask Notes API to GitHub."
echo "When prompted:"
echo "  Username: kidanuadalia-oss"
echo "  Password: [paste your GitHub Personal Access Token]"
echo ""
echo "Make sure your token has 'repo' permissions!"
echo ""

cd "$(dirname "$0")"

# Show current status
echo "📋 Current status:"
git status --short
echo ""

# Push
echo "⬆️  Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Your code is now on GitHub!"
    echo "🔗 https://github.com/kidanuadalia-oss/flask-notes-api"
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "   1. Token doesn't have 'repo' scope - regenerate it"
    echo "   2. Token expired - create a new one"
    echo "   3. Repository doesn't exist - create it on GitHub first"
    echo ""
    echo "Get a new token: https://github.com/settings/tokens"
fi

