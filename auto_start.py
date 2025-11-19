from pathlib import Path
import os
import win32com.client


def add_to_startup(exe_path):
    startup = Path(os.getenv("APPDATA")) / \
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    startup.mkdir(parents=True, exist_ok=True)
    shortcut_path = startup / "SystemService.lnk"
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(str(shortcut_path))
    shortcut.TargetPath = exe_path
    shortcut.WorkingDirectory = str(Path(exe_path).parent)
    shortcut.Description = "System Service"
    shortcut.Save()
