import string
import requests
import random

def randomString(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

baseUrl = "https://cryptoroll.su/api"
jwt_token = None
login = randomString()
passwd = randomString()


def test_signUp_user():
    global login
    global passwd

    body = {
        "username":f"{login}",
        "password":f"{passwd}"
    }

    response = requests.post(url=f"{baseUrl}/signup", json=body)
    assert response.status_code == 201, f"Error! Status code = {response.status_code}"

    dataOfResponse = response.json()
    jwt_token = dataOfResponse.get('jwtToken')
    assert jwt_token, "Error! JWT token was not provided"
    
    

def test_post_login():
    global jwt_token
    global login
    global passwd

    data={
    "username": f"{login}",
    "password": f"{passwd}"
    }

    response = requests.post(f"{baseUrl}/login", json=data)
    assert response.status_code == 201, f"Error! Response code is {response.status_code}"
    dataResponse = response.json()
    user = dataResponse.get('user', {})
    jwt_token = dataResponse.get('jwtToken')

    assert user, "User is empty"
    assert jwt_token, "User is empty"

    name = user.get('name')
    assert name == login

def test_get_user_info():
    global jwt_token
    global login

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(f"{baseUrl}/user?username={login}", headers=headers)
    dataOfResponse = response.json()

    assert response.status_code == 200, f"Error! Status code is {response.status_code}"
    assert dataOfResponse, "Error! The recieved data is empty"

    username = dataOfResponse.get('username')
    assert username == login

def test_put_change_user_info():
    global jwt_token
    global login

    data = {
    "name": "haha",
    "password": f"{passwd}",
    "walletAddress": "hehe"
    }

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.put(f"{baseUrl}/user?username={login}", json=data, headers=headers)
    assert response.status_code == 200, f"Error! Status code: {response.status_code}"
    dataOfResponse = response.json()

    newToken = dataOfResponse.get("newToken")
    assert newToken != token
    jwt_token = newToken

    data = {
    "name": f"{login}",
    "password": f"{passwd}",
    "walletAddress": "hehe"
    }

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.put(f"{baseUrl}/user?username=haha", json=data, headers=headers) 
    assert response.status_code == 200, f"Status code: {response.status_code}"
    dataOfResponse = response.json()

    newToken = dataOfResponse.get("newToken")
    assert newToken != token
    jwt_token = newToken


def test_get_users_tasks():
    global jwt_token
    global login

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }    

    response = requests.get(url=f"{baseUrl}/tasks?username={login}", headers=headers)
    assert response.status_code == 200, f"Error! Status code is {response.status_code}"

    dataOfResponse = response.json()
    assert dataOfResponse, "No data recieved"



def test_post_change_status_of_tasks():
    global jwt_token
    global login

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }    
    response = requests.get(url=f"{baseUrl}/tasks?username={login}", headers=headers)
    assert response.status_code == 200, f"Error! Status code is {response.status_code}"
    dataOfResponse = response.json()
    tasksInfo = dataOfResponse.get('tasks', [])
    statusTastOne = tasksInfo[0].get('status')
    assert statusTastOne == "Uncompleted"

    body = {
    "taskId": 1,
    "changedStatus": "Completed"
    }

    headers = {
        'Authorization': f'Bearer {token}',
    }    

    response = requests.post(url=f"{baseUrl}/tasks?username={login}", json= body, headers=headers)
    assert response.status_code == 200, f"Error! Status code is {response.status_code}"

    response = requests.get(url=f"{baseUrl}/tasks?username={login}", headers=headers)
    assert response.status_code == 200, f"Error! Status code is {response.status_code}"
    dataOfResponse = response.json()
    tasksInfo = dataOfResponse.get('tasks', [])
    statusTastOne = tasksInfo[0].get('status')
    assert statusTastOne == "Completed"

    
def test_get_live_price():
    global login

    response = requests.get(f"{baseUrl}/livePrice?sym=Btc")
    assert response.status_code == 200, f"Error! Status code is {response.status_code}"

    dataOfResponse = response.text
    assert dataOfResponse, f"Error! The price is {dataOfResponse}"

def test_post_make_prediction():
    global jwt_token
    global login

    token = jwt_token

    body = {
        "username": f"{login}",
        "coin": "Btc",
        "predictionAmount": 10,
        "predictionTimeframe": "00:30:00",
        "predictionValue": "Up"
    }

    headers = {
        'Authorization': f'Bearer {token}',
    }    

    response = requests.post(url=f"{baseUrl}/match/createMatch?username={login}", json=body, headers=headers)

    assert response.status_code == 204, f"Error! Status code is {response.status_code}"

    response = requests.post(url=f"{baseUrl}/match/createMatch?username={login}", json=body, headers=headers)

    assert response.status_code == 400, f"Error! Status code is {response.status_code}"

def test_get_match_history():
    global jwt_token
    global login

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }    

    response = requests.get(url=f"{baseUrl}/match/history?username={login}&offset=0&limit=10", headers=headers)
    assert response.status_code == 200, f"Error! Status code is {response.status_code}"

def test_get_reward_status():
    global jwt_token
    global login

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }    

    response = requests.get(url=f"{baseUrl}/rewards/dailyRewardStatus?username={login}", headers=headers)
    assert response.status_code == 200, f"Error! Status code is {response.status_code}"
    assert response.json()

def test_collect_daily_reward():
    global jwt_token
    global login

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }    

    response = requests.get(url=f"{baseUrl}/rewards/dailyRewardStatus?username={login}", headers=headers)
    assert response.status_code == 200, f"Error! Status code is {response.status_code}"
    assert response.text

def test_get_user_referral_link():
    global jwt_token
    global login

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }    

    response = requests.get(url=f"{baseUrl}/referralLinks/?username={login}", headers=headers)
    assert response.status_code == 200, f"Error! Status code is {response.status_code}"
    assert response.__str__, f"Error! The response is {response}"

def test_visit_referral_link():
    global jwt_token
    global login

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }    

    salt = requests.get(url=f"{baseUrl}/referralLinks/?username={login}", headers=headers).__str__
    
    response = requests.post(url=f"{baseUrl}/referralLinks/visit?visitorName=hehe&referralSalt={salt}", headers=headers)

    assert response.status_code == 403, f"Error! The status code is {response.status_code}"

def test_post_check_quiz_result():
    global jwt_token
    global login

    token = jwt_token

    headers = {
        'Authorization': f'Bearer {token}',
    }    

    body = [
    {
        "questionId": 1,
        "questionAnswer": 0
    },
    {
        "questionId": 2,
        "questionAnswer": 3
    },
    {
        "questionId": 3,
        "questionAnswer": 2
    },
    {
        "questionId": 4,
        "questionAnswer": 2
    },
    {
        "questionId": 5,
        "questionAnswer": 1
    }
    ]

    [
    {
        "questionId": 1,
        "questionAnswer": 0
    },
    {
        "questionId": 2,
        "questionAnswer": 3
    },
    {
        "questionId": 3,
        "questionAnswer": 2
    },
    {
        "questionId": 4,
        "questionAnswer": 2
    },
    {
        "questionId": 5,
        "questionAnswer": 1
    }
]

    response = requests.post(url=f"{baseUrl}/quiz?username={login}", headers=headers, json=body)
    assert response.status_code == 200, f"Error! The status code is {response.status_code}"

    dataOfResponse = response.json()
    isQuizCompleted = dataOfResponse.get('isQuizCompleted')
    assert isQuizCompleted == False