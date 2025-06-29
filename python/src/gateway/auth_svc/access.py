import os, requests

# Package called auth service because it was communicating with auth service

def login(request):
    auth = request.authorization
    if not auth:
        return None , ("MISSING CREDENTIALS" , 401)
    
    basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth=basicAuth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text , response.status_code)

