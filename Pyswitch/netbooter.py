#!/usr/bin/python3

import telnetlib
import time
import sys
import os
import re


SLEEP_TIME = 1

TIMEOUT = 3.0


class Interface:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def port_reboot(self, port_num):
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=TIMEOUT)

        s = tn.read_some()
        time.sleep(SLEEP_TIME)

        s = ("rb " + str(port_num)).encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(SLEEP_TIME)
        tn.close()


    def port_on(self, port_num):
        # print("On:", port_num)
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=TIMEOUT)

        s = tn.read_some()
        time.sleep(SLEEP_TIME)

        s = ("pset " + str(port_num) + " 1").encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(SLEEP_TIME)
        tn.close()


    def port_off(self, port_num):
        # print("Off:", port_num)
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=TIMEOUT)

        s = tn.read_some()
        # print(s)
        time.sleep(SLEEP_TIME)

        s = ("pset " + str(port_num) + " 0").encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(SLEEP_TIME)
        tn.close()


    def get_status(self):
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=TIMEOUT)

        s = tn.read_some()
        time.sleep(SLEEP_TIME)

        s = "pshow".encode("ascii") + b"\r\n"
        tn.write(s)
        time.sleep(SLEEP_TIME)

        s = ""
        while True:
            text = tn.read_eager()
            s += text.decode()
            if len(text) == 0:
                break

        tn.close()

        return s


    def is_port_on(self, port_num):
        text = self.get_status()
        lines = text.splitlines()

        for l in lines:
            m = re.match(r"\d+\|\s+Outlet" + str(port_num) + r"\|\s+(\w+)\s*\|", l.strip())
            if m:
                return m.group(1) == "ON"
        return None


    def print_usage():
        print("Incorrect usage!")
        print(os.path.splitext(__file__)[0], "<on|off|reboot|status> <port_num>")    


def main():
    ip_address = "192.168.1.100"
    port = 23
    netbooter = Interface(ip_address, port)
    # Get command
    if len(sys.argv) < 2:
        netbooter.print_usage()
        return

    cmd = sys.argv[1].lower()
    if cmd == "status":
        print(netbooter.get_status())
        return

    if len(sys.argv) != 3:
        netbooter.print_usage()
        return

    if cmd not in ("on", "off", "reboot"):
        netbooter.print_usage()
        return

    port_num = sys.argv[2]

    if cmd == "on":
        netbooter.port_on(port_num)
    elif cmd == "off":
        netbooter.port_off(port_num)
    elif cmd == "reboot":
        netbooter.port_reboot(port_num)


if __name__ == "__main__":
    main()