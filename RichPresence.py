import sys
import subprocess
import time
import os
from pypresence import Presence
import psutil

# Dépendances nécessaires
required_packages = ["pypresence", "psutil"]

# Vérifier et installer automatiquement les dépendances manquantes
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"📦 {package} Needed for Discord Activity to Work. Downloading...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Définir l'ID de l'application Discord
CLIENT_ID = "1345377251230879866"  # Remplace avec ton ID Discord App
RPC = Presence(CLIENT_ID)
RPC.connect()

# Trouver le chemin absolu du dossier contenant le script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # Récupère le chemin du dossier où est situé le script
print(f"📁 Script path: {CURRENT_DIR}")

# Construction du chemin complet vers l'exécutable du jeu
GAME_PATH = os.path.join(CURRENT_DIR, "Propnight", "Binaries", "Win64", "Propnight-Win64-Shipping.exe")
GAME_PROCESS_NAME = "Propnight-Win64-Shipping.exe"  # Nom exact du processus

# Vérifier si le jeu est en cours d'exécution
def is_game_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == GAME_PROCESS_NAME.lower():  # Ignore case
            return True
    return False

# Lancer le jeu
try:
    print("🚀 Game Starting...")
    game_process = subprocess.Popen(GAME_PATH, shell=True)  # Lancement du jeu
    game_running = True
except Exception as e:
    print(f"⚠️ Error during game launch.. : {e}")
    sys.exit(1)  # Quitte le script si le jeu ne peut pas être lancé

# Attente du lancement du jeu
while not is_game_running():
    print("⏳ Game Not Detected... Waiting...")
    time.sleep(5)

print("🎮 Game Detected! Starting Rich Presence!")
RPC.update(
    state="Classic Propnight",
    details="Playing Propnight V1.1",
    large_image="propnightgame",
    large_text="https://dc.gg/Propnight",
    buttons=[{"label": "Come Play Propnight!", "url": "https://propnight.info"}]
)

# Boucle principale : vérifie si le jeu est encore en cours
while is_game_running():
    time.sleep(60)  # Vérification toutes les 60 secondes

# Une fois que le jeu est fermé, arrêter la Rich Presence et fermer le script
print("⏳ Game Activity Lost.. Turning off Rich Presence...")
RPC.clear()
sys.exit(0)  # Ferme proprement le script