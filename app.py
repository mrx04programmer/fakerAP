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
        output = subprocess.check_output(['ip', 'link', 'show']).decode()
        interfaces = [line.split()[1][:-1] for line in output.split('\n') if 'state UP' in line]
        return interfaces[0] if interfaces else None

def configurar_red(interfaz):
    # Habilitar interfaz de red
    if platform.system() == 'Windows':
        os.system(f'netsh interface set interface "{interfaz}" admin=enable')
        os.system(f'netsh interface ip set address "{interfaz}" static 192.168.1.1 255.255.255.0')
    else:
        os.system(f'ip link set {interfaz} up')
        os.system(f'ip addr add 192.168.1.1/24 dev {interfaz}')

def crear_hostapd_conf(ssid, password):
    with open('hostapd.conf', 'w') as f:
        f.write(f'''
interface={interfaz}
driver=nl80211
ssid={ssid}
channel=6
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
''')

def crear_dnsmasq_conf():
    with open('dnsmasq.conf', 'w') as f:
        f.write('''
interface=wlan0
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
    password = getpass.getpass('Contraseña del AP (dejar vacío para red abierta): ')

    configurar_red(interfaz)
    crear_hostapd_conf(ssid, password)
    crear_dnsmasq_conf()
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
⠈⢿⣦⡉⠁⠈⠉⠛⠷⣶⣦⣤⣄⣀⣀⣠⣤⣴⣶⠾⠛⠉⠁⠈⢉⣴
⠀⠀⠙⠻⣦⣄⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⣠⣴⠟⠋⠀⠀
⠀⠀⠀⠀⠈⠻⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡶⣿⡟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢹⡇⠉⠙⠻⠷⢶⣶⣶⡶⠾⠟⠋⠉⢸⡟⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⠀ FAKER AP   ⠀⣸⡇⠀⠀⠀⠀⠀⠀
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
