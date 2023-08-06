# The `iciflaskn` Package


## Intro

The `iciflaskn` package provides a Flask blueprint that can be registered with your
Flask application to endow it with authentication based on OAuth2. 
The high-level steps to use this package are as follows:

1. Install the package, for example, using pip: `pip install iciflaskn`
2. Register an OAuth client with an ICICLE Tapis tenant.
3. Create a `config.yaml` containing the configuration of your OAuth client.
4. Import the iciflaskn blueprint and register it on your app.

See the Detailed Usage section for more details.

## Detailed Usage


Suppose we have a Flask application, `app.py`, that is already serving some routes, and
we would like to add authentication.

### Create an OAuth Client

First, we need to register an OAuth client.
The Tapis [documentation](https://tapis.readthedocs.io/en/latest/technical/authentication.html#oauth-clients)
 contains detailed instructions, but here's a simple curl command you can use:
 
 ```
curl -H "X-Tapis-Token: $JWT" -H "Content-type: application/json" -d '{"client_id": "my_app", "callback_url": "http://localhost:5000/oauth2/callback", "client_key": "myapp4ever"}' https://icicle.tapis.io/v3/oauth2/clients
```

 Notes: 
 
 1) You need an access token (the $JWT variable) to register an OAuth client; consider using the token webapp for your ICICLE tenant (e.g., https://icicleai.tapis.io/v3/oauth2/webapp) if you need to generate a token.

2) You need to register a callback URL for your app. This is the domain your app will respond to; for local development, that is likely  "localhost", but for production, you will use a different domain. So, you will likely require a different OAuth client for local dev vs production. 


### Create a `config.yaml `
Next, we create a config file. The file name and location can be anything; by default `iciflaskn` looks for a config file at the path `/app/config.yaml`, but you can configure the path by exporting APP_CONFIG_PATH set to the path to your file.

```
# Your client credentials
client_id: your_client_id
client_key: your_client_key

# The Tapis base URL and tenant id
tapis_base_url: https://icicleai.tapis.io
tenant: icicleai

# The base URL that you app isserved on; this needs to match what was registered with the  OAuth client
the catalog to a public URL. 
app_base_url: http://localhost:5000
```

### Import and Register the BluePrint

With two lines of code, we can now add full authentication functionality to our app:

```
# app.py

app = Flask(__name__)

from iciflaskn import icicle_flaskn
app.register_blueprint(icicle_flaskn)
```

This code registers 3 new routes: login, logout and callback, for handling the authentication flow.

The `auth` module provides convenience functions for working with authentication data:

```
from iciflaskn import auth

@app.route('/', methods=['GET'])
def hello():
    """
    Some route that requires authentication.
    """
    authenticated, user, roles = auth.is_logged_in()
    if not authenticated:
        message = 'Please login to continue'
        # . . .
    else:
        message = f"Hello, {user}"
        # . . .
```

The `iciflaskn.auth.is_logged_in()` returns the following:

  * `authenticated` (bool) -- Whether the user is authenticated in the session.
  * `user` (Optional(str)) -- Unique username for the authenticated user, or None.
  * `roles` (Optional([str])) -- List of role ids occupied by the authenticated user, or None.


# Acknowledgements

*This work has been funded by grants from the National Science Foundation, including the ICICLE AI Institute (OAC 2112606) and Tapis (OAC 1931439).*