import os
from datetime import datetime

# Adresse IP ou hostname du serveur FTP
FTP_HOST = "127.0.0.1"  # adapte selon ton serveur FTP

# Identifiants FTP par région (à adapter avec ce que tu as configuré)
ftp_credentials = {
    "Paris":     {"user": "ftp_user_paris",     "pass": "ftp_pass"},
    "Marseille": {"user": "ftp_user_marseille", "pass": "marseillepass"},
    "Rennes":    {"user": "ftp_user_rennes",    "pass": "rennespass"},
    "Grenoble":  {"user": "ftp_user_grenoble",  "pass": "123"},  # ex: Grenoble
}

# Chemin FTP de base (virtual_path FileZilla) par région
ftp_backup_dir = {
    "Paris": "/ftp/paris",
    "Marseille": "/ftp/marseille",
    "Rennes": "/ftp/rennes",
    "Grenoble": "/ftp/grenoble",
}

# Répertoire racine du système de fichiers local
BASE_DIR = os.path.abspath("./New_Tech")

# Fichier journal
LOG_FILE = "journal.log"

def log(message):
    """Écrit un message horodaté dans le fichier journal."""
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")
    print(message)
