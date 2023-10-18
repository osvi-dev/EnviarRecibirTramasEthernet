import argparse
import time
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import send, sniff
from scapy.layers.l2 import getmacbyip
from scapy.all import get_if_addr
from threading import Thread
import os

flag= 0
n_paquetes = 0
def get_ip():
    return get_if_addr('Intel(R) Wireless-AC 9560') # remplazarlo con la interfaz de red

def get_mac_by_ip(ip):
    return getmacbyip(ip)

def send_ptk(mac_o, mac_d, ip_o, ip_d, times):
    #pkt = Ether(src=mac_o, dst=mac_d) / IP(src=ip_o, dst=ip_d) / ICMP() # Se configura por defecto en 8
    for _ in range(times):
        pkt = IP(src=ip_o, dst=ip_d) / ICMP()
        # print(pkt.summary())
        send(pkt, verbose=False)
    
def sniffer(pkt):
    global flag
    global n_paquetes
    if flag != n_paquetes:
        if pkt.haslayer(ICMP) and pkt.getlayer(ICMP).type == 0: # Es un echo replay
            # print(pkt.show())
            print(f"Echo replay de {pkt[IP].src}, time stamp: {time.time() - start_time} seconds")
            flag +=1      
    else:
        print('[!] saliendo...')  
        os._exit(1)

parse = argparse.ArgumentParser()
# parse.add_argument('-ipO', help='Ip Origen para mandar paquete por ethernet', required=True)
parse.add_argument('-ipD', help='-Ip Destino para mandar un paquete por ethernet', required=True)
# El numero de paquetes es opcional, si no manda es uno por defecto
parse.add_argument('-n', '--numero', type=int, help='Numero de paquetes a mandar', default=1)

args = parse.parse_args()
ip_o = get_ip()
ip_d = args.ipD
mac_o = get_mac_by_ip(ip_o)
mac_d = get_mac_by_ip(ip_d)

n_paquetes = args.numero
if len(ip_d) >= 7:
    start_time = time.time()
    hilo_enviar = Thread(target=send_ptk, args=(mac_o, mac_d, ip_o, ip_d, n_paquetes))
    hilo_enviar.start()
    sniff(prn=sniffer, timeout=5)  # Si no llegan todos los paquetes por 5 segundos, para 
else:
    print('[!] Error con las direcciones IP')


# sacar ip automatica origen 
# mantener macs
# cuando las reciva se acaba
# mandar tiempo por paquete, time stamp (tiempo en ida y vuelta)
# cuantos mandados y perdidos