import requests
import argparse

def auth(id, secret):
    payload = {'grant_type':'client_credentials', 'client_id':id, 'client_secret':secret, 'scope':'token'}
    headers = {'Content-Type':'application/x-www-form-urlencoded'}

    response = requests.post('https://id.sophos.com/api/v2/oauth2/token', params=payload, headers=headers)
    return response.json()

def getTenant(jwt):
    headers = {'Authorization: Bearer {}'.format(jwt)}

    response = requests.get('https://api.central.sophos.com/whoami/v1', headers=headers)
    return response.json()

def getAllEndpoints(jwt, id, data_region):
    headers = {'Authorization: Bearer {}'.format(jwt), 'X-Tenant-ID: {}'.format(id)}

    response = requests.get('{}/endpoint/v1/endpoints'.format(data_region), headers=headers)
    endpoints = response.json()['items']
    while response.json()['nextKey'] != '':
        payload = {'pageFromKey': response.json()['nextKey']}
        response = requests.get('{}/endpoint/v1/endpoints'.format(data_region), headers=headers, params=payload)
        endpoints.append(response.json()['items'])

    return endpoints

def main(id, secret):
    auth_response = auth(id, secret)
    jwt_token = auth_response.json()['access_token']

    tenant_response = getTenant(jwt_token)
    tenant_id = tenant_response.json()['id']
    data_region = tenant_response.json()['apiHosts']['dataRegion']

    endpoints = getAllEndpoints(jwt_token, tenant_id, data_region)

    for endpoint in endpoints:
        requests.post('{}/endpoint/v1/endpoints/{}/scans'.format(data_region, endpoint['id']))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Sophos Tenant Endpoint Scanner', description='Trigger scan on all endpoints of a Sophos tenant', epilog='For help on generating Client ID & Client Secret visit https://developer.sophos.com/getting-started-tenant')
    parser.add_argument('-cid', '--clientid', required=True, help='Your Sophos Client ID')
    parser.add_argument('-cs', '--clientsecret', required=True, help='Your Sophos Client Secret')
    args = parser.parse_args()
    main(args.clientid, args.clientsecret)