#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Deploy script for Cloudflare Pages
.DESCRIPTION
    Builds the React frontend and prepares deployment folder with DevoCosm site structure
#>

Write-Host "`n[*] Cloudflare Pages Deployment Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Get script directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

Write-Host "[*] Building frontend..." -ForegroundColor Yellow
Set-Location frontend

# Install dependencies if node_modules doesn't exist
if (!(Test-Path "node_modules")) {
    Write-Host "[*] Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] npm install failed" -ForegroundColor Red
        exit 1
    }
}

# Build the React app
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Build failed" -ForegroundColor Red
    exit 1
}

Set-Location $projectRoot

Write-Host "[+] Build complete!`n" -ForegroundColor Green

# Prepare deployment folder
Write-Host "[*] Preparing deployment folder..." -ForegroundColor Yellow
$deployPath = Join-Path $projectRoot "deploy"

# Remove old deployment folder if exists
if (Test-Path $deployPath) {
    Remove-Item -Recurse -Force $deployPath
}

# Create deployment structure
New-Item -ItemType Directory -Force -Path "$deployPath/chinese-study" | Out-Null

# Copy DevoCosm main site files
Write-Host "[*] Copying DevoCosm site files..." -ForegroundColor Yellow
$devCosmPath = Join-Path $projectRoot "devocosm_html"
if (Test-Path $devCosmPath) {
    Copy-Item "$devCosmPath/*" -Destination $deployPath -Recurse
    Write-Host "[+] DevoCosm files copied" -ForegroundColor Green
} else {
    Write-Host "[!] Warning: devocosm_html folder not found" -ForegroundColor Yellow
    Write-Host "[i] Only Chinese Study app will be in deployment folder" -ForegroundColor Yellow
}

# Copy Chinese Study app build
Write-Host "[*] Copying Chinese Study app..." -ForegroundColor Yellow
$buildPath = Join-Path $projectRoot "frontend/build"
Copy-Item "$buildPath/*" -Destination "$deployPath/chinese-study/" -Recurse
Write-Host "[+] Chinese Study app copied`n" -ForegroundColor Green

# Display deployment info
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[+] Deployment folder ready!" -ForegroundColor Green
Write-Host "`n[i] Location: $deployPath" -ForegroundColor Cyan
Write-Host "`n[i] Folder structure:" -ForegroundColor Cyan
Write-Host "    deploy/" -ForegroundColor White
Write-Host "    ├── index.html              (DevoCosm home)" -ForegroundColor White
Write-Host "    ├── apps.html               (Apps listing)" -ForegroundColor White
Write-Host "    ├── listo.html              (Listo app)" -ForegroundColor White
Write-Host "    ├── privacy_policy.html     (Privacy policy)" -ForegroundColor White
Write-Host "    └── chinese-study/          (Chinese Study app)" -ForegroundColor White
Write-Host "        ├── index.html" -ForegroundColor White
Write-Host "        ├── _redirects" -ForegroundColor White
Write-Host "        └── static/" -ForegroundColor White

Write-Host "`n[i] Next steps:" -ForegroundColor Cyan
Write-Host "    1. Go to Cloudflare Dashboard -> Pages" -ForegroundColor White
Write-Host "    2. Select your devocosm.com project" -ForegroundColor White
Write-Host "    3. Create deployment" -ForegroundColor White
Write-Host "    4. Upload contents of 'deploy' folder" -ForegroundColor White
Write-Host "    5. Verify at: https://devocosm.com/chinese-study/`n" -ForegroundColor White

Write-Host "[+] Done!`n" -ForegroundColor Green

