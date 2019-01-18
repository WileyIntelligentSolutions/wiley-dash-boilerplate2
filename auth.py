import dash_auth
import os
from textwrap import dedent
import urllib3

import config

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file provides an interface to the `plotly_auth` library
# You do not need to edit this file
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def auth(app):
    
    # Configure path-based routing
    if 'DYNO' in os.environ:
        if os.getenv('PATH_BASED_ROUTING'):
            app.config.requests_pathname_prefix = '/{}/'.format(
                config.DASH_APP_NAME
            )


    # Configure private or secret auth
    if config.DASH_APP_PRIVACY in ['private', 'secret']:

        if os.getenv('PLOTLY_SSL_VERIFICATION') == False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # always path-based routing
        APP_URL = '{}/{}'.format(
            os.getenv('PLOTLY_DASH_DOMAIN').strip('/'),
            config.DASH_APP_NAME,
        )

        dash_auth.PlotlyAuth(
            app,
            config.DASH_APP_NAME,
            config.DASH_APP_PRIVACY,
            [APP_URL, 'http://localhost:8050', 'http://127.0.0.1:8050', 'http://0.0.0.0:5000']
        )

