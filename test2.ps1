$json = '{ "themes": ["default", "PizzaTheme"] }'
$obj = $json | ConvertFrom-Json
$contains = $obj.themes.Contains("PizzaTheme")
Write-Host "Contains result: $contains"

try {
    $obj.themes += "NewTheme"
    Write-Host "Addition worked. Themes:"
    $obj.themes
} catch {
    Write-Host "Addition failed: $_"
}

$scriptPath = (Get-Location).Path
Write-Host "Current location: $scriptPath"
