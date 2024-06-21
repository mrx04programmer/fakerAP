import os
import subprocess
import getpass
import platform

def obtener_interfaz_disponible():
    # Obtener interfaz de red disponible
    if platform.system() == 'Windows':
        output = subprocess.check_output('netsh wlan show interfaces').decode()
        for line in output.split('\n'):
            if 'Estado' in line and 'Conectado' in line:
                return line.split(':')[1].strip()
    else:
        os.system("ifconfig")
        interfaz = input("Interfaz >> ")
        return interfaz

def configurar_red(interfaz):
    # Habilitar interfaz de red
    if platform.system() == 'Windows':
        os.system(f'netsh interface set interface "{interfaz}" admin=enable')
        os.system(f'netsh interface ip set address "{interfaz}" static 192.168.1.1 255.255.255.0')
    else:
        os.system(f'ip link set {interfaz} up')
        os.system(f'ip addr add 192.168.1.1/24 dev {interfaz}')

def crear_hostapd_conf(ssid, password, seguridad, canal, interfaz):
    with open('hostapd.conf', 'w') as f:
        if seguridad == "1":
            conf = f'''
interface={interfaz}
driver=nl80211
ssid={ssid}
channel={canal}
'''
        elif seguridad == "2":
            conf = f'''
interface={interfaz}
driver=nl80211
ssid={ssid}
channel={canal}
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
'''
        f.write(conf)

def crear_dnsmasq_conf(interfaz):
    with open('dnsmasq.conf', 'w') as f:
        f.write(f'''
interface={interfaz}
dhcp-range=192.168.1.2,192.168.1.30,255.255.255.0,12h
''')

def iniciar_hostapd():
    # Iniciar hostapd
    subprocess.Popen(['hostapd', 'hostapd.conf'])

def iniciar_dnsmasq():
    # Iniciar dnsmasq
    subprocess.Popen(['dnsmasq', '-C', 'dnsmasq.conf'])

def detener_hostapd_dnsmasq():
    os.system('pkill hostapd')
    os.system('pkill dnsmasq')

def activar_ap():
    interfaz = obtener_interfaz_disponible()
    if not interfaz:
        print('No se encontraron interfaces de red disponibles.')
        return

    ssid = input('Nombre del AP (SSID): ')
    seguridad = input('Tipo de seguridad (1: Abierta, 2: WPA2): ')
    canal = input('Canal (1-11): ')
    password = ''
    
    if seguridad == "2":
        password = getpass.getpass('Contraseña del AP: ')

    configurar_red(interfaz)
    crear_hostapd_conf(ssid, password, seguridad, canal, interfaz)
    crear_dnsmasq_conf(interfaz)
    iniciar_hostapd()
    iniciar_dnsmasq()
    print('AP Falso ejecutándose')

def desactivar_ap():
    detener_hostapd_dnsmasq()
    print('AP Falso detenido')

def imprimir_banner():
    banner = '''
⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣴⡾⠛⠛⠻⣶⣶⡿⠛⠛⢿⣶⣶⠟⠛⠛⢷⣦⡀⠀⠀⠀⠀
⠀⠀⠀⠀⣾⠃⠀⣤⣴⠿⠀⣽⡇⠀⠀⢸⣯⠀⠿⣦⣤⠀⠘⣷⠀⠀⠀⠀
⠀⠀⠀⠀⣿⡠⠾⠟⠛⣠⡾⠋⠀⠀⠀⠀⠙⢷⣄⠛⠻⠷⢄⣿⠀⠀⠀⠀  
⠀⠀⢀⣴⡿⣷⣴⡶⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢶⣦⣾⢿⣦⡀  This tool was made for pentesting testing purposes and 
⠀⣠⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣄⠀    I am not responsible for any use that may be made of it.
⢰⡿⠁⢀⣴⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣦⡀⠈⢿⡆
⢺⡇⠀⣿⡿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⢿⣿⠀⢸⡗ 
⠈⢿⣦⡉⠁⠈⠉⠛⠷⣶⣦⣤⣄⣀⣀⣀⣠⣤⣴⣶⠾⠛⠉⠁⠈⢉⣴
⠀⠀⠙⠻⣦⣄⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⣠⣴⠟⠋⠀⠀
⠀⠀⠀⠀⠈⠻⣿⣶⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡶⣿⡟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢹⡇⠉⠙⠻⠷⢶⣶⣶⡶⠾⠟⠋⠉⠉⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⠻⣦⣤⣤⣀⣀⣀⣀⣠⣤⣴⠿⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀By Mrx04programmer
'''
    print(banner)

def main():
    imprimir_banner()
    while True:
        print('Selecciona una opción:')
        print('1. Activar AP Falso')
        print('2. Desactivar AP Falso')
        print('3. Salir')
        opcion = input('Opción: ')

        if opcion == '1':
            activar_ap()
        elif opcion == '2':
            desactivar_ap()
        elif opcion == '3':
            break
        else:
            print('Opción no válida, intenta de nuevo.')

if __name__ == '__main__':
    main()
