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


## Enter your dash domain here:
PLOTLY_DASH_DOMAIN='https://dash-dseplotly.wiley.com'   # never changes

## Don't touch this:
PATH_BASED_ROUTING=True                                 # always true
PLOTLY_SSL_VERIFICATION=True                            # always true

# Before deploying this app remember to add these environment variables
# in Dash settings:
# PLOTLY_DOMAIN
# PLOTLY_API_DOMAIN
# PLOTLY_USERNAME
# PLOTLY_API_KEY
# S3_BUCKET_NAME
# S3_ACCESS_KEY_ID
# S3_SECRET_ACCESS_KEY

# Note: If running locally, make sure to set the following variables
# in .env:
#       REDIS_URL=redis://0.0.0.0:6379
#       APP_URL=http://0.0.0.0:5000
#       PLOTLY_USERNAME=your-plotly-username
#       PLOTLY_API_KEY=your-plotly-api-key
#       PLOTLY_DOMAIN=https://dseplotly.wiley.com
#       PLOTLY_API_DOMAIN=https://dseplotly.wiley.com
#       DASH_DOMAIN_BASE=https://dash-dseplotly.wiley.com
#       PLOTLY_SSL_VERIFICATION=True
#       PATH_BASED_ROUTING=True



