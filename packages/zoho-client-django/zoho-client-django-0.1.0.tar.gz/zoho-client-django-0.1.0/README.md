# zoho-client-django

# setup

generate the refresh token

fetch the auth code:

scope:
ZohoCRM.modules.ALL,ZohoCRM.settings.ALL,ZohoCRM.users.ALL,ZohoCRM.bulk.ALL,ZohoCRM.notifications.ALL

choose either production or sandbox
press generate
copy the code

```
from zoho_client.zoho import ZohoClient

code = "1000.12c557408797e20c8432216dca0bbb5f.f1896d4f9e2329136806637798859a99"
ZohoClient().fetch_tokens(code)
'1000.03b32b6490d8573e242664710bbc4f2c.e009198b6ab4b89013485657409e4913'
```
