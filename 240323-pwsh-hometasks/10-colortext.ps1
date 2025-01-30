# To give permission to run PowerShell script on Windows 10 without admin rights, only for the current session:
# c:\> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

Write-Host "Blue text from file script" -ForegroundColor Blue

$colors = @("green", "blue", "red", "yellow")
for ($i=0; $i -lt $colors.Length; $i++) {
    Write-Host $colors[$i] -ForegroundColor $colors[$i]
}
