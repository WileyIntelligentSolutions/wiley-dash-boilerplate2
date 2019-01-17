# All imports needed to run the loading functions
# import ...
from slogger import slogger
import os

# Add any functions you need to load the required data here.
# These could be functions that pull lists of static files
# from the app repo, or from S3, or database queries or whatever.

def get_menu_options():
    """Function to get the menu options

    Runs a dummy search for available years.  Here you could connect to your database and
    fetch a list of unique towns, or count how many records are available etc.

    Args:
        
    Returns:
        [int]: List of years
    """
    slogger('get_menu_options', 'getting available years')
    
    results = [{'label': '2019', 'value': 2019},
                {'label': '2018', 'value': 2018},
                {'label': '2017', 'value': 2017},
                {'label': '2016', 'value': 2016},
                {'label': '2015', 'value': 2015},
                {'label': '2014', 'value': 2014},
                {'label': '2013', 'value': 2013},
                {'label': '2012', 'value': 2012},
                {'label': '2011', 'value': 2011}]
    
    # Return the results
    slogger('get_menu_options', '{} options found'.format(len(results)))
    return results


