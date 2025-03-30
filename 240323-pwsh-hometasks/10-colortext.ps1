<# To give permission to run PowerShell script on Windows 10 without admin rights, only for the current session:
 # c:\> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

 # OR
 # c:\> powershell -ExecutionPolicy Bypass -File .\10-colortext.ps1
Write-Host "Blue text from file script" -ForegroundColor Blue

$colors = @("green", "blue", "red", "yellow")
for ($i=0; $i -lt $colors.Length; $i++) {
    Write-Host $colors[$i] -ForegroundColor $colors[$i]
}
