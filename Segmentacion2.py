from os import system
import math

archivo_ips = open('ips.txt', 'w')

def binary_to_decimal(old_ip: str) -> str:
    octeto = '' # para ir guardando los octetos
    new_ip = ''
    being = 0
    end = 8
    for _ in range(4):
        octeto = old_ip[being:end]
        end +=1 
        being = end;
        end += 8
        new_ip = new_ip + '.' + str(int(octeto, 2)) 
    # print(new_ip)
    return new_ip[1:]

def build_ip(ip_base:str, subred:int, host:int, bits:int, delta_bits:int, num_red:int):
    # formamos una lista obtener las potencias
    potencias = []
    for i in range(subred):
        potencias.append(math.pow(2, i))
    potencias = sorted(potencias,reverse=True)  # ordemos al reves la lista    
    
    # Obtenemos la posicion de los numero 1's
    position_ones = []
    i = 0
    while num_red > 0:
        if potencias[i] <= num_red:
            position_ones.append(i)
            num_red = num_red - potencias[i]
        i +=1
    ceros = bits - delta_bits # saber cuantos ceros vamos a agregar
    ip_base = list(ip_base)
    for _ in range(ceros):
        ip_base.append('0')
    
    # agregamos los 1 en su posicion para la parte de red
    i = 0
    for j in range(delta_bits):
        if i < len(position_ones) and j == position_ones[i]:
            ip_base.append('1')
            i+=1
        else:
            ip_base.append('0')
            
    difusion = ip_base[::-1]
    ip = ''.join(ip_base)
    # print(ip) # me ayuda para ver la ip en binario
    
    # agremos 1's en la parte de host
    for j in range(host):
        difusion[j] = '1'
    difusion = difusion[::-1] #volteamos
    difusion = ''.join(difusion)  
    ip_red = split_ip(ip)
    ip_difusion = split_ip(difusion)
    
    return ip_red, ip_difusion

def split_ip(ip:str) -> str:
    partes = [ip[i:i+8] for i in range(0, len(ip), 8)]
    new_ip = '.'.join(partes)
    new_ip = binary_to_decimal(new_ip)
    return new_ip

def check_num_bits (n_subredes: int, n_host:int) -> list:
    i = 1
    list_bits = []
    bits = 0
    while bits <= n_subredes:
        bits = math.pow(2, i)
        i +=1
    list_bits.append(i-1)
    
    i = 1
    bits = 0
    while bits <= n_host:
        bits = math.pow(2, i)
        i +=1
    list_bits.append(i-1)
    
    return list_bits

system('cls')

mascara = {'A':24, 'B':16, 'C':8}
subredes = int(input('Ingrese el numero de subredes: '))

host = int(input('Ingrese el numero de host: '))

host += 2 # la primera y la ultima estan reservadas

list_bits = check_num_bits(subredes, host)
# print(list_bits) # bits necesarios de la parte de host y difusion
sum_bits = 0

for i in list_bits: # suma totales de bits
    sum_bits += i

clase = ''
for key in mascara:
    if sum_bits <= mascara[key]:
        clase = f'Es una red de clase {key}'
print(clase)

ip_base = ''
times = 0 
# Determinamos las clases
if clase[-1] == 'A':
    ip_base = '00011110' # 30
    times = 24
elif clase[-1] == 'B':
    ip_base = '1010110001100100' # 172.100
    times = 16
elif clase[-1] == 'C':
    ip_base = '110000001010100000000000' # 192.168.0
    times = 8

while True:
    try:
        num_red = input('Ingrese el numero de red que desee: ')
        if num_red == 'salir':
            print('[!] Saliendo...')
            for i in range(subredes):
                ip_red, ip_difusion = build_ip(ip_base,list_bits[0], list_bits[1],times,sum_bits,i)
                archivo_ips.write(f'Numero -> {i}\n')
                archivo_ips.write(f'Red -> {ip_red}\n')
                archivo_ips.write(f'Difusion -> {ip_difusion}\n')
                archivo_ips.write('\n')
            archivo_ips.close()  # Cerrar el archivo después de escribir los datos
            break
        num_red = int(num_red)
        if num_red > subredes-1:
            print('[!] Error.')
        else:
            ip_red, ip_difusion = build_ip(ip_base,list_bits[0], list_bits[1],times,sum_bits,num_red)
            print(f'Red -> {ip_red}')
            print(f'Difusion -> {ip_difusion}')
    except:
        pass 