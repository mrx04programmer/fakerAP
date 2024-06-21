import os
import subprocess
import getpass
import platform

def get_available_interface():
    # Get available network interface
    if platform.system() == 'Windows':
        output = subprocess.check_output('netsh wlan show interfaces').decode()
        for line in output.split('\n'):
            if 'State' in line and 'Connected' in line:
                return line.split(':')[1].strip()
    else:
        os.system("ifconfig")
        interface = input("Interface >> ")
        return interface

def configure_network(interface):
    # Enable network interface
    if platform.system() == 'Windows':
        os.system(f'netsh interface set interface "{interface}" admin=enable')
        os.system(f'netsh interface ip set address "{interface}" static 192.168.1.1 255.255.255.0')
    else:
        os.system(f'ip link set {interface} up')
        os.system(f'ip addr add 192.168.1.1/24 dev {interface}')

def create_hostapd_conf(ssid, password, security, channel, interface):
    with open('hostapd.conf', 'w') as f:
        if security == "1":
            conf = f'''
interface={interface}
driver=nl80211
ssid={ssid}
channel={channel}
'''
        elif security == "2":
            conf = f'''
interface={interface}
driver=nl80211
ssid={ssid}
channel={channel}
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
'''
        f.write(conf)

def create_dnsmasq_conf(interface):
    with open('dnsmasq.conf', 'w') as f:
        f.write(f'''
interface={interface}
dhcp-range=192.168.1.2,192.168.1.30,255.255.255.0,12h
''')

def start_hostapd():
    # Start hostapd
    subprocess.Popen(['hostapd', 'hostapd.conf'])

def start_dnsmasq():
    # Start dnsmasq
    subprocess.Popen(['dnsmasq', '-C', 'dnsmasq.conf'])

def stop_hostapd_dnsmasq():
    os.system('pkill hostapd')
    os.system('pkill dnsmasq')

def activate_ap():
    interface = get_available_interface()
    if not interface:
        print('No available network interfaces found.')
        return

    ssid = input('AP Name (SSID): ')
    security = input('Security Type (1: Open, 2: WPA2): ')
    channel = input('Channel (1-11): ')
    password = ''
    
    if security == "2":
        password = getpass.getpass('AP Password: ')

    configure_network(interface)
    create_hostapd_conf(ssid, password, security, channel, interface)
    create_dnsmasq_conf(interface)
    start_hostapd()
    start_dnsmasq()
    print('Fake AP running')

def deactivate_ap():
    stop_hostapd_dnsmasq()
    print('Fake AP stopped')
    exit()

def print_banner():
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
    print_banner()
    while True:
        print('Select an option:')
        print('1. Activate Fake AP')
        print('2. Deactivate Fake AP')
        print('3. Exit')
        option = input('Option: ')

        if option == '1':
            activate_ap()
        elif option == '2':
            deactivate_ap()
        elif option == '3':
            break
        else:
            print('Invalid option, try again.')

if __name__ == '__main__':
    main()
