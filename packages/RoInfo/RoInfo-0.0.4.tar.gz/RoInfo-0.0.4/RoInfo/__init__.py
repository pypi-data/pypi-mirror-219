import json
import re
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    "x-csrftoken": "a",
    "x-requested-with": "XMLHttpRequest",
    "referer": "https://roblox.com",
}

session = requests.Session()
session.cookies[".ROBLOSECURITY"] = ''
def rbx_request(method, url, **kwargs):
    request = session.request(method, url, **kwargs)
    method = method.lower()
    if method in ["post", "put", "patch", "delete"]:
        if "X-CSRF-TOKEN" in request.headers:
            session.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
            if request.status_code == 403:  # Request failed, send it again
                request = session.request(method, url, **kwargs)

    return request

class Session():

    def __init__(self, token):

        self.token = str(token)
        self._username = ''
        self._headers = headers
        self._cookies = {
            "roblosecurity" : self.token,
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        session.cookies[".ROBLOSECURITY"] = self.token

        testt = rbx_request("get", "https://users.roblox.com/v1/users/authenticated")
        test = testt.json()
        if test['name']:
            print(f"Welcome, {test['name']} you have signed in successfully!")
            self.id = test['id']
            self._username = test['name']
        else:
            print("\033[91m WARNING!: Your are not signed into an existing account, please put the security cookie to an existing account or some functions may not work! \033[00m")

    



    def get_current_robux(self):
        request = json.dumps(rbx_request("get","https://economy.roblox.com/v1/user/currency").text)

        returndata = request['robux']
        
        return returndata

    def change_display_name(self, displayname):
        requestt = rbx_request("patch", f"https://users.roblox.com/v1/users/{self.id}/display-names", data={"newDisplayName": str(displayname)})

        request = requestt.json()

            
        return request


    
    def sendmessage(self, recipientid, subject, body):

        responsee = rbx_request("post", "https://privatemessages.roblox.com/v1/messages/send", data={"userId": self.id, "subject": subject, "body": body, "recipientId": recipientid})

        response = responsee.json()

        return response

class groups():

    def getgroupusers(self, groupid, limit):
        
        responsee = rbx_request("get", f"https://groups.roblox.com/v1/groups/{groupid}/users?sortOrder=Asc&limit={limit}")
        
        response = response.json()
        
        json_data = response['data']
        list = []

        for items in json_data:
            #Iterate over the list of articles
            for user in items:
                list.append(user)
        return list

    def setusergrouprole(self, groupid, userid, roleid):

        responsee = rbx_request("patch", f"https://groups.roblox.com/v1/groups/{groupid}/users/{userid}", data={"roleId": roleid})

        response = responsee.json()

        return response

    def groupsuserisin(self, userid):

        responsee = rbx_request("get", f"https://groups.roblox.com/v1/users/{userid}/groups/roles")

        response = responsee.json()

        return response

    def findusersinrole(self, groupid, roleid):
        
        responsee = rbx_request("get", f"https://groups.roblox.com/v1/groups/{groupid}/roles/{roleid}/users")

        response = responsee.json()

        json_data = response['data']
        list = []


        for user in json_data:
            list.append(user)

        return list

        def sendgroupfunds(self, groupid, userid, amount):

            responsee = rbx_request("post", f"https://groups.roblox.com/v1/groups/{groupid}/payouts", data={"PayoutType": 1,
            "Recipients": [
                {
                "recipientId": userid,
                "recipientType": "User",
                "amount": amount
                }   
            ]})
            response = responsee.json()

            return response




def userfollowers(self, userid):

    responsee = rbx_request("get", f"https://friends.roblox.com/v1/users/{userid}/followers/count")

    response = responsee.json()

    returnresponse = response['count']

    return returnresponse

def userfriends(self, userid):

    responsee = rbx_request("get", f"https://friends.roblox.com/v1/users/{userid}/friends/count")

    response = responsee.json()

    returnresponse = response['count']

    return returnresponse

def userjoindate(self, userid):

    responsee = rbx_request("get", f"https://users.roblox.com/v1/users/{userid}")

    response = responsee.json()

    returnresponse = response['created']

    return returnresponse
