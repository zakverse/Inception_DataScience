$pptPath = Resolve-Path 'outputs\final\DSC_GajahHitam_PPT.pptx'
$exportDir = Join-Path (Resolve-Path 'outputs\final') 'slides_preview'
if (-not (Test-Path $exportDir)) {
    New-Item -ItemType Directory -Path $exportDir | Out-Null
}

try {
    $pptApp = New-Object -ComObject PowerPoint.Application
    $pres = $pptApp.Presentations.Open($pptPath.Path, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    $pres.SaveAs($exportDir, 18) # 18 = ppSaveAsPNG
    $pres.Close()
    $pptApp.Quit()
    [System.GC]::Collect()
    Write-Output "SUCCESS: Exported slides to $exportDir"
    Get-ChildItem -Path $exportDir -Filter "*.PNG" | ForEach-Object { Write-Output $_.Name }
} catch {
    Write-Output "COM Error: $_"
}
