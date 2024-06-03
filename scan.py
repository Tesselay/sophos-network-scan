import requests

def main():
    payload = {'grant_type':'client_credentials', 'client_id':'', 'client_secret':'', 'scope':'token'}
    header = {'Content-Type':'application/x-www-form-urlencoded'}

    r = requests.get('https://id.sophos.com/api/v2/oauth2/token', params=payload, headers=header)

if __name__ == '__main__':
    main()