$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$siteUrl = "https://www.aitnav.com"
$adNeedle = "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"

function Get-RelativePath([string]$path) {
  return $path.Substring($root.Path.Length + 1).Replace("\", "/")
}

function Get-TextLength([string]$html) {
  $text = $html `
    -replace '<script[\s\S]*?</script>', ' ' `
    -replace '<style[\s\S]*?</style>', ' ' `
    -replace '<[^>]+>', ' ' `
    -replace '&[^;]+;', ' ' `
    -replace '\s+', ' '
  return $text.Trim().Length
}

function Get-MetaRobots([string]$html) {
  $match = [regex]::Match($html, '<meta\s+name="robots"\s+content="([^"]+)"', 'IgnoreCase')
  if ($match.Success) { return $match.Groups[1].Value }
  return ""
}

function Get-Canonical([string]$html) {
  $match = [regex]::Match($html, '<link\s+rel="canonical"\s+href="([^"]+)"', 'IgnoreCase')
  if ($match.Success) { return $match.Groups[1].Value }
  return ""
}

$pages = Get-ChildItem -Path $root -Recurse -File -Filter "*.html" |
  Where-Object {
    $_.FullName -notmatch '\\\.git\\' -and
    $_.FullName -notmatch '\\template\\'
  } |
  ForEach-Object {
    $html = Get-Content -Raw -LiteralPath $_.FullName
    $robots = Get-MetaRobots $html
    $canonical = Get-Canonical $html
    [pscustomobject]@{
      File = Get-RelativePath $_.FullName
      TextLength = Get-TextLength $html
      Indexed = ($robots -notmatch 'noindex')
      Robots = $robots
      HasAdScript = $html.Contains($adNeedle)
      Canonical = $canonical
      HasCanonical = ($canonical.Length -gt 0)
      CanonicalWww = ($canonical -eq "" -or $canonical.StartsWith($siteUrl))
      HasSplash = $html.Contains('id="splash"')
    }
  }

$failures = @()

$indexedMissingAd = @($pages | Where-Object { $_.Indexed -and -not $_.HasAdScript })
if ($indexedMissingAd.Count -gt 0) {
  $failures += "Indexed pages missing AdSense script: $($indexedMissingAd.Count)"
  $indexedMissingAd | Select-Object File, TextLength, Robots | Format-Table -AutoSize
}

$indexedMissingCanonical = @($pages | Where-Object { $_.Indexed -and -not $_.HasCanonical })
if ($indexedMissingCanonical.Count -gt 0) {
  $failures += "Indexed pages missing canonical URL: $($indexedMissingCanonical.Count)"
  $indexedMissingCanonical | Select-Object File, TextLength, Robots | Format-Table -AutoSize
}

$indexedNonWwwCanonical = @($pages | Where-Object { $_.Indexed -and $_.HasCanonical -and -not $_.CanonicalWww })
if ($indexedNonWwwCanonical.Count -gt 0) {
  $failures += "Indexed pages with non-www canonical URL: $($indexedNonWwwCanonical.Count)"
  $indexedNonWwwCanonical | Select-Object File, Canonical | Format-Table -AutoSize
}

$thinIndexed = @($pages | Where-Object { $_.Indexed -and $_.TextLength -lt 800 -and $_.File -notin @("privacy.html", "terms.html") })
if ($thinIndexed.Count -gt 0) {
  $failures += "Indexed pages under 800 visible characters: $($thinIndexed.Count)"
  $thinIndexed | Select-Object File, TextLength, Robots | Format-Table -AutoSize
}

$homePage = $pages | Where-Object { $_.File -eq "index.html" } | Select-Object -First 1
if ($homePage -and $homePage.HasSplash) {
  $failures += "Home page still contains blocking splash markup"
}

$robotsPath = Join-Path $root "robots.txt"
if (Test-Path $robotsPath) {
  $robotsTxt = Get-Content -Raw -LiteralPath $robotsPath
  if (-not $robotsTxt.Contains("$siteUrl/sitemap.xml")) {
    $failures += "robots.txt does not reference $siteUrl/sitemap.xml"
  }
}

$sitemapPath = Join-Path $root "sitemap.xml"
if (Test-Path $sitemapPath) {
  $sitemap = Get-Content -Raw -LiteralPath $sitemapPath
  if ($sitemap.Contains("https://aitnav.com")) {
    $failures += "sitemap.xml still contains non-www URLs"
  }
}

Write-Host "Scanned HTML pages: $($pages.Count)"
Write-Host "Indexed pages: $(@($pages | Where-Object { $_.Indexed }).Count)"
Write-Host "Noindexed pages: $(@($pages | Where-Object { -not $_.Indexed }).Count)"

if ($failures.Count -gt 0) {
  Write-Host ""
  Write-Host "AdSense audit failed:"
  $failures | ForEach-Object { Write-Host "- $_" }
  exit 1
}

Write-Host "AdSense audit passed."
