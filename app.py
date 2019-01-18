import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable
import flask
import redis
import time
import base64
import os
import config
from slogger import slogger
from auth import auth
from celery.result import AsyncResult
from tasks import query

# Add your imports here for the UI only:
from urllib.parse import quote
import json
from flask import send_file
import io
import flask
import boto3
import sys

# Don't touch this:
app = dash.Dash(__name__)
if config.AUTHENTICATE:
    auth(app)
server = app.server
app.config.supress_callback_exceptions = True
app.title = config.DASH_APP_NAME

# Don't touch this:
r = redis.StrictRedis.from_url(os.environ['REDIS_URL'])
app.scripts.config.serve_locally = config.SERVE_LOCALLY
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'
assets_folder = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'assets')
reports_folder = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'reports')

#      __                ___
#     / /  ___  ___ ____/ (_)__  ___ _
#    / /__/ _ \/ _ `/ _  / / _ \/ _ `/ _ _
#   /____/\___/\_,_/\_,_/_/_//_/\_, (_|_|_)
#                              /___/
#   Loading ...
#       - collect all data required to start the app e.g. for large menu selections
#       - can be from static files in the deployment or on S3, database queries, health checks, etc...
#       - note that any data loaded here can only be refreshed by re-deploying the app
from loading import get_menu_options
menu_options = get_menu_options()

# Import graphics files from assets
# (recommended method is to load images as base64 strings)
wiley_logo = base64.b64encode(
    open(os.path.join(assets_folder, 'wiley.png'), 'rb').read())
team_logo = base64.b64encode(
    open(os.path.join(assets_folder, 'Intelligent-Solutions-icon.png'), 'rb').read())
spinner = base64.b64encode(
    open(os.path.join(assets_folder, 'spinner.gif'), 'rb').read())

#      ___               __                       __
#     / _ | ___  ___    / /  ___ ___ _____  __ __/ /_
#    / __ |/ _ \/ _ \  / /__/ _ `/ // / _ \/ // / __/
#   /_/ |_/ .__/ .__/ /____/\_,_/\_, /\___/\_,_/\__/
#        /_/  /_/               /___/
#
#   App layout
#   Customize this however you like but be careful not to break the callbacks

# Declare any markdown text here as it becomes difficult to read if defined inside app.layout
# Change these to anything you want:
md_description = "This is the new Boilerplate Dash App from Wiley Intelligent Solutions."
md_help = "Select a year and click submit to see some random data about cats."

