import socket
import subprocess
import webbrowser
import os
import platform
import threading
import time
# Modules à installer avec 'pip install requests'
try:
    import requests
except ImportError:
    requests = None

# --- CONFIGURATION ---
HOST = '192.168.1.54' # IP de ton téléphone
PORT = 65432
PASSWORD = "1234"

def execute_action(command):
    try:
        if command.startswith("popup:"):
            # notify-send est intégré à Bazzite
            subprocess.run(['notify-send', '📱 Mobile', command[6:]])
            return "Notification OK"
        
        elif command.startswith("speak:"):
            # spd-say est le standard Linux pour la synthèse vocale
            subprocess.run(['spd-say', command[6:]])
            return "Vocalisation OK"
        
        elif command.startswith("browser:"):
            webbrowser.open(command[8:])
            return "Navigateur ouvert"
        
        elif command == "lock":
            os.system("xdg-screensaver lock")
            return "Session verrouillée"
        
        elif command == "battery":
            # Lecture du fichier système Linux pour la batterie
            with open("/sys/class/power_supply/BAT0/capacity", "r") as f:
                return f"Batterie : {f.read().strip()}%"
        
        elif command == "location":
            if requests:
                r = requests.get('https://ipinfo.io/json', timeout=5).json()
                return f"Ville: {r.get('city')}, IP: {r.get('ip')}"
            return "Module 'requests' manquant sur le PC"
            
        return "Commande inconnue"
    except Exception as e:
        return f"Erreur : {str(e)}"

def main():
    print(f"[*] Recherche de l'Android sur {HOST}...")
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((HOST, PORT))
                
                # Auth
                if s.recv(1024) == b"AUTH_REQUIRED":
                    s.sendall(PASSWORD.encode())
                
                if s.recv(1024) == b"AUTH_SUCCESS":
                    print("[+] Connecté !")
                    s.settimeout(None)
                    while True:
                        data = s.recv(4096).decode()
                        if not data or data == "exit": break
                        # threading permet de lancer l'action sans geler le script
                        res = execute_action(data)
                        s.sendall(res.encode())
        except Exception:
            # Reconnexion auto toutes les 5 secondes
            time.sleep(5)

if __name__ == "__main__":
    main()import subprocess
import webbrowser
import requests
import os
import socket as sock
import sys
import time
import platform
import threading

try:
    import ctypes  # Pour Windows (verrouillage de session)
    import pyttsx3  # Pour la synthèse vocale
except ImportError:
    pass  # On gère l'absence de ces modules plus tard

# --- CONFIGURATION ---
HOST = '127.0.0.1'  # Adresse IP du serveur
PORT = 65432        # Port de connexion
BUFFER_SIZE = 4096  # Taille du buffer réseau

def get_local_ip():
    """Récupère l'adresse IP locale de la machine."""
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

