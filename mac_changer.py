

import subprocess
import optparse
import re


def get_current_mac(interface):
    interface_val = subprocess.check_output(["ifconfig", interface])
    mac_val = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(interface_val))
    if mac_val:
        return str(mac_val.group(0))
    else:
      print("[-] Error Reading Mac address")


def change_mac(interface, new_mac):
    print("[+] Changing " + interface + " Mac to new_mac " + new_mac)
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])
    current_mac = get_current_mac(interface)
    if current_mac == new_mac:
        print("[+] Mac Address Changed Successfully \n Current Mac " + current_mac)
    else:
        print("[-] Error Changing Mac")


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Change interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="Change Device Mac")
    (options, args) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify a value for the interface use -h for more")
    elif not options.new_mac:
        parser.error("[-] Please specify a value for the mac use -h for more")
    else:
        return options


val = get_args()
print("Current Mac = " + get_current_mac(val.interface))
change_mac(val.interface, val.new_mac)
