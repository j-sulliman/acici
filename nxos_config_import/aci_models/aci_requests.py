import json
import requests
from requests import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def aci_get(mo_dn, apic_url, apic_user, apic_pw):
    base_url = ('https://%s/api/' % apic_url)
    cookies = {}
    name_pwd = {'aaaUser': {'attributes': {'name': apic_user, 'pwd': apic_pw}}}
    json_credentials = json.dumps(name_pwd)
    # log in to API
    login_url = base_url + 'aaaLogin.json'
    post_response = requests.post(login_url, data=json_credentials, verify=False)
    # get token from login response structure
    auth = json.loads(post_response.text)
    login_attributes = auth['imdata'][0]['aaaLogin']['attributes']
    auth_token = login_attributes['token']
    # create cookie array from token
    # cookies = {}
    cookies['APIC-Cookie'] = auth_token
    sensor_url = (base_url + mo_dn)
    get_response = requests.get(sensor_url, cookies=cookies, verify=False).json()
    return get_response

def aci_post(mo_dn, mo, mo_data, apic_url, apic_user, apic_pw):
    # Construct JSON for logon request
    base_url = ('https://%s/api/' % apic_url)
    cookies = {}
    name_pwd = {'aaaUser': {'attributes': {'name': apic_user, 'pwd': apic_pw}}}
    json_credentials = json.dumps(name_pwd)


    # log in to API
    login_url = base_url + 'aaaLogin.json'
    post_response = requests.post(login_url, data=json_credentials, verify=False)
    # get token from login response structure
    auth = json.loads(post_response.text)
    login_attributes = auth['imdata'][0]['aaaLogin']['attributes']
    auth_token = login_attributes['token']
    # create cookie array from token
    cookies['APIC-Cookie'] = auth_token
    sensor_url = (base_url + mo_dn)

    # Convert the class based object into a dictionary and load into JSON format
    post_dict = mo_data.__dict__
    json_post = json.dumps(post_dict)
    get_response = requests.post(sensor_url, data=json_post, cookies=cookies, verify=False)
    time.sleep(0.5)


    # Check for success or failure of the post
    if get_response.status_code == 200:
        print("SUCCESS Posting Object: \'{}\' Name: \'{}\': Recieved response %s from APIC.".format(mo,
                                                                                                    post_dict[mo]['attributes']['name'], get_response.status_code))
        #logfile.write("SUCCESS Posting Object: \'%s\' Name: \'%s\': Recieved response %s from APIC.\n"
        #% (mo, post_dict[mo]['attributes']['name'], get_response.status_code))
    elif get_response.status_code != 200:
        print("FAILED Posting Object: \'{}\' Name: \'{}\': Recieved Response {}.".format(mo, post_dict[mo]['attributes']['name'], get_response.status_code))
        print('Review the input data and logfile for more detail')
        #pause = raw_input('PRESS ANY KEY TO CONTINUE PROCESSING')
        #logfile.write("FAILED Posting Object: \'%s\' Name: \'%s\': Recieved Response %s.\n"
        #% (mo, post_dict[mo]['attributes']['name'], get_response.status_code))
        #logfile.write('APIC Sent Response:\n')
        #logfile.write("%s\n" % (get_response).json())
    return json_post, get_response.status_code, sensor_url
