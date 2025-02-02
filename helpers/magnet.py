from seedrcc import Login,Seedr
from config import Config
import time
seedr = Login(Config.SEEDR_EMAIL,Config.SEEDR_PASSWORD)
seedr.authorize()
account = Seedr(seedr.token)

class Magnet:
    def __init__(self):
        self.seedr = seedr
        self.account = account
        self.delete_all_torrents()
    def delete_all_torrents(self):
        response = self.account.listContents()
        if response['files'] != []:
            for file in response['files']:
                self.account.deleteFile(file['id'])
        if response['folders'] != []:
            for folder in response['folders']:
                self.account.deleteFolder(folder['id'])
        if response['torrents'] != []:
            for file in response['torrents']:
                self.account.deleteTorrent(file['id'])
    def upload_torrent(self,magnet_link):
        self.account.addTorrent(magnet_link)
    def check_torrent(self,attempt=1):
        response = account.listContents()
        if attempt >= 20:
            return False
        elif response['torrents'] != []:
            time.sleep(10)
            return self.check_torrent(attempt+1)
        else:
            return True
    def select_File(self, response):
        # Check for files
        if response.get('files'):
            for file in response.get('files'):
                # Check for video files with size constraint
                if ('.mp4' in file['name'] or '.mkv' in file['name']) and file['size'] < 1950000000:
                    return file['name'], self.account.fetchFile(file['folder_file_id'])['url']
            # If we've checked all files but found none matching criteria
            return None, None
        # Check folders recursively
        elif response.get('folders'):       
            response = self.account.listContents(folderId=response['folders'][0]['id'])
            return self.select_File(response)
        # If no files or folders found
        return None, None
