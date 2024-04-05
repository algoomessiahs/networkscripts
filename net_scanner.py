
import scapy.all as scapy
import argparse


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="Target IP / IP range", dest="target")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please Specify a IP for the scanning use --help for more")
    return options.target


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    ans_lis = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]

    clients_list = []
    for element in ans_lis:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list
    # scapy.arping(ip) Just a solution to long lines...


def print_result(res_lis):
    print("IP\t\t\tMAC Address\n-------------------------------------------")
    for client in res_lis:
        print(client["ip"] + "\t\t" + client["mac"])


ip_addrs = getargs()
scan_res = scan(ip_addrs)
# scan_res = scan("10.0.2.1/24") # route -n to get router info Gateway
print_result(scan_res)
