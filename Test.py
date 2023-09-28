from uuid import getnode
from scapy.all import Ether, sendp, sniff
from  threading import Thread, Event
import os
flag = Event() # variable de comunicacion de los hilos

def obtener_mac():
    mac = hex(getnode()).replace('0x','').upper()
    mac = mac.zfill(12)
    return ":".join(mac[i: i+2] for i in range(0,11,2))

class Enviar(Thread):
    
    def __init__(self, mac_o, mac_d):
        super().__init__()
        self.mac_o = mac_o
        self.mac_d = mac_d
    
    def run(self):
        
        print("Introduce un mensaje\no teclea salir para acabar con la aplicacion\n")
        while not flag.is_set():
            mensaje = input('> ')
            trama = Ether(src=self.mac_o, dst=self.mac_d) / mensaje.encode()
            sendp(trama, iface='Ethernet')
            if mensaje[0:5] == 'salir':
                print("\nPrograma finalizado...")
                os._exit(1) #salimos del hilo principal
                
class Recibir(Thread):
    def __init__(self, mac_d):
        super().__init__()
        self.mac_d = mac_d
    
    def run(self):
        while not flag.is_set():
            sniff(iface= "Ethernet", prn=self.leer_trama, stop_filter=self.stop)
    
    def leer_trama(self, trama):
        try:
            if trama[Ether].src == self.mac_d.lower() and trama.haslayer('Raw'):
                datos = trama.getlayer('Raw').load
                mensaje = datos.decode('utf-8')
                if mensaje[0:8] != "M-SEARCH": # Para que no llegue el trafico del navegador
                    print("\nMensaje recibido: ", mensaje)
                    if mensaje[0:5] == 'salir':
                        print("\nPrograma finalizado...")
                        os._exit(1)       
        except:
            pass
        
    def stop(self, trama):
        try:        
            if trama[Ether].src == self.mac_d.lower() and trama.haslayer('Raw'):
                datos = trama.getlayer('Raw').load
                mensaje = datos.decode('utf-8')
                if mensaje[0:5] == 'salir':
                    print("\nPrograma finalizado...")
                    os._exit(1) 
        except:
            pass
        
class Interconexion():
    
    MAC_ORIGEN = obtener_mac()
    # '80:E8:2C:28:BF:A3'
    MAC_DESTINO = 'D4:5D:64:5B:14:95'
    
    enviar = Enviar(MAC_ORIGEN, MAC_DESTINO)
    recibir = Recibir(MAC_DESTINO)
    
    enviar.start()
    recibir.start()
    
    enviar.join()
    recibir.join()
    
if __name__ == '__main__':
    conexion = Interconexion()