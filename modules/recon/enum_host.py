import platform
import wmi
import os

def get_host_info():
    info = dict()
    h_info = platform.uname()
    info['system'] = h_info[0]
    info['hostname'] = h_info[1]
    info['version'] = h_info[3]
    return info

def get_running_processes():
    processes = list()
    win = wmi.WMI()
    wql = 'SELECT * FROM Win32_Service WHERE State = "Running"'
    for proc in win.query(wql):
        processes.append({'name' : proc.name, 'pid' : proc.processid})
    return processes


def list_files():
    return os.listdir()
