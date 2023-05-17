from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()
from utils.helpers import create_role,get_role,delete_role,update_role,create_role_payload,update_role_payload,user_api_headers
key = os.getenv('key')
baseUrl = os.getenv("baseUrl")
organization = os.getenv("organization")
adminUserId = os.getenv("adminUserId")


headers = user_api_headers(key,adminUserId)


def test_can_create_role():
    payload = create_role_payload()
    create_role_response = create_role(f"{baseUrl}/organization/{organization}/roles", headers=headers,payload=payload)
    data = create_role_response.json()
    status_code = create_role_response.status_code
    print(f"Status code: {status_code}")
    print(f"Response: {data}")
    # test the response with payload data
    payload_json = json.loads(payload)
    assert status_code == 201, f"Can't create the role, Actual status code {status_code}"
    assert data['newRole']['name'] == payload_json["name"]
    assert data['newRole']['description'] == payload_json["description"]
    assert set(data['newRole']['permissions']) == set(payload_json["permissions"])
    # delete the role after the test
    roleId = data['newRole']['id']
    delete_role_response = delete_role(f"{baseUrl}/roles/{roleId}", headers)
    assert delete_role_response.status_code == 200, f"Can't delete the role, Actual status code {delete_role_response.status_code}"

def test_can_get_role():
    # create a role
    payload = create_role_payload()
    create_role_response = create_role(f"{baseUrl}/organization/{organization}/roles", headers=headers,payload=payload)
    create_role_data = create_role_response.json()
    # get roleId
    roleId = create_role_data['newRole']['id']
    # get role using roleID
    get_role_response = get_role(f"{baseUrl}/roles/{roleId}", headers)
    status_code = get_role_response.status_code
    get_role_data = get_role_response.json()
    print(f"Status code: {status_code}")
    print(f"Response: {get_role_data}")
    # test the response with payload data
    payload_json = json.loads(payload)
    assert status_code == 200, f"Can't get the role, Actual status code {status_code}"
    assert get_role_data['role']['name'] == payload_json["name"]
    assert get_role_data['role']['description'] == payload_json["description"]
    assert set(get_role_data['role']['permissions']) == set(payload_json["permissions"])
    # delete the role after the test
    delete_role_response = delete_role(f"{baseUrl}/roles/{roleId}", headers)
    assert delete_role_response.status_code == 200, f"Can't delete the role, Actual status code {delete_role_response.status_code}"

def test_can_update_role():
    # create a role
    payload = create_role_payload()
    create_role_response = create_role(f"{baseUrl}/organization/{organization}/roles", headers=headers,payload=payload)
    create_role_data = create_role_response.json()
    # get roleId
    roleId = create_role_data['newRole']['id']
    # update role using roleID
    update_payload = update_role_payload()
    update_role_response = update_role(f"{baseUrl}/roles/{roleId}", headers, payload=update_payload)
    status_code = update_role_response.status_code
    update_role_data = update_role_response.json()
    print(f"Status code: {status_code}")
    print(f"Response: {update_role_data}")
    # test the response with data
    update_role_payload_json =  json.loads(update_payload)
    assert status_code == 200, f"Can't update the role, Actual status code {status_code}"
    assert update_role_data['updated']['name'] == update_role_payload_json["name"]
    assert update_role_data['updated']['description'] == update_role_payload_json["description"]
    assert set(update_role_data['updated']['permissions']) == set(update_role_payload_json["permissions"])
    # delete the role after the test
    delete_role_response = delete_role(f"{baseUrl}/roles/{roleId}", headers)
    assert delete_role_response.status_code == 200, f"Can't delete the role, Actual status code {delete_role_response.status_code}"

def test_can_delete_role():
    # create a role
    payload = create_role_payload()
    create_role_response = create_role(f"{baseUrl}/organization/{organization}/roles", headers=headers,payload=payload)
    create_role_data = create_role_response.json()
    # get roleId
    roleId = create_role_data['newRole']['id']
    # delete role using roleID
    delete_role_response = delete_role(f"{baseUrl}/roles/{roleId}", headers)
    status_code = delete_role_response.status_code
    delete_role_data = delete_role_response.json()
    print(f"Status code: {status_code}")
    print(f"Response: {delete_role_data}")
    # test the response with data
    payload_json =  json.loads(payload)
    assert status_code == 200, f"Can't delete the role, Actual status code {status_code}"
    assert delete_role_data['deleted']['name'] == payload_json["name"]
    assert delete_role_data['deleted']['description'] == payload_json["description"]
    assert set(delete_role_data['deleted']['permissions']) == set(payload_json["permissions"])