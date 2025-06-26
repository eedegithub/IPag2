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

def browse_input_file():
    input_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if input_file:
        try:
            with open(input_file, 'r') as f:
                networks = [line.strip() for line in f if line.strip()]
                # 新增处理：对每个网络地址按分号分割并展平列表
                processed_networks = []
                for network in networks:
                    processed_networks.extend(network.split(';'))
                output_file = browse_output_file()
                if output_file:
                    print_ips(processed_networks, output_file)
        except Exception as e:
            status_var.set(f"错误: {str(e)}")

def on_submit():
    networks = entry_networks.get().split(';')
    output_file = browse_output_file()
    if output_file:
        print_ips(networks, output_file)

root = tk.Tk()
root.title("IP地址生成器")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_networks = tk.Label(frame, text="输入IP地址段（用分号分隔）：")
label_networks.grid(row=0, column=0, sticky="e", pady=5)
entry_networks = tk.Entry(frame, width=50)
entry_networks.grid(row=0, column=1, pady=5)

button_submit = tk.Button(frame, text="提交", command=on_submit)
button_submit.grid(row=1, column=0, pady=10, padx=5)

button_load = tk.Button(frame, text="载入文件", command=browse_input_file)
button_load.grid(row=1, column=1, pady=10, padx=5)

status_var = tk.StringVar()
status_var.set("就绪")
status_label = tk.Label(frame, textvariable=status_var, fg="green")
status_label.grid(row=2, columnspan=2, pady=5)

root.mainloop()
