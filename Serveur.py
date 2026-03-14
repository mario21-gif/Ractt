import socket
import time

# --- CONFIGURATION ---
HOST = '0.0.0.0' 
PORT = 65432
PASSWORD = "1234"

def start_server():
    # Utilisation d'un bloc 'with' pour fermer le socket proprement
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((HOST, PORT))
            s.listen(1)
            print(f"[*] Serveur Android en ligne sur le port {PORT}")
            print("[*] En attente du PC...")

            conn, addr = s.accept()
            with conn:
                print(f"[+] PC Connecté : {addr}")
                
                # Sécurité
                conn.sendall(b"AUTH_REQUIRED")
                if conn.recv(1024).decode().strip() != PASSWORD:
                    conn.sendall(b"AUTH_FAILED")
                    return

                conn.sendall(b"AUTH_SUCCESS")
                print("[OK] Authentifié.")

                while True:
                    cmd = input("\nCommande (popup:, speak:, browser:, lock, battery, location, exit) > ")
                    if not cmd: continue
                    
                    conn.sendall(cmd.encode())
                    if cmd == "exit": break
                    
                    response = conn.recv(4096).decode(errors='ignore')
                    print(f"[PC] {response}")
        except Exception as e:
            print(f"Erreur Serveur : {e}")

if __name__ == "__main__":
    start_server()
