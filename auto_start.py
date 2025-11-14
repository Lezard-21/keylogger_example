# import os
# from pathlib import Path
# import ctypes
# from ctypes import wintypes
# import sys
#
#
# class ShellLink:
#     def __init__(self):
#         self._setup_types()
#
#     def _setup_types(self):
#         # Define required Windows API types
#         self.LPWSTR = ctypes.POINTER(wintypes.WCHAR)
#         self.LPDWORD = ctypes.POINTER(ctypes.c_ulong)
#
#         # Load shell32.dll
#         self.shell32 = ctypes.WinDLL('shell32', use_last_error=True)
#
#         # Define interface signatures
#         self.shell32.CoInitialize.argtypes = [ctypes.c_void_p]
#         self.shell32.CoCreateInstance.argtypes = [
#             ctypes.c_void_p,
#             ctypes.c_void_p,
#             ctypes.c_void_p,
#             ctypes.c_void_p
#         ]
#
#         # CLSID_ShellLink
#         self.CLSID_ShellLink = ctypes.c_char_p(
#             b'{000214EE-0000-0000-C000-000000000046}')
#
#         # IID_IShellLink
#         self.IID_IShellLink = ctypes.c_char_p(
#             b'{000214EE-0000-0000-C000-000000000046}')
#
#     def create_shortcut(self, link_path, target_path, description=""):
#         """
#         Creates a shortcut (.lnk file) pointing to the target path.
#
#         Args:
#             link_path (str): Path where the shortcut will be created
#             target_path (str): Path to the executable/file being linked
#             description (str): Optional description for the shortcut
#
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         # Initialize COM
#         try:
#             self.shell32.CoInitialize(None)
#
#             # Create IShellLink object
#             ptr = ctypes.c_void_p()
#             self.shell32.CoCreateInstance(
#                 self.CLSID_ShellLink,
#                 None,
#                 4,  # CLSCTX_INPROC_SERVER
#                 self.IID_IShellLink,
#                 ctypes.byref(ptr)
#             )
#
#             # Get IShellLink interface
#             self.IShellLink = ctypes.cast(ptr.value, ctypes.c_void_p)
#
#             # Set target path
#             self.shell32.IPersistFile_SetSaveFile(
#                 self.IShellLink, link_path, 0)
#
#             # Set description
#             if description:
#                 self.shell32.IPersistFile_SetDescriptionW(
#                     self.IShellLink, description)
#
#             # Save the shortcut
#             self.shell32.IPersistFile_Save(self.IShellLink, None, False)
#
#             return True
#
#         except Exception as e:
#             print(f"Error creating shortcut: {str(e)}")
#             return False
#
#         finally:
#             # Clean up
#             if hasattr(self, 'IShellLink'):
#                 self.shell32.Release(self.IShellLink)
#             self.shell32.CoUninitialize()
#
#
# def add_to_startup_folder(executable_path):
#     """
#     Adds an executable to Windows startup folder by creating a shortcut.
#
#     Args:
#         executable_path (str): Path to the executable to add to startup
#
#     Returns:
#         str: Path to the created shortcut, or None if creation failed
#     """
#     # Get the startup folder path
#     startup_folder = str(
#         Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")
#
#     # Create a descriptive filename for the shortcut
#     shortcut_name = f"SystemService.lnk"
#     shortcut_path = os.path.join(startup_folder, shortcut_name)
#
#     # Verify paths exist
#     if not os.path.exists(executable_path):
#         print(f"Error: Executable not found at {executable_path}")
#         return None
#
#     if not os.path.exists(startup_folder):
#         print(f"Error: Startup folder not found at {startup_folder}")
#         return None
#
#     # Create the shortcut
#     shell_link = ShellLink()
#     success = shell_link.create_shortcut(
#         link_path=shortcut_path,
#         target_path=executable_path,
#         description="System Service"
#     )
#
#     if success:
#         print(f"Successfully created shortcut at: {shortcut_path}")
#         return shortcut_path
#     else:
#         print("Failed to create shortcut")
#         return None
#
#
# def main():
#     """Example usage"""
#     if len(sys.argv) != 2:
#         print("Usage: python script.py <path_to_executable>")
#         sys.exit(1)
#
#     executable_path = sys.argv[1]
#     result = add_to_startup_folder(executable_path)
#     if result:
#         print(f"Executable will now run at system startup: {result}")
#
#
# if __name__ == "__main__":
#     main()
import os
from pathlib import Path
import win32com.client


def add_to_startup(exe_path):
    # Startup folder
    startup = Path(os.getenv("APPDATA")) / \
        r"Microsoft\Windows\Start Menu\Programs\Startup"

    if not Path(exe_path).exists():
        print("No existe el ejecutable.")
        return

    shortcut_path = startup / "SystemService.lnk"

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(str(shortcut_path))
    shortcut.TargetPath = str(exe_path)
    shortcut.WorkingDirectory = str(Path(exe_path).parent)
    shortcut.Description = "System Service"
    shortcut.Save()

    print(f"Shortcut creado correctamente en:\n{shortcut_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python script.py <ruta_del_exe>")
        sys.exit(1)

    add_to_startup(sys.argv[1])
