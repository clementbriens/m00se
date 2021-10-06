import os
import sys

def add_registry_key():
    exe = sys.executable
    os.system('REG ADD HKEY_CURRENT_USER\SOFTWARE\Microsoft\CurrentVersion\Run /v 1 /d "{}" /f'.format(exe))
