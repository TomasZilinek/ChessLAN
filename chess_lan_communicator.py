from tkinter import *


class Communicator:
    def __init__(self, root):
        self.root = root

    def connect(self):
        try:
            import subprocess
            import ipaddress
            import wmi
            import socket
        except:
            import pip
            pip.main(['install', "subprocess"])
            pip.main(['install', "ipaddress"])
            pip.main(['install', "wmi"])
            pip.main(['install', "socket"])

        wmi_obj = wmi.WMI()
        wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
        wmi_out = wmi_obj.query(wmi_sql)
        default_gateway = ""

        for dev in wmi_out:
            default_gateway = dev.DefaultIPGateway[0]
            default_gateway_remade = dev.DefaultIPGateway[0][:dev.DefaultIPGateway[0].rfind(".") + 1] + str(0)

        net_addr = default_gateway_remade + "/26"
        ip_net = ipaddress.ip_network(net_addr)
        all_hosts = list(ip_net.hosts())
        print("len(all_hosts) =", len(all_hosts), "\n"
                                                  "default_gateway =", default_gateway)
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE
        adresses = []

        print("\nSearching for online adresses...")

        for i in range(len(all_hosts)):
            output = subprocess.Popen(['ping', '-n', '1', '-w', '500', str(all_hosts[i])], stdout=subprocess.PIPE,
                                      startupinfo=info).communicate()[0]
            if not ("Destination host unreachable" in output.decode('utf-8') or "Request timed out" in output.decode(
                    'utf-8')):
                adresses.append(str(all_hosts[i]))
                print(all_hosts[i])

        print("online adresses: ", adresses)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_ip = socket.gethostbyname(socket.gethostname())
        host = socket.gethostname()
        port = 10000

        for addr in adresses:
            try:
                s.connect((addr, port))
                if s.recv(1024).decode("ascii") == "done":
                    print("connection successful: " + addr)
                    l = Label(self.root, text="connection successful")
                    l.pack()
            except Exception as e:
                print("cannot not connect to: " + addr + " ==> ", e)
        s.close()
