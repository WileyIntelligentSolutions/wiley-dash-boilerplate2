import os

# Set to 'private' if you want to add a login screen to your app
# You can choose who can view the app in your list of files
# at <your-plotly-server>/organize.
# Set to 'public' if you want your app to be accessible to
# anyone who has access to your Plotly server on your network without
# a login screen.
# Set to 'secret' if you want to add a login screen, but allow it
# to be bypassed by using a secret "share_key" parameter.
DASH_APP_PRIVACY = 'public'

# Set this to True to require the user to authenticate via
# plotly-on-premises.  Caution: If set this to False your app will
# be open to the entire world !!
AUTHENTICATE = False

# Enter the dash app name here:
DASH_APP_NAME = 'boilerplate2'

# Set this to True if you are running the app locally.
# Set to False before deploying
SERVE_LOCALLY = True