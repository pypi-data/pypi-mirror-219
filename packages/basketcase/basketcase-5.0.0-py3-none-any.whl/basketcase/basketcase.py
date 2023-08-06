import stat
from pathlib import Path
from datetime import datetime
import requests

from . import extractor
from . import authenticator
from . import storage


class BasketCase:
    def __init__(
        self,
        force_flag: bool = False
    ):
        # Create application data directory
        self.data_dir = f'{Path.home()!s}/.basketcase'
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        Path(self.data_dir).chmod(stat.S_IRWXU)

        # Set output directory
        output_name = f'basketcase_downloads/{datetime.now()!s}'
        self.output_dir = f'{Path.cwd()!s}/{output_name}'

        # Initialize dependencies
        self.http_client = requests.Session()
        self.storage = storage.Storage(self.data_dir)
        self.authenticator = authenticator.Authenticator(self.http_client, self.storage)
        self.extractor = extractor.Extractor(http_client=self.http_client, force=force_flag)

    def fetch(self, target_urls: set):
        resources = self.extractor.scan(target_urls)

        if resources['images'] or resources['videos']:
            for index, resource in resources['images'].items():
                self.get_image(resource)

            for index, resource in resources['videos'].items():
                self.get_video(resource)
        else:
            print('Nothing to download.')

    def get_image(self, resource: dict):
        user_dir = f'{self.output_dir}/{resource["username"]}'
        Path(user_dir).mkdir(parents=True, exist_ok=True)

        print(f'Downloading image: {resource["username"]}/{resource["id"]}')

        with self.http_client.get(resource['url'], timeout=10) as response:
            response.raise_for_status()

            with open(f'{user_dir}/{resource["id"]}.jpg', mode='w+b') as file:
                file.write(response.content)

    def get_video(self, resource: dict):
        user_dir = f'{self.output_dir}/{resource["username"]}'
        Path(user_dir).mkdir(parents=True, exist_ok=True)

        print(f'Downloading video: {resource["username"]}/{resource["id"]}')

        with self.http_client.get(resource['url'], timeout=10) as response:
            response.raise_for_status()

            with open(file=f'{user_dir}/{resource["id"]}.mp4', mode='w+b') as file:
                file.write(response.content)
