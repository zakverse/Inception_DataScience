$ppt = New-Object -ComObject PowerPoint.Application
Write-Host "PowerPoint COM created successfully. Version: $($ppt.Version)"
$ppt.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()
Write-Host "PowerPoint closed cleanly."