# Layout is defined in this dict:
app.layout = html.Div([
    # Insert team logo top-right
    html.Div(
        html.Img(id='robot-logo',
                 src='data:image/gif;base64,{}'.format(team_logo.decode()),
                 style={'width': '100px'}), style={'display': 'inline',
                                                   'float': 'right',
                                                   'vertical-align': 'middle'}
    ),
    # App name and description
    # Insert the app name here:
    html.H1(children='Boilerplate2'),
    dcc.Markdown(md_description),
    # Invisible divs to safely store the current task-id and task-status 
    # Don't touch this, and don't put it below a DataTable:
    # (if debugging, you can use these to make the divs visible)                     
    html.Div(id='task-id', children='none',
             style={'display': 'none'}),                
    html.Div(id='task-status', children='task-status',
             style={'display': 'none'}),                
    # This is an Interval div and determines the initial app refresh rate.
    # The current settings should be ok for all applications.
    # Don't put it below a Data Table:
    dcc.Interval(
        id='task-interval',
        interval=250,  # in milliseconds
        n_intervals=0),
    #     ____                      ____
    #    / __ \__ _____ ______ __  / __/__  ______ _
    #   / /_/ / // / -_) __/ // / / _// _ \/ __/  ' \
    #   \___\_\_,_/\__/_/  \_, / /_/  \___/_/ /_/_/_/
    #                  /___/
    #   Query form containing:
    #       - help
    #       - drop-down menu
    #       - spinner (hidden unless a task is running)
    #       - submit button
    # Display help:
    html.Br(),
    dcc.Markdown(md_help),
    # User input
    html.H6(children='Year'),
    dcc.Dropdown(
        id='year_menu',
        options=menu_options
    ),
    # Submit button
    html.Br(),
    html.Button(id='submit', type='submit', children='Submit'),
    html.Br(),
    html.Br(),
    # This div contains the spinner and is hidden unless a task is running
    # Do not touch:
    html.Div(
        id='spinner',
        children=[html.Img(src='data:image/gif;base64,{}'
                           .format(spinner.decode())),
                  "Don't go away - we're working on your results"],
        style={'display': 'none'}
    ),
    #      ___               ____        ____
    #     / _ \___ ___ __ __/ / /____   / __/__  ______ _
    #    / , _/ -_|_-</ // / / __(_-<  / _// _ \/ __/  ' \
    #   /_/|_|\__/___/\_,_/_/\__/___/ /_/  \___/_/ /_/_/_/
    #   Results form placeholder
    #       Intially nothing is displayed.  The form itselfs is defined when
    #       results are returned from the query in the get_results function
    #       below.
    html.Div(id='results-form', children=[]),
    html.Br(),
    #       ______            __           
    #      / ____/___  ____  / /____  _____
    #     / /_  / __ \/ __ \/ __/ _ \/ ___/
    #    / __/ / /_/ / /_/ / /_/  __/ /    
    #   /_/    \____/\____/\__/\___/_/     
    #   Footer                                   
    #       Footer with corporate branding
    dcc.Markdown(children="***"),
    html.Div(children='Brought to you by Wiley Intelligent Solutions'),
    html.Div([
        html.Div(children='Copyright © 2018 by John Wiley & Sons, Inc., \
                 or related companies. All rights reserved.',
                 style={'text-align': 'left',
                        'display': 'inline-block',
                        'vertical-align': 'middle'}),
    ], style={'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div(
        html.Img(id='wiley-logo',
                 src='data:image/png;base64,{}'.format(wiley_logo.decode()),
                 style={'width': '150px'}),
        style={'display': 'inline',
               'float': 'right',
               'vertical-align': 'middle'}),
], className="container")

#     _____     ______            __
#    / ___/__ _/ / / /  ___ _____/ /__ ___
#   / /__/ _ `/ / / _ \/ _ `/ __/  '_/(_-<
#   \___/\_,_/_/_/_.__/\_,_/\__/_/\_\/___/
#
#   Callbacks
#       - callbacks enable the interactivity of the app
@app.callback(Output('task-id', 'children'),
              [Input('submit', 'n_clicks')],
              [State('task-id', 'children'),     # <--- task-id must always be first
               State('year_menu', 'value')])
def start_task_callback(n_clicks, task_id, year_choice):    
    """This callback is triggered by  clicking the submit button click event.  If the button was
    really pressed (as opposed to being self-triggered when the app is launch) it checks if the
    user input is valid then puts the query on the Celery queue.  Finally it returns the celery 
    task ID to the invisible div called 'task-id'.
    """
    # Don't touch this:
    slogger('start_task_callback', 'n_clicks={}, task_id={}, year_choice={}'.format(n_clicks, task_id, year_choice))
    if n_clicks is None or n_clicks == 0:
        return 'none'
    
    # Validate the user input.  If invalid return 'none' to task-id and don't queue anything
    # For our dummy search we just need to make sure the user has selected a year:
    if year_choice is None:
        # invalid input
        slogger('start_task_callback', 'user has not selected any year')
        return 'none'
    else:
        # valid, so proceed
        slogger('start_task_callback', 'year_choice={}'.format(year_choice))

    # Put search function in the queue and return task id
    # (arguments must always be passed as a list)
    slogger('start_task_callback', 'query accepted and applying to Celery')
    task = query.apply_async([year_choice])
    # don't touch this:
    slogger('start_Task_callback', 'query is on Celery, task-id={}'.format(task.id))
    return str(task.id)


# Don't touch this:
@app.callback(Output('task-interval', 'interval'),
              [Input('task-id', 'children'),
               Input('task-status', 'children')])
def toggle_interval_speed(task_id, task_status):
    """This callback is triggered by changes in task-id and task-status divs.  It switches the 
    page refresh interval to fast if a task is running, or slow (24 hours) if a task is pending or
    complete."""
    if task_id == 'none':
        slogger('toggle_interval_speed', 'no task-id --> slow refresh')
        return 24*60*60*1000
    if task_id != 'none' and (task_status == 'SUCCESS'
                              or task_status == 'FAILURE'):
        slogger('toggle_interval_speed', 'task-id is {} and status is {} --> slow refresh'.format(task_id, task_status))
        return 60*60*1000
    else:
        slogger('toggle_interval_speed', 'task-id is {} and status is {} --> fast refresh'.format(task_id, task_status))
        return 1000


# Don't touch this:
@app.callback(Output('spinner', 'style'),
              [Input('task-interval', 'n_intervals'),
               Input('task-status', 'children')])
def show_hide_spinner(n_intervals, task_status):
    """This callback is triggered by then Interval clock and checks the task progress
    via the invisible div 'task-status'.  If a task is running it will show the spinner,
    otherwise it will be hidden."""
    if task_status == 'PROGRESS':
        slogger('show_hide_spinner', 'show spinner')
        return None
    else:
        slogger('show_hide_spinner', 'hide spinner because task_status={}'.format(task_status))
        return {'display': 'none'}


# Don't touch this:
@app.callback(Output('task-status', 'children'),
              [Input('task-interval', 'n_intervals'),
               Input('task-id', 'children')])
def update_task_status(n_intervals, task_id):
    """This callback is triggered by the Interval clock and task-id .  It checks the task
    status in Celery and returns the status to an invisible div"""
    return str(AsyncResult(task_id).state)


@app.callback(Output('results-form', 'children'),
              [Input('task-status', 'children')],
              [State('task-id', 'children')])
def get_results(task_status, task_id):
    """This callback is triggered by task-status.  It checks the task status, and if the status 
    is 'SUCCESS' it retrieves results, defines the results form and returns it, otherwise it 
    results [] so that nothing is displayed"""
    status = str(AsyncResult(task_id).state)
    if status == 'SUCCESS':
        # Fetch results from Celery and forget the task
        slogger('get_results', 'retrieve results for task-id {} from Celery'.format(task_id))
        result = AsyncResult(task_id).result    # fetch results
        forget = AsyncResult(task_id).forget()  # delete from Celery
        # Return the populated DataTable
        return [html.Br(),
                html.A('Download results (Excel)',
                href="{}/download_excel/{}".format(config.DASH_APP_NAME, task_id)),
                html.Br(),
                dcc.Markdown('Displaying 25 rows at a time'),
                DataTable(id='results_table',
                            columns=[{'id': 'name', 'name': 'Name'},
                                        {'id': 'town', 'name': 'Town'},
                                        {'id': 'chipcode', 'name': 'Chipcode'},
                                        {'id': 'brand', 'name': 'Favourite Brand'},
                                        {'id': 'weight', 'name': 'Weight (grams)'},
                                        {'id': 'age', 'name': 'Age (years)'}], 
                            data=result,
                            sorting=True,
                            virtualization=True,
                            pagination_mode='fe',
                            pagination_settings={'current_page': 0,
                                                'page_size': 25})]
    else:
        # don't display any results
        return []


#      ___                  __             __  ____             __
#     / _ \___ _    _____  / /__  ___ ____/ / / __/_ _________ / /
#    / // / _ \ |/|/ / _ \/ / _ \/ _ `/ _  / / _/ \ \ / __/ -_) / 
#   /____/\___/__,__/_//_/_/\___/\_,_/\_,_/ /___//_\_\\__/\__/_/  
#
#   Download Excel with some Flask magikkk                                                              
#
@app.server.route('/download_excel/<task_id>')
def download_excel(task_id):
    # Retrieve the results Excel file from S3 and send to user as Flask attachment
    bucket_name = 'wiley-dse-appdata-bucket'
    excel_filename = '{}.xlsx'.format(task_id)
    s3_excel_key = '{}/{}'.format(config.DASH_APP_NAME, excel_filename)
    slogger('download_excel', 'retrieve object {} from S3 bucket {}'.format(s3_excel_key, bucket_name))
    client = boto3.client('s3', 
                                aws_access_key_id=os.environ['S3_ACCESS_KEY_ID'], 
                                aws_secret_access_key=os.environ['S3_SECRET_ACCESS_KEY'])
    excel_file = client.get_object(Bucket=bucket_name, Key=s3_excel_key)['Body']
    return send_file(excel_file,
                    attachment_filename='ExpertFinder.xlsx',
                    as_attachment=True)


# don't touch this:
app.css.append_css({
    'external_url': ([
        'https://codepen.io/chriddyp/pen/dZVMbK.css'
    ])
})

# don't touch this:
if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

# don't touch this:
if __name__ == '__main__':
    app.run_server()