# Wiley AHEAD2

This is the new Boilerplate Dash App from Wiley Intelligent Solutions.

## Key features

- Execution of long-running tasks on a Redis database via Celery (no more server timeouts or flashing screens!)
- Display/interrogate results using DataTable
- Download results in Excel format via Amazon S3

## How to customize this app

Instead of starting from scratch, functions to perform tasks (e.g. database queries) can be developed and tested in Jupyter then directly imported into [tasks.py](tasks.py).  You can then create and forms for submitting queries and displaying the results by walking through and adapting [app.py](app.py) as necessary.  Query functions in [tasks.py](tasks.py) are executed in a Celery queue to ensure stability and an up-to-date user experience.  In the case of AHEAD2 the query function is imported from another file, [ahead_search.py](ahead_search.py)

## Running locally

Install [Redis](https://redis.io/) and follow the instructions to make it start automatically

Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

Clone this repo and release it from the original app:

```bash
$ git clone https://github.com/WileyIntelligentSolutions/AHEAD2
$ cd AHEAD2
$ rm -rf .git
```

Create a new environment, activate it and install packages:

```bash
$ cd wiley-boilerplate2
$ conda create -n wiley-boilerplate2
$ source activate wiley-boilerplate2
$ pip install -r requirements.txt
```

We also recommend ensuring that all packages in your new environment are fully up-to-date.  This may take a few minutes though:

```bash
$ pipdate
```

Populate .env with the following:

```bash
REDIS_URL=redis://0.0.0.0:6379
APP_URL=http://0.0.0.0:5000
PLOTLY_USERNAME=your-plotly-username
PLOTLY_API_KEY=your-plotly-api-key
PLOTLY_DOMAIN=https://dseplotly.wiley.com
PLOTLY_API_DOMAIN=https://dseplotly.wiley.com
DASH_DOMAIN_BASE=https://dash-dseplotly.wiley.com
PLOTLY_SSL_VERIFICATION=True
S3_
```

Start the server

```bash
$ heroku local
```

## Deploy to Dash

Update requirements.txt:

```bash
$ pip freeze > requirements.txt
```

Check that requirements.txt contains gunicorn, redis and celery.  If not, add them at the end.  Following standard practice, we will create 2 apps: One production (boilerplate2) and one as a dev environment (boilerplate2-dev)

In the Dash Deployment Server:

Create new Databases called `boilerplate2` and `boilerplate2-dev`

### Deploy Production App

Create a new Dash app called `boilerplate2` and connect it to the `boilerplate2` Redis database.  Follow these instructions to add your SSH credentials and set your `.ssh/config` to allow both pushing of git repos and connection to the dokku client:

https://dash.plot.ly/dash-deployment-server/ssh

In Settings, populate the following environment variables:

```bash
PLOTLY_API_DOMAIN=https://dseplotly.wiley.com
PLOTLY_API_KEY=...
PLOTLY_DOMAIN=https://dseplotly.wiley.com
PLOTLY_USERNAME=...
S3_BUCKET_NAME=... # name of your S3 bucket
S3_ACCESS_KEY_ID=... # credentials for IAM user 'dashapp'
S3_SECRET_ACCESS_KEY=... # ...
```

Deploy:

```bash
$ git push plotly master
```

Scale-up worker:

```bash
$ ssh dokku@dash-dseplotly.wiley.com ps:scale name-of-your-app worker=1
```

The production app should now be online.

## Deploy Dev App

Create a new Dash app called `ahead2-dev` and connect it to `ahead2-dev-redis`. Then follow the above instructions except:

Change the DASH_APP_NAME variable in config.py to `ahead2-dev`

```bash
$ git remote add dev https://your-dash-deployment-server/GIT/ahead2-dev
$ git push dev master
```