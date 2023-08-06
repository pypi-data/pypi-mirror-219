import re
import typing

if typing.TYPE_CHECKING:
    import requests


class Extractor:
    def __init__(
            self,
            http_client: 'requests.Session',
            force: bool = False
    ):
        self.http_client = http_client
        self.force = force

    def scan(self, target_urls):
        resources = {
            'images': dict(),
            'videos': dict()
        }

        print('Searching for downloadable media. This can take a while.')

        total = len(target_urls)
        counter = 0

        for target_url in target_urls:
            counter = counter + 1
            print(f'{counter} of {total}')

            response = self.http_client.get(target_url, timeout=10)
            response.raise_for_status()

            media_id = re.search(r'"media_id"\s*:\s*"(.*?)"', response.text)
            profile_id = re.search(r'"profile_id"\s*:\s*"(.*?)"', response.text)
            highlight_id = re.search(r'"highlight_reel_id"\s*:\s*"(.*?)"', response.text)

            if profile_id:
                response = self.http_client.get(
                    f'https://www.instagram.com/api/v1/feed/reels_media/?reel_ids={profile_id.group(1)}',
                    timeout=10,
                    headers={
                        'x-ig-app-id': '936619743392459'
                    }
                )

                response.raise_for_status()
                media_info = response.json()

                for reel_id, reel_item in media_info['reels'].items():
                    for item in reel_item['items']:
                        image_url = item['image_versions2']['candidates'][0]['url']
                        resource_id = item['id']
                        username = reel_item['user']['username']

                        resources['images'][image_url] = {
                            'url': image_url,
                            'id': resource_id,
                            'username': username
                        }

                        # Obtain the complete user object
                        with self.http_client.get(
                            f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}',
                            timeout=10,
                            headers={
                                'x-ig-app-id': '936619743392459'
                            }
                        ) as response:
                            response.raise_for_status()
                            user_data = response.json()
                            profile_picture_url = user_data['data']['user']['profile_pic_url_hd']

                            resources['images'][profile_picture_url] = {
                                'url': profile_picture_url,
                                'id': user_data['data']['user']['id'],
                                'username': user_data['data']['user']['username']
                            }

                        if 'video_versions' in item:
                            video_url = item['video_versions'][0]['url']

                            resources['videos'][video_url] = {
                                'url': video_url,
                                'id': resource_id,
                                'username': username
                            }
            elif media_id:
                response = self.http_client.get(
                    f'https://i.instagram.com/api/v1/media/{media_id.group(1)}/info/',
                    timeout=10,
                    headers={
                        'x-ig-app-id': '936619743392459'
                    }
                )

                response.raise_for_status()
                media_info = response.json()

                for item in media_info['items']:
                    if 'carousel_media' in item:
                        carousel_items = item['carousel_media']

                        for carousel_item in carousel_items:
                            image_url = carousel_item['image_versions2']['candidates'][0]['url']
                            resource_id = carousel_item['id']
                            username = item['user']['username']

                            resources['images'][image_url] = {
                                'url': image_url,
                                'id': resource_id,
                                'username': username
                            }

                            if 'video_versions' in carousel_item:
                                video_url = carousel_item['video_versions'][0]['url']

                                resources['videos'][video_url] = {
                                    'url': video_url,
                                    'id': resource_id,
                                    'username': username
                                }
                    else:
                        image_url = item['image_versions2']['candidates'][0]['url']
                        resource_id = item['id']
                        username = item['user']['username']

                        resources['images'][image_url] = {
                            'url': image_url,
                            'id': resource_id,
                            'username': username
                        }

                        if 'video_versions' in item:
                            video_url = item['video_versions'][0]['url']

                            resources['videos'][video_url] = {
                                'url': video_url,
                                'id': resource_id,
                                'username': username
                            }
            elif highlight_id:
                response = self.http_client.get(
                    f'https://www.instagram.com/api/v1/feed/reels_media/?reel_ids=highlight:{highlight_id.group(1)}',
                    timeout=10,
                    headers={
                        'x-ig-app-id': '936619743392459'
                    }
                )

                response.raise_for_status()
                media_info = response.json()

                for reel_id, reel_item in media_info['reels'].items():
                    for item in reel_item['items']:
                        image_url = item['image_versions2']['candidates'][0]['url']
                        resource_id = item['id']
                        username = reel_item['user']['username']

                        resources['images'][image_url] = {
                            'url': image_url,
                            'id': resource_id,
                            'username': username
                        }

                        if 'video_versions' in item:
                            video_url = item['video_versions'][0]['url']

                            resources['videos'][video_url] = {
                                'url': video_url,
                                'id': resource_id,
                                'username': username
                            }
            elif not self.force:
                raise RuntimeError(f'Failed to recognize resource type: {target_url}')

        return resources
