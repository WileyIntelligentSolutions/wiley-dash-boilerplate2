import pandas as pd
import os
from slogger import slogger
from random import randint
import time

# Add your own imports here and retrieve credentials from env vars to access
# whichever databases, APIs or static files are required by your search

def search(year_choice):
    """The search function

    Runs a dummy search for data about cats.  Replace this with your actual search function which you
    may have already tested and developed in a Jupyter Notebook.

    Args:
        str: Replace with the actual arguments you need for your search
    Returns:
        dict: The results
    """

    slogger('search', 'running search: {}'.format(year_choice))
    
    # Generate between 10 and 50 rows of random cat data
    names = ['Jack', 'Fluffy', 'Popsy', 'Doofus', 'Bobek', 'Zofia', 'Puszek', 'Kitka', 'Einstein', 'Mruchek',
            'Tomek', 'Prezez', 'Miśu', 'Kopernik', 'Łomża']
    towns = ['Wrocław', 'Tarnów', 'Sandomierz', 'Zakopane', 'Sopot', 'Kielce', 'Katowice', 'Szczotkowice',
            'Busko-Zdrój', 'Szczecin']
    brands = ['Whiskers', 'Sheba', 'Felix', 'Applaws', 'Carrefour Whitelabel', 'Tesco Whitelabel', 'Other']
    results = []
    for i in range(0, randint(50, 500)):
        results.append(dict(name=names[randint(0, len(names) - 1)],
                            town=towns[randint(0, len(towns) - 1)],
                            chipcode=randint(100000000, 999999999),
                            brand=brands[randint(0, len(brands) - 1)],
                            weight=randint(20, 50)*100,
                            age=randint(0, 7)))
    # Include a random dwell to make it seem like we actually did something
    time.sleep(randint(2, 8))

    # Return the results - make sure you return an empty dictionary and not None:
    slogger('search', 'return results')
    if results is None:
        return [{}]
    else:
        return results
