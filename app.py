import os
import subprocess
import getpass
import platform
from colorama import Fore, Style

translations = {
    'es': {
        'Bienvenido': 'Bienvenido',
        'Nombre del AP (SSID): ': 'Nombre del AP (SSID): ',
        'Contraseña del AP (dejar vacío para red abierta): ': 'Contraseña del AP (dejar vacío para red abierta): ',
        'No se encontraron interfaces de red disponibles.': 'No se encontraron interfaces de red disponibles.',
        'AP Falso ejecutándose': 'AP Falso ejecutándose',
        'AP Falso detenido': 'AP Falso detenido',
        'Selecciona una opción:': 'Selecciona una opción:',
        '1. Activar AP Falso': '1. Activar AP Falso',
        '2. Desactivar AP Falso': '2. Desactivar AP Falso',
        '3. Salir': '3. Salir',
        'Opción: ': 'Opción: ',
        'Opción no válida, intenta de nuevo.': 'Opción no válida, intenta de nuevo.',
    },
    'en': {
        'Bienvenido': 'Welcome',
        'Nombre del AP (SSID): ': 'AP Name (SSID): ',
        'Contraseña del AP (dejar vacío para red abierta): ': 'AP Password (leave empty for open network): ',
        'No se encontraron interfaces de red disponibles.': 'No network interfaces available.',
        'AP Falso ejecutándose': 'Fake AP running',
        'AP Falso detenido': 'Fake AP stopped',
        'Selecciona una opción:': 'Select an option:',
        '1. Activar AP Falso': '1. Activate Fake AP',
        '2. Desactivar AP Falso': '2. Deactivate Fake AP',
        '3. Salir': '3. Exit',
        'Opción: ': 'Option: ',
        'Opción no válida, intenta de nuevo.': 'Invalid option, please try again.',
    }
}

def translate(text, lang='es'):
    return translations[lang].get(text, text)

def obtener_interfaz_disponible():
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
    if platform.system() == 'Windows':
        os.system(f'netsh interface set interface "{interfaz}" admin=enable')
        os.system(f'netsh interface ip set address "{interfaz}" static 192.168.1.1 255.255.255.0')
    else:
        os.system(f'ip link set {interfaz} up')
        os.system(f'ip addr add 192.168.1.1/24 dev {interfaz}')

def crear_hostapd_conf(ssid, password, interfaz):
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
    subprocess.Popen(['hostapd', 'hostapd.conf'])

def iniciar_dnsmasq():
    subprocess.Popen(['dnsmasq', '-C', 'dnsmasq.conf'])

def detener_hostapd_dnsmasq():
    os.system('pkill hostapd')
    os.system('pkill dnsmasq')

def activar_ap():
    interfaz = obtener_interfaz_disponible()
    if not interfaz:
        print(Fore.RED + translate('No se encontraron interfaces de red disponibles.') + Style.RESET_ALL)
        return

    ssid = input(translate('Nombre del AP (SSID): '))
    password = getpass.getpass(translate('Contraseña del AP (dejar vacío para red abierta): '))

    configurar_red(interfaz)
    crear_hostapd_conf(ssid, password, interfaz)
    crear_dnsmasq_conf()
    iniciar_hostapd()
    iniciar_dnsmasq()
    print(Fore.GREEN + translate('AP Falso ejecutándose') + Style.RESET_ALL)

def desactivar_ap():
    detener_hostapd_dnsmasq()
    print(Fore.YELLOW + translate('AP Falso detenido') + Style.RESET_ALL)

def imprimir_banner(lang='es'):
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
⠀⠀⠙⠻⣦⣄⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⣠⣴⠟⠋⠀⠀
⠀⠀⠀⠀⠈⠻⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡶⣿⡟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢹⡇⠉⠙⠻⠷⢶⣶⣶⡶⠾⠟⠋⠉⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⠻⣦⣤⣤⣀⣀⣀⣀⣠⣤⣴⠿⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀By Mrx04programmer
'''
    print(Fore.GREEN + translate('Bienvenido') + Style.RESET_ALL if lang == 'es' else Fore.GREEN + translate('Welcome') + Style.RESET_ALL)
    print(banner)

def main():
    lang = input('Select language (es/en): ')
    while lang not in ['es', 'en']:
        print('Invalid language. Please select es or en.')
        lang = input('Select language (es/en): ')

    imprimir_banner(lang)
    while True:
        print(Style.BRIGHT + translate('Selecciona una opción:') + Style.RESET_ALL)
        print('1. ' + translate('Activar AP Falso', lang))
        print('2. ' + translate('Desactivar AP Falso', lang))
        print('3. ' + translate('Salir', lang))
        opcion = input(translate('Opción: ', lang))

        if opcion == '1':
            activar_ap()
        elif opcion == '2':
            desactivar_ap()
        elif opcion == '3':
            break
        else:
            print(Fore.RED + translate('Opción no válida, intenta de nuevo.', lang) + Style.RESET_ALL)

if __name__ == '__main__':
    main()
