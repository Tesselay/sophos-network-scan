import requests

def auth(id, secret):
    payload = {'grant_type':'client_credentials', 'client_id':id, 'client_secret':secret, 'scope':'token'}
    headers = {'Content-Type':'application/x-www-form-urlencoded'}

    response = requests.post('https://id.sophos.com/api/v2/oauth2/token', params=payload, headers=headers)
    return response

def getTenant(jwt):
    headers = {'Authorization: Bearer {}'.format(jwt)}

    response = requests.get('https://api.central.sophos.com/whoami/v1', headers=headers)
    return response

def getAllEndpoints(jwt, id, data_region):
    headers = {'Authorization: Bearer {}'.format(jwt), 'X-Tenant-ID: {}'.format(id)}

    response = requests.get('{}/endpoint/v1/endpoints'.format(data_region), headers=headers)
    endpoints = response['items']
    while response['nextKey'] != '':
        payload = {'pageFromKey': response['nextKey']}
        response = requests.get('{}/endpoint/v1/endpoints'.format(data_region), headers=headers, params=payload)
        endpoints.append(response['items'])

    return endpoints

def main(id, secret):
    auth_response = auth(id, secret)
    jwt_token = auth_response['access_token']

    tenant_response = getTenant(jwt_token)
    tenant_id = tenant_response['id']
    data_region = tenant_response['apiHosts']['dataRegion']

    endpoints = getAllEndpoints(jwt_token, tenant_id, data_region)

    for endpoint in endpoints:
        requests.post('{}/endpoint/v1/endpoints/{}/scans'.format(data_region, endpoint['id']))

if __name__ == '__main__':
    main()