# psutil: Cross-platform lib for process and system monitoring in Python.
# winreg: Windows registry access module. (Windows Registry API)
# pywintypes: Python for Windows extensions.


import psutil
import winreg
import win32api
from win32event import WAIT_OBJECT_0, WAIT_TIMEOUT, WaitForMultipleObjects
from win32api import CloseHandle
from ctypes.wintypes import HANDLE
from browser_monitor_interface import ProcessMonitorInterface


class BrowserProcessMonitor(ProcessMonitorInterface):
    def __init__(self):
        self.default_browser_process = []
        self.default_browser_handles = []

    def get_default_browser_processes(self):
        # Retrieve the default browser path
        default_browser_path = self.get_default_browser_path()
        # Get the process id of the default browser executable
        default_browser_pid = self.get_default_browser_pid(default_browser_path)

        if default_browser_pid:
            self.default_browser_process.append(default_browser_pid)

    def get_process_id(self, process_name):
        for proc in psutil.process_iter(['name'], ['pid']):
            if proc.info['name'] == process_name:
                return proc.info['pid']
        return None

    def pid_is_running(self, pid):
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            if proc.info['pid'] == pid:
                print(f"Process {pid} - Name: {proc.info['name']} - Status: {proc.info['status']}")
                return True
        return False

    def get_process_handle(self, process_id):
        return win32api.OpenProcess(0x1000, False, process_id)

    def initialize_driver(self):
        handles_to_wait = [HANDLE(handle) for handle in self.default_browser_handles]
        while True:
            result = WaitForMultipleObjects(handles_to_wait, False, 1000)
            if result == WAIT_TIMEOUT:
                pass
            elif WAIT_OBJECT_0 <= result < WAIT_OBJECT_0 + len(handles_to_wait):
                pass
            break

    def wait_for_all_handles(self):
        handles_to_wait = [HANDLE(handle) for handle in self.default_browser_handles]

        while True:
            result = WaitForMultipleObjects(handles_to_wait, False, 1000)
            if result == WAIT_TIMEOUT:
                pass
            elif WAIT_OBJECT_0 <= result < WAIT_OBJECT_0 + len(handles_to_wait):
                pass
            break

    def get_default_browser_name(self):
        # Open the Windows Registry key for the default browser
        key_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            # Retrieve the ProgId associated with the default browser
            prog_id, _ = winreg.QueryValueEx(key, 'ProgId')

        # Determine the default browser based on the ProgId
        if prog_id == 'ChromeHTML':
            default_browser_name = 'Google Chrome'
        elif prog_id == 'FireFoxHTML':
            default_browser_name = 'Mozilla Firefox'
        elif prog_id == 'IE.HTTP':
            default_browser_name = 'Internet Explorer'
        else:
            default_browser_name = 'Unknown'

        return default_browser_name

    def get_default_browser_path(self):
        # Open the Windows Registry key for the default browser
        key_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            # Retrieve the ProgId associated with the default browser
            prog_id, _ = winreg.QueryValueEx(key, 'ProgId')

        # Determine the default browser path based on the ProgId
        if prog_id == 'ChromeHTML':
            default_browser_path = 'C:\\Program Files\\Google\\Chrome\\chrome.exe'
            # TODO: Needs Fixing FireFox
        elif prog_id == 'FireFoxHTML':
            default_browser_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
            # TODO: Needs Fixing Edge
        elif prog_id == 'IE.HTTP':
            default_browser_path = 'C:\\Program Files\\Internet Explorer\\iexplore.exe'
        else:
            default_browser_path = None

        return default_browser_path

    def get_default_browser_pid(self, browser_path):
        # Use psutil to find the process ID of the default browser executable
        for proc in psutil.process_iter(['name', 'exe'], ['pid']):
            if proc.info['exe'] == browser_path:
                return proc.info['pid']
        return None
