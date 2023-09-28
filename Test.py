from uuid import getnode
from scapy.all import Ether, sendp, sniff
from  threading import Thread, Event

flag = Event()

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
        while not flag.is_set():
            mensaje = input('Introduce un mensaje\n o teclea salir para acabar con la aplicacion')
            trama = Ether(src=self.mac_o, dst=self.mac_d) / mensaje.encode()
            sendp(trama, iface='Ethernet')
            if mensaje[0:5] == 'salir':
                flag.set()
                break
                
class Recibir(Thread):
    def __init__(self, mac_d):
        super().__init__()
        self.mac_d = mac_d
    
    def run(self):
        while not flag.is_set():
            sniff(iface= "Ethernet", prn=self.leer_trama, stop_filter=self.stop)
    
    def leer_trama(self, trama):
        try:
            if trama[Ether].src == self.mac_d.lower() and trama.haslayer('Raw'): #implementar el filtro
                datos = trama.getlayer('Raw').load
                mensaje = datos.decode('utf-8')
                print("\n Mensaje recibido: ", mensaje)            
        except:
            pass
        
    def stop(self, trama):
        try:
            if trama[Ether].src == self.mac_d.lower() and trama.haslayer('Raw'): #implementar el filtro para que no salga el trafico de red
                datos = trama.getlayer('Raw').load
                mensaje = datos.decode('utf-8')
                if mensaje[0:5] == 'salir':
                   flag.set()
                   return True 
        except:
            pass
        
class Interconexion():
    global flag
    MAC_ORIGEN = obtener_mac()
    MAC_DESTINO = '80:E8:2C:28:BF:A3'
    
    enviar = Enviar(MAC_ORIGEN, MAC_DESTINO)
    recibir = Recibir(MAC_DESTINO)
    
    enviar.start()
    recibir.start()
    
    enviar.join()
    recibir.join()
    

    