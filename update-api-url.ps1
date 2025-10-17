# PowerShell script to update API URLs for deployment
param(
    [Parameter(Mandatory=$true)]
    [string]$RailwayUrl
)

Write-Host "Updating API URLs to: $RailwayUrl" -ForegroundColor Green

# Update api.ts
$apiFile = "frontend/src/services/api.ts"
$apiContent = Get-Content $apiFile -Raw
$apiContent = $apiContent -replace "https://your-backend-app\.railway\.app", $RailwayUrl
Set-Content $apiFile $apiContent

# Update AnalysisPane.tsx
$analysisFile = "frontend/src/components/AnalysisPane.tsx"
$analysisContent = Get-Content $analysisFile -Raw
$analysisContent = $analysisContent -replace "https://your-backend-app\.railway\.app", $RailwayUrl
Set-Content $analysisFile $analysisContent

Write-Host "✅ Updated API URLs in:" -ForegroundColor Green
Write-Host "  - $apiFile" -ForegroundColor Yellow
Write-Host "  - $analysisFile" -ForegroundColor Yellow

Write-Host "`n🔄 Now rebuilding frontend..." -ForegroundColor Blue
Set-Location frontend
npm run build

Write-Host "`n✅ Frontend built successfully!" -ForegroundColor Green
Write-Host "📁 Build files are in: frontend/build/" -ForegroundColor Yellow

