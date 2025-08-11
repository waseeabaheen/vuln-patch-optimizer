param(
    [switch]$DryRun = $true,
    [string]$TargetsPath = "data\sample_targets_windows.json"
)

# Requires: PSWindowsUpdate module and admin privileges
# Install-Module -Name PSWindowsUpdate

$targets = Get-Content -Raw -Path $TargetsPath | ConvertFrom-Json

foreach ($t in $targets) {
    if ($DryRun) {
        Write-Host "[DRY-RUN] Would patch Windows host:" $t.hostname
    } else {
        Write-Host "Patching Windows host:" $t.hostname
        # Example (local): Get-WindowsUpdate -AcceptAll -Install -AutoReboot
        # Example (remote): Invoke-WUJob -ComputerName $t.hostname -AcceptAll -Install -AutoReboot
    }
}