def show_popup(message):
    """Affiche un popup selon le système d'exploitation."""
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(['msg', '*', message], check=True)
        elif system == "Linux":
            try:
                subprocess.run(['notify-send', 'Message', message], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(['zenity', '--info', '--text', message], check=True)
        else:
            print(f"\n[POPUP] {message}\n")
        return "Popup affichée"
    except Exception as e:
        return f"Erreur popup: {str(e)}"

def open_browser(url):
    """Ouvre une URL dans le navigateur par défaut."""
    try:
        webbrowser.open(url)
        return "Navigateur ouvert"
    except Exception as e:
        return f"Erreur navigateur: {str(e)}"

def get_location():
    """Récupère la localisation via ipinfo.io."""
    try:
        r = requests.get('https://ipinfo.io/json', timeout=5).text
        return r
    except Exception:
        return "Erreur localisation"

def run_command(cmd):
    """Exécute une commande shell et retourne la sortie."""
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return out.decode('utf-8', errors='ignore') if out else "OK"
    except Exception as e:
        return str(e)

def lock_session():
    """Verrouille la session utilisateur selon le système d'exploitation."""
    system = platform.system()
    try:
        if system == "Windows":
            ctypes.windll.user32.LockWorkStation()
        elif system == "Linux":
            os.system("xdg-screensaver lock")
        return "Session verrouillée"
    except Exception as e:
        return f"Erreur verrouillage: {str(e)}"

def speak(text):
    """Synthétise vocalement le texte donné."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return "Message vocalisé"
    except Exception as e:
        return f"Erreur voix: {str(e)}"

def main():
    """Fonction principale du client."""
    print(f"[*] Client actif sur {platform.system()}. Connexion vers {HOST}:{PORT}...")

    while True:  # Boucle de reconnexion automatique
        try:
            with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(f"Connecté: {platform.system()} ({get_local_ip()})".encode())

                while True:
                    command = s.recv(BUFFER_SIZE).decode('utf-8', errors='ignore')
                    if not command:
                        break

                    print(f"[RECU] Commande : {command}")

                    if command.startswith("popup:"):
                        threading.Thread(target=show_popup, args=(command[6:],)).start()
                        s.sendall("OK: Popup affichée".encode())

                    elif command.startswith("browser:"):
                        webbrowser.open(command[8:])
                        s.sendall("OK: Navigateur ouvert".encode())

                    elif command == "location":
                        try:
                            r = requests.get('https://ipinfo.io/json', timeout=5).text
                            s.sendall(r.encode())
                        except Exception:
                            s.sendall("Erreur localisation".encode())

                    elif command.startswith("cmd:"):
                        try:
                            out = subprocess.check_output(command[4:], shell=True, stderr=subprocess.STDOUT)
                            s.sendall(out if out else b"OK")
                        except Exception as e:
                            s.sendall(str(e).encode())

                    elif command == "lock":
                        s.sendall(lock_session().encode())

                    elif command.startswith("speak:"):
                        threading.Thread(target=speak, args=(command[6:],)).start()
                        s.sendall("OK: Message vocalisé".encode())

                    elif command == "screenshot":
                        s.sendall("Fonctionnalité désactivée".encode())

                    elif command == "exit":
                        print("[INFO] Déconnexion demandée.")
                        return

        except ConnectionRefusedError:
            print("[ERREUR] Impossible de se connecter au serveur. Réessai dans 5 secondes...")
        except Exception as e:
            print(f"[ERREUR] {str(e)}")
        time.sleep(5)

if __name__ == "__main__":
    main()
import subprocess
import webbrowser
import requests
import os
import socket as sock
import sys
import time
import platform
import threading
try:
    import ctypes  # Pour Windows (verrouillage de session)
    import pyttsx3  # Pour la synthèse vocale
except ImportError:
    pass  # On gère l'absence de ces modules plus tard

# --- CONFIGURATION ---
HOST = '127.0.0.1'  # Adresse IP du serveur
PORT = 65432        # Port de connexion
BUFFER_SIZE = 4096  # Taille du buffer réseau

def get_local_ip():
    """Récupère l'adresse IP locale de la machine."""
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

def show_popup(message):
    """Affiche un popup selon le système d'exploitation."""
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(['msg', '*', message], check=True)
        elif system == "Linux":
            try:
                subprocess.run(['notify-send', 'Message', message], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(['zenity', '--info', '--text', message], check=True)
        else:
            print(f"\n[POPUP] {message}\n")
        return "Popup affichée"
    except Exception as e:
        return f"Erreur popup: {str(e)}"

def open_browser(url):
    """Ouvre une URL dans le navigateur par défaut."""
    try:
        webbrowser.open(url)
        return "Navigateur ouvert"
    except Exception as e:
        return f"Erreur navigateur: {str(e)}"

def get_location():
    """Récupère la localisation via ipinfo.io."""
    try:
        r = requests.get('https://ipinfo.io/json', timeout=5).text
        return r
    except Exception:
        return "Erreur localisation"

def run_command(cmd):
    """Exécute une commande shell et retourne la sortie."""
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return out.decode('utf-8', errors='ignore') if out else "OK"
    except Exception as e:
        return str(e)

def lock_session():
    """Verrouille la session utilisateur selon le système d'exploitation."""
    system = platform.system()
    try:
        if system == "Windows":
            ctypes.windll.user32.LockWorkStation()
        elif system == "Linux":
            os.system("xdg-screensaver lock")
        return "Session verrouillée"
    except Exception as e:
        return f"Erreur verrouillage: {str(e)}"

def speak(text):
    """Synthétise vocalement le texte donné."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return "Message vocalisé"
    except Exception as e:
        return f"Erreur voix: {str(e)}"

def main():
    """Fonction principale du client."""
    print(f"[*] Client actif sur {platform.system()}. Connexion vers {HOST}:{PORT}...")

    while True:  # Boucle de reconnexion automatique
        try:
            with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(f"Connecté: {platform.system()} ({get_local_ip()})".encode())

                while True:
                    command = s.recv(BUFFER_SIZE).decode('utf-8', errors='ignore')
                    if not command:
                        break

                    print(f"[RECU] Commande : {command}")

                    if command.startswith("popup:"):
                        threading.Thread(target=show_popup, args=(command[6:],)).start()
                        s.sendall("OK: Popup affichée".encode())

                    elif command.startswith("browser:"):
                        webbrowser.open(command[8:])
                        s.sendall("OK: Navigateur ouvert".encode())

                    elif command == "location":
                        try:
                            r = requests.get('https://ipinfo.io/json', timeout=5).text
                            s.sendall(r.encode())
                        except Exception:
                            s.sendall("Erreur localisation".encode())

                    elif command.startswith("cmd:"):
                        try:
                            out = subprocess.check_output(command[4:], shell=True, stderr=subprocess.STDOUT)
                            s.sendall(out if out else b"OK")
                        except Exception as e:
                            s.sendall(str(e).encode())

                    elif command == "lock":
                        s.sendall(lock_session().encode())

                    elif command.startswith("speak:"):
                        threading.Thread(target=speak, args=(command[6:],)).start()
                        s.sendall("OK: Message vocalisé".encode())

                    elif command == "screenshot":
                        s.sendall("Fonctionnalité désactivée".encode())

                    elif command == "exit":
                        print("[INFO] Déconnexion demandée.")
                        return

        except ConnectionRefusedError:
            print("[ERREUR] Impossible de se connecter au serveur. Réessai dans 5 secondes...")
        except Exception as e:
            print(f"[ERREUR] {str(e)}")
        time.sleep(5)

if __name__ == "__main__":
    main()
