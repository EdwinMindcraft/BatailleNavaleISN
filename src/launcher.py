import bataillenavale.main
import tkinter as tk
from tkinter import Frame
import socket
from threading import Thread


root = tk.Tk()
root.title("Launcher")

app = Frame(root, width = 300)
app.pack()

def runSolo():
    root.destroy()
    Thread(target=bataillenavale.main.run_game, args=(True, True, socket.gethostname())).start()
    
def runHost():
    host_help = tk.Tk()
    label_ip = tk.Label(host_help)
    label_ip["text"] = "IP : " + socket.gethostbyname(socket.gethostname())
    label_ip.pack()
    
    label_info = tk.Label(host_help)
    label_info["text"] = "En attente d\'un autre joueur..."
    label_info.pack()
    
    root.destroy()
    Thread(target=bataillenavale.main.run_game, args=(False, True, socket.gethostname())).start()
    
def runClient():
    root.destroy()
    join_window = tk.Tk()
    
    label_info = tk.Label(join_window)
    label_info["text"] = "Entrez une adresse IP"
    label_info.pack()
    
    entry = tk.Entry(join_window)
    entry.pack()
    
    connect = tk.Button()
    connect["text"] = "Connexion"
    connect["command"] = lambda: launchClient(entry.get(), join_window)
    connect.pack()

def launchClient(ip, join_window):
    join_window.destroy()
    Thread(target=bataillenavale.main.run_game, args=(False, False, ip)).start()
    
solo = tk.Button(root)
solo["text"] = "Solo"
solo["command"] = runSolo
solo.pack()

host = tk.Button(root)
host["text"] = "Host a game"
host["command"] = runHost
host.pack()

join = tk.Button(root)
join["text"] = "Join a game"
join["command"] = runClient
join.pack()


app.mainloop()