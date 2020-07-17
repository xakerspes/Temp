Set-ExecutionPolicy Unrestricted
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut("$Env:USERPROFILE\Desktop\Notepad.lnk")
$Shortcut.TargetPath = "$Env:USERPROFILE\Desktop\run.py"
$Shortcut.Save()
 
