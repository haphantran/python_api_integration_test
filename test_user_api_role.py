from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()
from utils.helpers import create_role,get_role,new_role_payload,user_api_headers
key = os.getenv('key')
baseUrl = os.getenv("baseUrl")
organization = os.getenv("organization")
adminUserId = os.getenv("adminUserId")




hearders = user_api_headers(key,adminUserId)

payload = new_role_payload()



def test_can_create_role():
    payload = new_role_payload()
    create_role_response = requests.post(f"{baseUrl}/organization/{organization}/roles", headers=hearders,data=payload)
    data = create_role_response.json()
    status_code = create_role_response.status_code
    payload_json = json.loads(payload)
    print(f"Status code: {status_code}")
    print(f"Response: {data}")
    assert status_code == 201, f"Actual status code {status_code}"
    assert data['newRole']['name'] == payload_json["name"]
    assert data['newRole']['description'] == payload_json["description"]
    assert set(data['newRole']['permissions']) == set(payload_json["permissions"])

