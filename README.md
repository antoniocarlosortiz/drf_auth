# drf_auth

##App usage guide using httpie (CURL substitute)
###Register a user
`http --json POST :8000/users/ email=a@c.com first_name=a last_name=c password=ac`
* this will send an email which make is_active field of user, True.

###Create a token for user
`http :8000/users/sign-in/ email=a@c.com password=ac`
* only works if user is active

###List users (without auth token)
`http :8000/users/`

###List users (with auth token)
`http :8000/users/ 'Authorization:Token 03abfb30d9f8960090951ac70c1b4defd0307bb9'`

###Detail users (without auth token)
`http :8000/users/1/`

###Detail users (with auth token)
`http :8000/users/1/ 'Authorization:Token 03abfb30d9f8960090951ac70c1b4defd0307bb9'`

###Change password
`http :8000/users/change-password/ password=hello 'Authorization:Token 6d9a181e9936ac6a75afc20e9c59a8c27cac37af'`

##Other Notes
* edit `ADMIN_HOST` on `settings.py` depending on your choice of dev server address.
* Chose not to use viewsets and routers because there are too many endpoints on the app that I cant use it on.
