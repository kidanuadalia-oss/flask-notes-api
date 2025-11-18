#!/bin/bash

echo "🔐 Push with Token"
echo "=================="
echo ""
echo "Enter your GitHub Personal Access Token when prompted."
echo "The token should start with 'github_pat_' or 'ghp_'"
echo ""

cd "$(dirname "$0")"

# Read token securely
read -sp "Enter your GitHub token: " TOKEN
echo ""

if [ -z "$TOKEN" ]; then
    echo "❌ No token provided!"
    exit 1
fi

# Push using token in URL
echo "⬆️  Pushing to GitHub..."
git push https://kidanuadalia-oss:${TOKEN}@github.com/kidanuadalia-oss/flask-notes-api.git main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Your code is now on GitHub!"
    echo "🔗 https://github.com/kidanuadalia-oss/flask-notes-api"
    
    # Reset remote URL to clean version
    git remote set-url origin https://github.com/kidanuadalia-oss/flask-notes-api.git
    echo "✅ Remote URL cleaned (token removed)"
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "   1. Token has 'repo' scope enabled"
    echo "   2. Token is correct (starts with github_pat_ or ghp_)"
    echo "   3. Repository exists on GitHub"
fi

