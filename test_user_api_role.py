from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()
from utils.helpers import *
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

def test_can_get_all_roles():
    # create a role
    payload = create_role_payload()
    create_role_response = create_role(f"{baseUrl}/organization/{organization}/roles", headers=headers,payload=payload)
    create_role_data = create_role_response.json()
    # get roleId
    roleId = create_role_data['newRole']['id']
    # get all roles
    get_all_roles_response = get_all_roles(f"{baseUrl}/organization/{organization}/roles", headers)
    status_code = get_all_roles_response.status_code
    get_all_roles_data = get_all_roles_response.json()
    print(f"Status code: {status_code}")
    print(f"Total number of roles: {len(get_all_roles_data['roles'])}")
    role_ids = [role['id'] for role in get_all_roles_data['roles']]
    # test the status and new role in the list of roles
    assert status_code == 200, f"Can't get all the roles, Actual status code {status_code}"
    assert get_all_roles_data['success'] == True, f"Can't get all the roles, Actual response {get_all_roles_data['success']}"
    assert roleId in role_ids, f"Newly created roles is not in roles list"
    # delete the role after the test
    delete_role_response = delete_role(f"{baseUrl}/roles/{roleId}", headers)
    assert delete_role_response.status_code == 200, f"Can't delete the role, Actual status code {delete_role_response.status_code}"

def test_can_assign_and_unassign_user_role():
    # create a role
    new_role_payload = create_role_payload()
    create_role_response = create_role(f"{baseUrl}/organization/{organization}/roles", headers=headers,payload=new_role_payload)
    create_role_data = create_role_response.json()
    # get roleId
    roleId = create_role_data['newRole']['id']
    # create a user
    new_user_payload = create_user_payload()
    create_user_response = create_user(f"{baseUrl}/organization/{organization}/users", headers=headers,payload=new_user_payload)
    create_user_data = create_user_response.json()
    # get userId
    userId = create_user_data['newUser']['id']
    # assign role to user
    assign_role_response = assign_user_role(f"{baseUrl}/users/{userId}/roles/{roleId}", headers)
    status_code = assign_role_response.status_code
    assign_role_data = assign_role_response.json()
    print(f"Status code: {status_code}")
    print(f"Response: {assign_role_data}")
    # test the response with data
    assert status_code == 200, f"Can't assign role to user, Actual status code {status_code}"
    assert assign_role_data['success'] == True, f"Can't assign role to user, Actual response {assign_role_data['success']}"
    # get roles for users
    get_roles_for_user_response = get_roles_for_user(f"{baseUrl}/users/{userId}/roles", headers)
    status_code = get_roles_for_user_response.status_code
    get_roles_for_user_data = get_roles_for_user_response.json()
    print(f"Status code: {status_code}")
    print(f"Response: {get_roles_for_user_data}")
    # test that user has the new role
    assert status_code == 200, f"Can't get roles for user, Actual status code {status_code}"
    assert get_roles_for_user_data['success'] == True, f"Can't get roles for user, Actual response {get_roles_for_user_data['success']}"
    assert roleId in [role['id'] for role in get_roles_for_user_data['roles']], f"Newly created role is not in roles list for user"
    
    # unassigne role from user
    unassign_role_response = unassign_user_role(f"{baseUrl}/users/{userId}/roles/{roleId}", headers)
    status_code = unassign_role_response.status_code
    unassign_role_data = unassign_role_response.json()
    print(f"Status code: {status_code}")
    print(f"Response: {unassign_role_data}")
    # test the response with data
    assert status_code == 200, f"Can't unassign role from user, Actual status code {status_code}"
    assert unassign_role_data['success'] == True, f"Can't unassign role from user, Actual response {unassign_role_data['success']}"
    # get roles for users again
    get_roles_for_user_response = get_roles_for_user(f"{baseUrl}/users/{userId}/roles", headers)
    status_code = get_roles_for_user_response.status_code
    get_roles_for_user_data = get_roles_for_user_response.json()

    # test user doesn't have the role anymore
    assert status_code == 200, f"Can't get roles for user, Actual status code {status_code}"
    assert get_roles_for_user_data['success'] == True, f"Can't get roles for user, Actual response {get_roles_for_user_data['success']}"
    assert roleId not in [role['id'] for role in get_roles_for_user_data['roles']], f"User does not have the role after unassigning"

    # delete the user after the test
    delete_user_response = delete_user(f"{baseUrl}/users/{userId}", headers)
    assert delete_user_response.status_code == 200, f"Can't delete the user, Actual status code {delete_user_response.status_code}"
    # delete the role after the test
    # might not beable to delete role, need to un assign first
    delete_role_response = delete_role(f"{baseUrl}/roles/{roleId}", headers)
    assert delete_role_response.status_code == 200, f"Can't delete the role, Actual status code {delete_role_response.status_code}"

