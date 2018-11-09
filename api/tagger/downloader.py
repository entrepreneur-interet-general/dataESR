import os
import sys
import logging
import tarfile
import shutil
import requests
import re
from tqdm import tqdm

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
URL_DATA = ""

class Downloader(object):
    def __init__(self, app, url=URL_DATA, download_dir=DATA_DIR):
        self._error = None
        self.url = url
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
            self.download_dir = download_dir
            self._download_data()
        else:
            app.logger.info('data already set up')

    @staticmethod
    def get_filename_from_cd(cd):
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        fname = re.findall('filename="(.+)"', cd)
        if len(fname) == 0:
            return None
        return fname[0]

    def _download_data(self):
        app.logger.info('downloading data...')
        r = requests.get(self.url, stream=True)
        total_length = r.headers.get('content-length', 0)
        pbar = tqdm(
            unit='B', unit_scale=True,
            total=int(total_length))
        if total_length is None:
            app.logger.error("Couldn't fetch app data.")
            raise Exception("Couldn't fetch app data.")
        else:
            filename = self.get_filename_from_cd(
                r.headers.get('content-disposition'))
            path = os.path.join(self.download_dir, filename)
            with open(path, 'wb') as f:
                for data in r.iter_content(chunk_size=4096):
                    f.write(data)
                    pbar.update(len(data))
            if filename.endswith('.tar.gz'):
                tar = tarfile.open(path, "r:gz")
                for tarinfo in tar:
                    tar.extract(tarinfo, self.download_dir)
                tar.close()
            # clean raw tar gz
            os.remove(path)
            app.logger.info('download complete')
