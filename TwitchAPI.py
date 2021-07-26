import requests
import dotenv

BASE_URL = 'https://api.twitch.tv/helix/'
CLIENT_ID = dotenv.get_key(".env", "TWITCHAPI")
CLIENT_SECRET = dotenv.get_key(".env", 'TWITCHAPISECRET')
OAUTHHEADERS = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'grant_type': 'client_credentials'}
OAUTHURL = "https://id.twitch.tv/oauth2/token"

def getOauth():  # This function gets the oauth2 token which is required for interacting with the twitchAPI
    try:
        req = requests.post(OAUTHURL, OAUTHHEADERS)
        jsondata = req.json()
        if 'access_token' in jsondata:
            OAUTH = jsondata['access_token']
            return OAUTH
    except Exception as e:
        print(e)


getOauth()

def checkUser(username, oauth):  # Checks to see if someone is live
    HEADERS = {'client-id': CLIENT_ID, 'Authorization': 'Bearer ' + oauth}
    URL = BASE_URL + 'streams?user_login=' + username
    try:
        req = requests.get(URL, headers=HEADERS)
        jsondata = req.json()
        if len(jsondata['data']) == 1:
            return True
        else:
            return False
    except Exception as e:
        print("Error checking user: ", e)
        return False


def getUserID(username, oauth):  # Gets the USERSID based on the Username they are given and also uses the OAUTH token
    # generated above
    HEADERS = {'client-id': CLIENT_ID, 'Authorization': 'Bearer ' + oauth}
    URL = BASE_URL + "users?login=" + username
    try:
        req = requests.get(URL, headers=HEADERS)
        jsondata = req.json()
        if len(jsondata['data']) == 1:
            ID = jsondata['id']
            return ID

    except Exception as e:
        print(e)

    # except Exception as e:
    #   print("Error getting ID for: ", Username, "Caused by: ", e)


def getstream(username, oauth):
    TWITCHURL = " https://www.twitch.tv/demomute"
    HEADERS = {'client-id': CLIENT_ID, 'Authorization': 'Bearer ' + oauth}
    URL = BASE_URL + 'streams?user_login=' + username
    try:
        req = requests.get(URL, headers=HEADERS)
        jsondata = req.json()
        if len(jsondata['data']) == 1:
            response = 'Demomute is live: ' + f'{TWITCHURL}'
            return response
        else:
            return False
    except Exception as e:
        print("Getting stream details: ", e)
        return False