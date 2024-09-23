import requests


url = "https://sandbox-api.paddle.com/transactions/txn_01j8bk4sb3gz4nec7qbxtfh403"
headers = {
    "Authorization": "Bearer c991aec23aea278df89bbcf0b6ed3361ebee1750e72808018e",  # Replace with your Paddle access token
    "Content-Type": "application/json",
}

response = requests.get(url, headers=headers)
data = response.json().get('data').get('status')
print(data)



