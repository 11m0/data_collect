import scrapy
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagramfollowers'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login_url = "https://www.instagram.com/accounts/login/ajax/"
    insta_login = 'Onliskill_udm'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1629825416:ASpQAMvl1EAdo0NdRZNcM1/' \
                'pjlU9rRg4n4cjCM00SDGSV5pDN6XbC93ZbYN67HUOHkXZnGGe2gIWPU2qtQY0HA' \
                'kIjR5U5syu+lv8qtqeI7cyy2ua6WmBV6AngVo1apn3eJ6O3UAFVgb+q5HtHsQ='
    user_parse_accounts_list = ['slyfoxbar', 'linux_memes']
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'
    api_url = 'https://i.instagram.com/api/v1/'

    def parse(self, response):
        yield scrapy.FormRequest(self.insta_login_url,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pwd},
                                 headers={'X-CSRFToken': self.fetch_csrf_token(response.text)})

    def login(self, response):
        j_data = response.json()
        if j_data['authenticated']:
            for user_parse_account in self.user_parse_accounts_list:
                yield response.follow(f'/{user_parse_account}',
                                      callback=self.parse_user,
                                      cb_kwargs={'username': user_parse_account})

    def parse_user(self, response, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {"count": 12}

        for user_status in ('following', 'followers'):
            get_follow_users_url = f'{self.api_url}friendships/{user_id}/{user_status}/?{urlencode(variables)}'
            yield response.follow(get_follow_users_url,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables),
                                             'user_status': user_status},
                                  callback=self.parse_user_follow,
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def parse_user_follow(self, response, username, user_id, variables, user_status):
        json_data = response.json()
        if json_data.get('next_max_id'):
            variables['max_id'] = json_data.get('next_max_id')
            get_following_users_url = f'{self.api_url}friendships/{user_id}/{user_status}/?{urlencode(variables)}'

            yield response.follow(get_following_users_url,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables),
                                             'user_status': user_status},
                                  callback=self.parse_user_follow,
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        for user in json_data.get('users'):
            item = InstaparserItem(
                username=user.get('username'),
                user_status=user_status,
                user_id=user.get('pk'),
                photo=user.get('profile_pic_url'),
                from_username=username
            )

            yield item


    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')


    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')