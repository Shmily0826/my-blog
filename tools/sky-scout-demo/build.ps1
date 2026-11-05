param(
  [Parameter(Mandatory=$true)][string]$SourceRepository,
  [Parameter(Mandatory=$true)][string]$FlutterRoot
)
$ErrorActionPreference = 'Stop'
$siteRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$buildRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('sky-scout-portfolio-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $buildRoot | Out-Null
$archive = Join-Path $buildRoot 'source.zip'
git -C $SourceRepository archive --format=zip --output $archive 4fdf1ac943992b8fd5934145b35d734212906123 app_sky_scout
if ($LASTEXITCODE -ne 0) { throw 'Pinned source export failed' }
Expand-Archive -LiteralPath $archive -DestinationPath $buildRoot
$appRoot = Join-Path $buildRoot 'app_sky_scout'
python (Join-Path $PSScriptRoot 'prepare.py') $appRoot $FlutterRoot
if ($LASTEXITCODE -ne 0) { throw 'Demo adaptation failed' }
Push-Location $appRoot
try {
  & (Join-Path $FlutterRoot 'bin/flutter.bat') --suppress-analytics pub get --offline
  if ($LASTEXITCODE -ne 0) { throw 'Offline Flutter dependencies unavailable' }
  & (Join-Path $FlutterRoot 'bin/flutter.bat') --suppress-analytics build web --release --no-pub --no-web-resources-cdn --no-wasm-dry-run --target lib/portfolio_demo.dart --base-href /demos/sky-scout/
  if ($LASTEXITCODE -ne 0) { throw 'Flutter build failed' }
} finally { Pop-Location }
python (Join-Path $PSScriptRoot 'package.py') (Join-Path $appRoot 'build/web') (Join-Path $siteRoot 'public/demos/sky-scout') $FlutterRoot
if ($LASTEXITCODE -ne 0) { throw 'Demo packaging failed' }
Write-Output ('Build retained for inspection: ' + $buildRoot)
