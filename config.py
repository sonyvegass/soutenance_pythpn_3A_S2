import os
from ftplib import FTP
from datetime import datetime

# Répertoire racine du système de fichiers
BASE_DIR = os.path.abspath("./New_Tech")

# Infos serveur FTP (à adapter selon ton environnement)
FTP_HOST = "127.0.0.1"
FTP_USER = "ftp_user"
FTP_PASS = "ftp_pass"
FTP_BACKUP_DIR = "/documents"

# Fichier journal
LOG_FILE = "journal.log"


def log(message):
    """Écrit un message horodaté dans le fichier journal."""
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")
    print(message)

def upload_file(ftp, local_path, remote_path):
    """Upload un fichier local vers le FTP, en créant les dossiers si besoin."""
    remote_dirs = os.path.dirname(remote_path).split('/')
    current_path = ""
    for d in remote_dirs:
        if d == '':
            continue
        current_path += '/' + d
        try:
            ftp.mkd(current_path)
        except Exception:
            # Le dossier existe peut-être déjà, on ignore l'erreur
            pass

    with open(local_path, "rb") as file:
        ftp.storbinary(f"STOR {remote_path}", file)
    log(f"Fichier uploadé : {local_path} → {remote_path}")

def sauvegarder():
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        log(f"Connecté au FTP {FTP_HOST}")

        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                local_file = os.path.join(root, file)
                relative_path = os.path.relpath(local_file, BASE_DIR)
                remote_file = os.path.join(FTP_BACKUP_DIR, relative_path).replace("\\", "/")
                upload_file(ftp, local_file, remote_file)

        ftp.quit()
        log("Sauvegarde terminée avec succès.")
    except Exception as e:
        log(f"Erreur lors de la sauvegarde FTP : {e}")

if __name__ == "__main__":
    sauvegarder()