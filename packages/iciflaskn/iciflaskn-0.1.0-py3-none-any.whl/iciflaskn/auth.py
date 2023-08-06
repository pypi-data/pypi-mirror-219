from iciflaskn.config import config
from flask import session, current_app
from tapipy.tapis import Tapis
import requests



def is_logged_in():
    """
    Check whether the current session contains a valid login;
    If so: return True, username, roles
    Otherwse: return False, None, None
    """
    if 'username' in session:
        return True, session['username'], session['roles']
    return False, None, None 


def get_username(token):
    """
    Validate a Tapis JWT, `token`, and resolve it to a username.
    """
    headers = {'Content-Type': 'text/html'}
    # call the userinfo endpoint
    url = f"{config['tapis_base_url']}/v3/oauth2/userinfo"
    headers = {'X-Tapis-Token': token}
    try:
        rsp = requests.get(url, headers=headers)
        rsp.raise_for_status()
        username = rsp.json()['result']['username']
    except Exception as e:
        raise Exception(f"Error looking up token info; debug: {e}")
    return username


def add_user_to_session(username, token):
    """
    Add a user's identity and Tapis token to the session. 
    Also, look up users roles in Tapis and add those to the session.
    The list of roles are returned.
    """
    session['username'] = username
    session['token'] = token
    # also, look up user's roles
    t = Tapis(base_url=config['tapis_base_url'], access_token=token)
    try:
        result = t.sk.getUserRoles(user=username, tenant=config['tenant'])
        session['roles'] = result.names
    except Exception as e:
        raise Exception(f"Error getting user's roles; debug: {e}")
    return result.names


def clear_session():
    """
    Remove all data on the session; this function is called on logout.
    """
    session.pop('username', None)
    session.pop('token', None)
    session.pop('roles', None)

# config validation ---
if 'client_id' not in config:
    raise Exception("no client_id in config. Quitting..")
# else: 
#     current_app.logger.info(f"using client_id: {config['client_id']}")

if 'client_key' not in config or config['client_key'] == None:
    raise Exception("no client_key in config. Quitting..")
# else: 
#     current_app.logger.info(f"using client_key: ********")
    
if 'tapis_base_url' not in config:
    raise Exception("no tapis_base_url in config. Quitting..")
# else: 
#     current_app.logger.info(f"using tapis_base_url: {config['tapis_base_url']}")

if 'app_base_url' not in config:
    raise Exception("no app_base_url in config. Quitting..")
# else: 
#     current_app.logger.info(f"using app_base_url: {config['app_base_url']}")

