import requests
import json
def create_role(endpoint,payload,hearders):
    return requests.post(endpoint, headers=hearders,data=payload)

def get_role(endpoint,roleId,hearders):
    return requests.get(endpoint, headers=hearders)

def new_role_payload():
    return json.dumps({
        "name": "Test Role for integration testing",
        "description": "Role for testing",
        "permissions": ["user-create", "user-update"]
    })
def user_api_headers(key,adminUserId):
    return { "Ocp-Apim-Subscription-Key": key, 
            "caller-id": adminUserId,
            "Content-Type": "application/json" }