from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()

key = os.getenv('key')
baseUrl = os.getenv("baseUrl")
organization = os.getenv("organization")
adminUserId = os.getenv("adminUserId")




hearders = { "Ocp-Apim-Subscription-Key": key, 
            "caller-id": adminUserId,
            "Content-Type": "application/json" }

payload =json.dumps({
    "name": "Test Role",
    "description": "Role for testing",
    "permissions": ["user-create", "user-update"]
})
create_role_response = requests.post(ENDPOINT, headers=hearders,data=payload)
data = create_role_response.json()
status_code = create_role_response.status_code

print(f"Status Code: {status_code}")
print(f"Response: {data}")

def test_can_create_role():
    payload ={
        "name": "Test Role",
        "description": "Role for testing",
        "permissions": ["user-create", "user-update"]
    }
    create_role_response = requests.post(f"{baseUrl}/organization/{organization}/roles", headers=hearders,data=payload)
    data = create_role_response.json()
    status_code = create_role_response.status_code
    assert status_code == 201

def create_role(payload,hearders):
    return requests.post(f"{baseUrl}/organization/{organization}/roles", headers=hearders,data=payload)

def get_role(roleId,hearders):
    return requests.get(f"{baseUrl}/roles/{roleId}", headers=hearders)

def new_role_payload():
    return 