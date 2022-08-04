pipreqs "./app" --savepath "./requirements.prod.txt"
Write-Host "Merging files..."
Get-Content requirements.prod.txt, requirements.ocluded.txt | Set-Content requirements.txt
Write-Host "Requirements file generated"
