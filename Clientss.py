import socket
import subprocess
import webbrowser
import os
import time
import platform
import sys

# --- CONFIGURATION ---
HOST = '192.168.1.54'  # Remplace par l'IP de ton téléphone
PORT = 65432
PASSWORD = "1234"

def execute_action(command):
    try:
        system = platform.system()

        if command.startswith("popup:"):
            message = command[6:]
            if system == "Linux":
                subprocess.run(['notify-send', '📱 Mobile', message])
            elif system == "Windows":
                from win10toast import ToastNotifier
                ToastNotifier().show_toast("📱 Mobile", message)
            elif system == "Darwin":  # macOS
                subprocess.run(['osascript', '-e', f'display notification "{message}" with title "📱 Mobile"'])
            return "Message affiché"

        elif command.startswith("speak:"):
            text = command[6:]
            if system == "Linux":
                subprocess.run(['espeak-ng', '-v', 'fr', text])
            elif system == "Windows":
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            elif system == "Darwin":
                subprocess.run(['say', text])
            return "Vocalisation faite"

        elif command.startswith("browser:"):
            webbrowser.open(command[8:])
            return "Navigateur ouvert"

        elif command == "lock":
            if system == "Linux":
                os.system("xdg-screensaver lock")
            elif system == "Windows":
                import ctypes
                ctypes.windll.user32.LockWorkStation()
            elif system == "Darwin":
                subprocess.run(['osascript', '-e', 'tell app "System Events" to keystroke "q" using {command down, control down}'])
            return "Écran verrouillé"

        elif command == "battery":
            if system == "Linux":
                with open("/sys/class/power_supply/BAT0/capacity", "r") as f:
                    return f"Batterie : {f.read().strip()}%"
            elif system == "Windows":
                import psutil
                battery = psutil.sensors_battery()
                return f"Batterie : {battery.percent}%"
            elif system == "Darwin":
                return "Batterie : Non supporté sur macOS (nécessite script AppleScript avancé)"
            else:
                return "Batterie : Non supporté sur cet OS"

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
