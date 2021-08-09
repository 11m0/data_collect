import requests
import json

user_name = input('Input username: ')

response = requests.get(f'https://api.github.com/users/{user_name}/repos').json()

repos_list = []
for n, el in enumerate(response):
    repos_list.append(response[n].get('name'))

print(f'\nList of user repositories {user_name}:\n{repos_list}')

with open('repos_list.json', 'w') as file:
    json.dump(repos_list, file)
