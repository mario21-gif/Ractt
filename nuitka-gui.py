import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os, sys, subprocess
import ctypes

# ====== Windows Admin ======
def ensure_admin():
    if os.name != "nt":
        return
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False
    if not is_admin:
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit()

# ================== FONCTIONS ==================
assets_files = []

def browse_script():
    path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if path:
        script_entry.delete(0, tk.END)
        script_entry.insert(0, path)

def browse_icon():
    path = filedialog.askopenfilename(filetypes=[("ICO files", "*.ico")])
    if path:
        icon_entry.delete(0, tk.END)
        icon_entry.insert(0, path)

def browse_assets_files():
    files = filedialog.askopenfilenames(title="Sélectionne plusieurs fichiers", filetypes=[("Tous fichiers", "*.*")])
    if files:
        assets_files.clear()
        assets_files.extend(files)
        assets_entry.delete(0, tk.END)
        assets_entry.insert(0, ", ".join([os.path.basename(f) for f in files]))

def browse_output():
    path = filedialog.askdirectory()
    if path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, path)

def build_command():
    script = script_entry.get().strip()
    icon = icon_entry.get().strip()
    output_dir = output_entry.get().strip()

    if not script:
        messagebox.showerror("Erreur", "Sélectionne un fichier Python !")
        return None, None

    if not output_dir:
        output_dir = os.path.dirname(script)

    cmd = ["python -m nuitka"]
    if standalone_var.get(): cmd.append("--standalone")
    if onefile_var.get(): cmd.append("--onefile")
    if noconsole_var.get(): cmd.append("--windows-console=disable")
    if show_progress_var.get(): cmd.append("--show-progress")
    if remove_output_var.get(): cmd.append("--remove-output")
    if icon: cmd.append(f'--windows-icon-from-ico={icon}')

    for f in assets_files:
        dest = os.path.basename(f)
        cmd.append(f'--include-data-files={f}={dest}')

    if admin_uac_var.get():
        cmd.append("--windows-uac-admin")

    cmd.append("--enable-plugin=tk-inter")
    cmd.append(f'--output-dir={output_dir}')
    cmd.append(script)
    return cmd, output_dir

def run_nuitka():
    cmd, _ = build_command()
    if not cmd: return
    full_command = " ".join(cmd)
    subprocess.Popen(f'start cmd /k "{full_command}"', shell=True)
    print(f"Commande Nuitka : {full_command}")

# ================== GUI ==================
root = tk.Tk()
root.title("Nuitka GUI niggers")
root.geometry("600x600")

style = ttk.Style(root)
style.theme_use("clam")

# ----- FRAME FICHIERS -----
files_frame = ttk.LabelFrame(root, text="Fichiers / Dossiers", padding=10)
files_frame.pack(fill="x", padx=10, pady=5)

row1 = ttk.Frame(files_frame); row1.pack(fill="x", pady=4)
ttk.Label(row1, text="Script Python :", width=18).pack(side="left")
script_entry = ttk.Entry(row1, width=45); script_entry.pack(side="left", padx=5, fill="x", expand=True)
ttk.Button(row1, text="Choisir .py", command=browse_script).pack(side="right")

row2 = ttk.Frame(files_frame); row2.pack(fill="x", pady=4)
ttk.Label(row2, text="Icône (.ico) :", width=18).pack(side="left")
icon_entry = ttk.Entry(row2, width=45); icon_entry.pack(side="left", padx=5, fill="x", expand=True)
ttk.Button(row2, text="Parcourir", command=browse_icon).pack(side="right")

row3 = ttk.Frame(files_frame); row3.pack(fill="x", pady=4)
ttk.Label(row3, text="Fichiers assets :", width=18).pack(side="left")
assets_entry = ttk.Entry(row3, width=45); assets_entry.pack(side="left", padx=5, fill="x", expand=True)
ttk.Button(row3, text="Choisir fichiers", command=browse_assets_files).pack(side="right")

row4 = ttk.Frame(files_frame); row4.pack(fill="x", pady=4)
ttk.Label(row4, text="Dossier de sortie :", width=18).pack(side="left")
output_entry = ttk.Entry(row4, width=45); output_entry.pack(side="left", padx=5, fill="x", expand=True)
ttk.Button(row4, text="Parcourir", command=browse_output).pack(side="right")

# ----- OPTIONS NUITKA -----
options_frame = ttk.LabelFrame(root, text="Options Nuitka", padding=10)
options_frame.pack(fill="x", padx=10, pady=5)

standalone_var = tk.BooleanVar(value=True)
onefile_var = tk.BooleanVar(value=True)
noconsole_var = tk.BooleanVar(value=True)
show_progress_var = tk.BooleanVar(value=True)
remove_output_var = tk.BooleanVar(value=True)
admin_uac_var = tk.BooleanVar(value=False)

opts = [
    ("Standalone", standalone_var),
    ("Onefile", onefile_var),
    ("Console désactivée", noconsole_var),
    ("Barre de progression", show_progress_var),
    ("Nettoyer les fichiers temp", remove_output_var),
    ("Admin (UAC)", admin_uac_var),
]

for text, var in opts:
    ttk.Checkbutton(options_frame, text=text, variable=var).pack(anchor="w", pady=2)

# ----- BOUTON COMPILER -----
ttk.Button(root, text="🚀 Compiler", command=run_nuitka).pack(pady=20)
ensure_admin()
root.mainloop()