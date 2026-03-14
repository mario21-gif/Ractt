import socket
import subprocess
import webbrowser
import os
import time
import requests

# --- CONFIGURATION ---
HOST = '192.168.1.54' # <--- METS L'IP DE TON TEL ICI
PORT = 65432
PASSWORD = "1234"

def execute_action(command):
    try:
        if command.startswith("popup:"):
            subprocess.run(['notify-send', '📱 Mobile', command[6:]])
            return "Message affiché"
        
        elif command.startswith("speak:"):
            # Utilise espeak-ng qui est plus simple sur Linux
            subprocess.run(['espeak-ng', '-v', 'fr', command[6:]])
            return "Vocalisation faite"
        
        elif command.startswith("browser:"):
            webbrowser.open(command[8:])
            return "Navigateur ouvert"
        
        elif command == "lock":
            os.system("xdg-screensaver lock")
            return "Écran verrouillé"
        
        elif command == "battery":
            with open("/sys/class/power_supply/BAT0/capacity", "r") as f:
                return f"Batterie : {f.read().strip()}%"
                
        return "Commande inconnue"
    except Exception as e:
        return f"Erreur : {str(e)}"

def main():
    print(f"[*] Tentative de connexion vers {HOST}...")
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((HOST, PORT))
                
                # Authentification
                if s.recv(1024).decode() == "AUTH_REQUIRED":
                    s.sendall(PASSWORD.encode())
                
                if s.recv(1024).decode() == "AUTH_SUCCESS":
                    print("[+] Connecté au téléphone !")
                    s.settimeout(None)
                    while True:
                        data = s.recv(4096).decode()
                        if not data or data == "exit": break
                        print(f"[-] Reçu : {data}")
                        reponse = execute_action(data)
                        s.sendall(reponse.encode())
        except Exception:
            # Attend 5s si le serveur n'est pas joignable
            time.sleep(5)

if __name__ == "__main__":
    main()
