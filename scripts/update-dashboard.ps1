$ErrorActionPreference = 'Stop'
$username = 'PasupuletiC'
$headers = @{ Accept = 'application/vnd.github+json'; 'User-Agent' = 'profile-dashboard' }
if ($env:GITHUB_TOKEN) { $headers.Authorization = "Bearer $env:GITHUB_TOKEN" }
$profile = Invoke-RestMethod "https://api.github.com/users/$username" -Headers $headers
$repos = @()
$page = 1
do {
    $batch = Invoke-RestMethod "https://api.github.com/users/$username/repos?per_page=100&page=$page" -Headers $headers
    $repos += $batch
    $page++
} while ($batch.Count -eq 100)
$originals = @($repos | Where-Object { -not $_.fork })
$stars = [int](($originals | Measure-Object stargazers_count -Sum).Sum)
$forks = [int](($originals | Measure-Object forks_count -Sum).Sum)
$languages = @($originals | Where-Object language | Group-Object language | Sort-Object Count -Descending | Select-Object -First 5)
$updated = [DateTime]::UtcNow.ToString('yyyy-MM-dd')
$svg = @'
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="330" viewBox="0 0 1000 330" role="img">
<title>Live GitHub dashboard for PasupuletiC</title>
<rect x="1" y="1" width="998" height="328" rx="16" fill="#ffffff" stroke="#dce3ed"/>
<g font-family="Arial, Helvetica, sans-serif">
<circle cx="27" cy="27" r="5" fill="#f87171"/><circle cx="45" cy="27" r="5" fill="#fbbf24"/><circle cx="63" cy="27" r="5" fill="#4ade80"/>
<text x="88" y="33" fill="#475569" font-size="15">github / public metrics</text>
<path d="M1 52H999" stroke="#dce3ed"/>
'@
$labels = @('PUBLIC REPOS', 'STARS EARNED', 'FOLLOWERS', 'FORKS EARNED')
$values = @($profile.public_repos, $stars, $profile.followers, $forks)
for ($i = 0; $i -lt 4; $i++) {
    $x = 34 + $i * 246
    $svg += "<text x='$x' y='118' fill='#0f172a' font-size='42' font-weight='700'>$($values[$i])</text><text x='$x' y='150' fill='#4338ca' font-size='15'>$($labels[$i])</text>"
}
$svg += "<path d='M34 177H966' stroke='#dce3ed'/><text x='34' y='210' fill='#475569' font-size='16'>Primary languages / original public repositories</text>"
$colors = @('#4338ca', '#0f766e', '#be185d', '#9a580b', '#0f766e')
$x = 34
$i = 0
foreach ($language in $languages) {
    $label = [System.Security.SecurityElement]::Escape($language.Name)
    $svg += "<circle cx='$x' cy='246' r='5' fill='$($colors[$i])'/><text x='$($x+13)' y='252' fill='#475569' font-size='16'>$label ($($language.Count))</text>"
    $x += 185
    $i++
}
$svg += "<text x='34' y='301' fill='#526075' font-size='13'>Updated $updated UTC / GitHub API / stars and forks exclude forked repos</text></g></svg>"
$destination = Join-Path $PSScriptRoot '../assets/github-dashboard.svg'
[System.IO.File]::WriteAllText($destination, $svg + "`n", [System.Text.UTF8Encoding]::new($false))
[xml]$validated = $svg
Write-Output "Dashboard refreshed: $($profile.public_repos) public repositories, $stars stars."
