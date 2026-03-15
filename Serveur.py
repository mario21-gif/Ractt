import socket
import time

# --- CONFIGURATION ---
HOST = '0.0.0.0'
PORT = 65432
PASSWORD = "1234"

def afficher_aide():
    print("""
Commandes disponibles :
  popup:<message>    - Affiche une notification sur le PC
  speak:<texte>      - Fait parler le PC
  browser:<url>      - Ouvre une URL dans le navigateur du PC
  lock               - Verrouille l'écran du PC
  battery            - Affiche le niveau de batterie du PC
  exit               - Quitte le serveur
  help               - Affiche ce menu d'aide
""")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((HOST, PORT))
            s.listen(1)
            print(f"[*] Serveur en ligne sur le port {PORT}")
            print("[*] En attente du PC...")

            conn, addr = s.accept()
            with conn:
                print(f"[+] PC Connecté : {addr}")

                # Authentification
                conn.sendall(b"AUTH_REQUIRED")
                auth_attempt = conn.recv(1024).decode().strip()
                if auth_attempt != PASSWORD:
                    print("[!] Mot de passe incorrect.")
                    conn.sendall(b"AUTH_FAILED")
                    return

                conn.sendall(b"AUTH_SUCCESS")
                print("[OK] Authentifié. Tapez 'help' pour voir les commandes disponibles.")

                # Boucle de commande
                while True:
                    cmd = input("\n> ").strip()
                    if not cmd:
                        continue

                    if cmd.lower() == "help":
                        afficher_aide()
                        continue

                    conn.sendall(cmd.encode())
                    if cmd == "exit":
                        print("[*] Déconnexion demandée.")
                        break

                    response = conn.recv(4096).decode(errors='ignore')
                    print(f"[PC] {response}")

        except socket.error as e:
            print(f"[!] Erreur réseau : {e}")
        except KeyboardInterrupt:
            print("\n[*] Arrêt du serveur par l'utilisateur.")
        except Exception as e:
            print(f"[!] Erreur inattendue : {e}")

if __name__ == "__main__":
    start_server()
