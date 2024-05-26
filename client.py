import requests

# response_user = requests.post('http://localhost:5000/user',
#                          json={'name': 'user_2', 'password': '12345678'}
#                          )
# response_user = requests.get('http://localhost:5000/user/5')
# print(response_user.text)

# response_ad = requests.post('http://localhost:5000/user/1/ad',
#                             json={
#                                 'header': 'exemple',
#                                 'description': 'exemple'
#                             })
response_ad = requests.get('http://localhost:5000/ad/show/4')
print(response_ad.text)
