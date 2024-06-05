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

    response = requests.get('{}/endpoint/v1/endpoints'.format(data_region))
    return response

def main(id, secret):
    auth_response = auth(id, secret)
    tenant_response = getTenant(auth_response['access_token'])

    data_region = tenant_response['apiHosts']['dataRegion']

if __name__ == '__main__':
    main()