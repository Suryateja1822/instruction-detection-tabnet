# TabNet-IDS Deployment Script
# Quick push to GitHub

Write-Host "🚀 TabNet-IDS GitHub Deployment" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized!" -ForegroundColor Green
    Write-Host ""
}

# Get GitHub username
Write-Host "👤 Enter your GitHub username:" -ForegroundColor Yellow
$username = Read-Host

# Check if remote exists
$remoteExists = git remote | Select-String "origin"
if (-not $remoteExists) {
    Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
    git remote add origin "https://github.com/$username/tabnet-ids-executive.git"
    Write-Host "✅ Remote added!" -ForegroundColor Green
    Write-Host ""
}

# Add all files
Write-Host "📁 Adding files..." -ForegroundColor Yellow
git add .
Write-Host "✅ Files added!" -ForegroundColor Green
Write-Host ""

# Commit
Write-Host "💾 Enter commit message (or press Enter for default):" -ForegroundColor Yellow
$commitMsg = Read-Host
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "feat: TabNet-IDS Executive Dashboard with AI threat detection"
}

git commit -m $commitMsg
Write-Host "✅ Changes committed!" -ForegroundColor Green
Write-Host ""

# Push
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! Code pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://streamlit.io/cloud" -ForegroundColor White
    Write-Host "2. Sign in with GitHub" -ForegroundColor White
    Write-Host "3. Click 'New app'" -ForegroundColor White
    Write-Host "4. Select repository: $username/tabnet-ids-executive" -ForegroundColor White
    Write-Host "5. Main file: app_with_upload.py" -ForegroundColor White
    Write-Host "6. Click 'Deploy!'" -ForegroundColor White
    Write-Host ""
    Write-Host "🌐 Your app will be live at:" -ForegroundColor Cyan
    Write-Host "https://$username-tabnet-ids-executive.streamlit.app" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Push failed! Please check the error above." -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Common fixes:" -ForegroundColor Yellow
    Write-Host "1. Create the repository on GitHub first: https://github.com/new" -ForegroundColor White
    Write-Host "2. Name it: tabnet-ids-executive" -ForegroundColor White
    Write-Host "3. Run this script again" -ForegroundColor White
    Write-Host ""
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
