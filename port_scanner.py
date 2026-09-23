import socket
import tkinter as tk
import threading
import time

def start_scan():
    thread = threading.Thread(target=scan_ports)
    thread.start()


def scan_ports():
    target = entry.get()

    if not target:
        output.insert(tk.END, "Enter valid target\n")
        return
    try:
        target_ip = socket.gethostbyname(target)
    except Exception as e:
        output.insert(tk.END, f"Error resolving host or Invalid host:{e}\n")
        return

    output.delete('1.0', tk.END)
    output.insert(tk.END, f"Scanning {target}...\n\n")

    start_time = time.time()
    open_ports = []
    threads = [] 


    def scan_single_port(port, target):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.05)
        
         
        try:
            result = s.connect_ex((target, port))

            if result == 0:
              open_ports.append(port)
        except:
             pass
        s.close()

    for port in range(1, 1001):
            t = threading.Thread(target=scan_single_port, args=(port, target_ip))
            threads.append(t)
            t.start()
    
    for t in threads:
        t.join()
        
    open_ports.sort()

    if len(open_ports) == 0:
             output.insert(tk.END, "No open Ports Found\n")
           
    else:
            for port in open_ports:
                 output.insert(tk.END, f"Port {port} is OPEN\n")
           

    end_time = time.time()
    total_time = end_time - start_time

    output.insert(tk.END, "\nScan Completed")
    output.insert(tk.END, f"\nTime Taken: {round(total_time, 2)} seconds")

#GUI
root = tk.Tk()
root.title("Port Scanner")
root.geometry("400x400")

tk.Label(root, text="Enter Target:").pack()
entry = tk.Entry(root)
entry.pack()
tk.Button(root, text="Scan", command=start_scan).pack()
output = tk.Text(root, height=20, width=50)
output.pack()
root.mainloop()
