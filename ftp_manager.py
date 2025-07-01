from ftplib import FTP, error_perm
import os
from config import BASE_DIR, FTP_HOST, ftp_credentials, ftp_backup_dir
from logger import log

def backup_to_ftp(local_path, region, client):
    creds = ftp_credentials.get(region)
    if not creds:
        print(f"❌ Aucun identifiant FTP défini pour la région : {region}")
        return
    
    base_backup_dir = ftp_backup_dir.get(region)
    if not base_backup_dir:
        print(f"❌ Aucun chemin FTP défini pour la région : {region}")
        return

    rel_path = os.path.relpath(local_path, BASE_DIR)
    ftp = FTP(FTP_HOST)
    ftp.login(user=creds["user"], passwd=creds["pass"])

    # Navigation dans FTP (ex: /ftp/grenoble/client)
    for folder in [base_backup_dir, client]:
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
