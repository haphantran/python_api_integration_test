import requests
import json
def create_role(endpoint,headers,payload):
    return requests.post(endpoint, headers=headers,data=payload)

def get_role(endpoint,headers):
    return requests.get(endpoint, headers=headers)

def delete_role(endpoint,headers):
    return requests.delete(endpoint, headers=headers)

def update_role(endpoint,headers,payload):
    return requests.put(endpoint, headers=headers, data = payload)

def create_role_payload():
    return json.dumps({
        "name": "Test Role for integration testing",
        "description": "Role for testing",
        "permissions": ["user-create", "user-update"]
    })

def update_role_payload():
    return json.dumps({
        "name": "Test Role 1",
        "description": "Testing role",
        "permissions": [
            "user-create"
        ]
    })  


def user_api_headers(key,adminUserId):
    return { "Ocp-Apim-Subscription-Key": key, 
            "caller-id": adminUserId,
            "Content-Type": "application/json" }


