import paramiko
import os
from datetime import datetime
import pysftp

# SFTP Server credentials
SFTP_HOST = "your_sftp_server.com"
SFTP_PORT = 22  # Default SFTP port
SFTP_USERNAME = "your_username"
SFTP_PASSWORD = "your_password"
REMOTE_DIR = "/path/to/remote/directory"
LOCAL_DIR = "/path/to/local/directory"

# Ensure local directory exists
os.makedirs(LOCAL_DIR, exist_ok=True)

def download_daily_files():
    """Connects to SFTP, lists and downloads today's files"""
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disable host key checking (not recommended for production)

    try:
        with pysftp.Connection(SFTP_HOST, username=SFTP_USERNAME, password=SFTP_PASSWORD, cnopts=cnopts) as sftp:
            print("Connected to SFTP server.")

            sftp.cwd(REMOTE_DIR)  # Change to the target directory

            today_str = datetime.today().strftime('%Y-%m-%d')  # Format today's date
            files = sftp.listdir()

            for file in files:
                if today_str in file:  # Check if filename contains today's date
                    remote_file_path = f"{REMOTE_DIR}/{file}"
                    local_file_path = os.path.join(LOCAL_DIR, file)

                    sftp.get(remote_file_path, local_file_path)
                    print(f"Downloaded: {file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_daily_files()
