import ipaddress
import tkinter as tk
from tkinter import filedialog

def print_ips(networks, output_file):
    with open(output_file, 'w') as f:
        for network in networks:
            try:
                if '-' in network:  # Check if it is a range
                    start_ip, end_ip = network.split('-')
                    start_ip = ipaddress.ip_address(start_ip)
                    end_ip = ipaddress.ip_address(end_ip)
                    for ip_int in range(int(start_ip), int(end_ip) + 1):
                        f.write(str(ipaddress.ip_address(ip_int)) + '\n')
                else:  # It is a single IP or network
                    net = ipaddress.ip_network(network)
                    for ip in net:
                        f.write(str(ip) + '\n')
            except ValueError:
                f.write(f"无效的IP地址段： {network}\n")

def browse_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    return output_file

def on_submit():
    networks = entry_networks.get().split(',')
    output_file = browse_output_file()
    print_ips(networks, output_file)

root = tk.Tk()
root.title("IP地址生成器")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_networks = tk.Label(frame, text="输入IP地址段（用逗号分隔，支持范围如192.168.1.1-192.168.1.5）：")
label_networks.grid(row=0, column=0, sticky="e")
entry_networks = tk.Entry(frame, width=50)
entry_networks.grid(row=0, column=1)

button_submit = tk.Button(frame, text="提交", command=on_submit)
button_submit.grid(row=1, columnspan=2, pady=10)

root.mainloop()
