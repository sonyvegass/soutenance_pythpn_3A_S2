from ftplib import FTP, error_perm
import os
from config import BASE_DIR, FTP_HOST, FTP_USER, FTP_PASS, FTP_BACKUP_DIR
from logger import log

def backup_to_ftp(local_path, region, client):
    rel_path = os.path.relpath(local_path, BASE_DIR)
    ftp = FTP(FTP_HOST)
    ftp.login(user=FTP_USER, passwd=FTP_PASS)

    # Navigue dans le bon répertoire
    for folder in [FTP_BACKUP_DIR, region, client]:
        try:
            ftp.cwd(folder)
        except error_perm:
            try:
                ftp.mkd(folder)
                ftp.cwd(folder)
            except error_perm as e:
                log(f"Erreur MKD {folder} : {e}")
                print(f"Impossible de créer ou accéder à {folder}")
                ftp.quit()
                return

    # Envoi du fichier
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {os.path.basename(local_path)}", f)

    ftp.quit()
    log(f"Backup FTP : {local_path} vers {region}/{client}")
    print("✅ Fichier sauvegardé avec succès sur le FTP.")
