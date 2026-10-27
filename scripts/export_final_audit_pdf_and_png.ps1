# PowerPoint COM Automation: Export Audited PPTX to PDF and Slide PNGs
$pptxPath = "Z:\Projects\Inception\outputs\final\INCEPTION_2026_GajahHitam_PPT_Final_Audit.pptx"
$pdfPath  = "Z:\Projects\Inception\outputs\final\INCEPTION_2026_GajahHitam_PPT_Final_Audit.pdf"
$pngDir   = "Z:\Projects\Inception\outputs\final\slides_preview_final_audit"

if (!(Test-Path $pngDir)) {
    New-Item -ItemType Directory -Path $pngDir -Force | Out-Null
}

Write-Host "Opening PowerPoint Application..."
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue

Write-Host "Opening Presentation: $pptxPath"
$pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)

Write-Host "Exporting to PDF: $pdfPath"
# 32 = ppSaveAsPDF
$pres.SaveAs($pdfPath, 32)
Write-Host "PDF exported successfully. Size: $((Get-Item $pdfPath).Length) bytes"

Write-Host "Exporting slides to PNG: $pngDir"
$pres.Export($pngDir, "PNG", 1920, 1080)
Write-Host "Slide PNGs exported successfully."

$pres.Close()
$ppt.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($pres) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()
Write-Host "PowerPoint closed cleanly."
