from ftplib import FTP

ftp = FTP('127.0.0.1')
ftp.login('ftp_user', 'ftp_pass')
ftp.cwd('/documents')  # Dossier racine configuré dans FileZilla
print("Contenu du dossier FTP :", ftp.nlst())
ftp.quit()
