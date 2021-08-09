import requests

url = 'https://api.worldweatheronline.com/premium/v1/weather.ashx'
params = {'key':'7403b4802025428b93f153851210708',
          'q':'Moscow',
          'format':'json'}

response = requests.get(url, params=params).json()

print(f"Погода в городе Москве - {response['data']['current_condition'][0]['temp_C']} градус(а) по цельсию.\n"
      f"Ощущается как - {response['data']['current_condition'][0]['FeelsLikeC']} градус(а) по цельсию.")
