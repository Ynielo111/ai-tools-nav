$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$minReviewTextLength = 2200

function Decode-Text([string]$base64) {
  return [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($base64))
}

$templatePhrases = @(
  "5Lul5LiK5o6o6I2Q55qE5bel5YW35ZCE5pyJ5L6n6YeN",
  "5bu66K6u5qC55o2u6Ieq5bex55qE5YW35L2T6ZyA5rGC5ZKM5L2/55So5Lmg5oOv5p2l6YCJ5oup5pyA5ZCI6YCC55qE5bel5YW3",
  "5LiK6KGo5LuO5aSa5Liq5YWz6ZSu57u05bqm6L+b6KGM5LqG55u06KeC5a+55q+U",
  "6YCJ5a+55bel5YW35Y+q5piv56ys5LiA5q2l",
  "5Lul5LiL5piv5LiA5Lqb57uP6L+H6aqM6K+B55qE5L2/55So5oqA5ben"
) | ForEach-Object { Decode-Text $_ }

$evidencePatterns = @(
  "5a6Y5pa55paH5qGj",
  "5YWs5byA5paH5qGj",
  "5a6e6ZmF5L2/55So",
  "5a6e6ZmF5a6J6KOF5rWL6K+V",
  "6aqM6K+B6YCa6L+H",
  "5p2l5rqQ",
  "6ZmQ5Yi2",
  "5Lu35qC85Y+v6IO9",
  "5a6Y572R",
  "5L+h5oGv"
) | ForEach-Object { [regex]::Escape((Decode-Text $_)) }

function Get-RelativePath([string]$path) {
  return $path.Substring($root.Path.Length + 1).Replace("\", "/")
}

function Get-Text([string]$html) {
  return ($html `
    -replace '<script[\s\S]*?</script>', ' ' `
    -replace '<style[\s\S]*?</style>', ' ' `
    -replace '<[^>]+>', ' ' `
    -replace '&[^;]+;', ' ' `
    -replace '\s+', ' ').Trim()
}

function Get-MetaRobots([string]$html) {
  $match = [regex]::Match($html, '<meta\s+name="robots"\s+content="([^"]+)"', 'IgnoreCase')
  if ($match.Success) { return $match.Groups[1].Value }
  return ""
}

function Count-TemplatePhrases([string]$text) {
  $count = 0
  foreach ($phrase in $templatePhrases) {
    $count += ([regex]::Matches($text, [regex]::Escape($phrase))).Count
  }
  return $count
}

function Has-EvidenceSignal([string]$text) {
  foreach ($pattern in $evidencePatterns) {
    if ($text -match $pattern) {
      return $true
    }
  }
  return $false
}

$reviewPages = Get-ChildItem -Path (Join-Path $root "articles") -File -Filter "*.html" |
  Where-Object { $_.Name -ne "index.html" } |
  ForEach-Object {
    $html = Get-Content -Raw -Encoding UTF8 -LiteralPath $_.FullName
    $robots = Get-MetaRobots $html
    $text = Get-Text $html
    [pscustomobject]@{
      File = Get-RelativePath $_.FullName
      Indexed = ($robots -notmatch "noindex")
      TextLength = $text.Length
      TemplatePhraseHits = Count-TemplatePhrases $text
      HasEvidenceSignal = Has-EvidenceSignal $text
      Robots = $robots
    }
  } |
  Where-Object { $_.Indexed }

$failures = @()

$shortPages = @($reviewPages | Where-Object { $_.TextLength -lt $minReviewTextLength })
if ($shortPages.Count -gt 0) {
  $failures += "Indexed review articles under $minReviewTextLength visible characters: $($shortPages.Count)"
  $shortPages | Select-Object File, TextLength, Robots | Format-Table -AutoSize
}

$templatePages = @($reviewPages | Where-Object { $_.TemplatePhraseHits -gt 0 })
if ($templatePages.Count -gt 0) {
  $failures += "Indexed review articles with repeated template phrases: $($templatePages.Count)"
  $templatePages | Select-Object File, TemplatePhraseHits, TextLength | Format-Table -AutoSize
}

$weakEvidencePages = @($reviewPages | Where-Object { -not $_.HasEvidenceSignal })
if ($weakEvidencePages.Count -gt 0) {
  $failures += "Indexed review articles missing source, evidence, limitation, or update signals: $($weakEvidencePages.Count)"
  $weakEvidencePages | Select-Object File, TextLength | Format-Table -AutoSize
}

Write-Host "Indexed review articles scanned: $($reviewPages.Count)"

if ($failures.Count -gt 0) {
  Write-Host ""
  Write-Host "Low-value content audit failed:"
  $failures | ForEach-Object { Write-Host "- $_" }
  exit 1
}

Write-Host "Low-value content audit passed."
