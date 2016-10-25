#!/usr/bin/python3

import json
import re
import requests
import sys
import time
import webbrowser


def getData(request_string):
    data = json.loads(requests.get(request_string).text)
    if not "parse" in data.keys():
        print("No results found")
        exit(0)
    data = data['parse']
    # Regex to pull out most of the html
    data['text']['*'] = re.sub("<[^>]*>", "", str(data['text']['*']))
    # Take out multiple newlines
    data['text']['*'] = re.sub('\n+', '\n', data['text']['*'])
    return data


start_time = time.time()

if len(sys.argv) == 1:
    print("Enter a topic to search about, Grok will print the wikipedia summary")
    print("-Verbose flag prints whole article")
    print("-Concise flag prints a short summary")
    print("-Search flag searches wikipedia")
    print("-Browser flag opens page in web browser")
    print("-Debug flag prints debug info")
    exit(0)
else:
    # Flags
    verbose = any("-v" in arg.lower() for arg in sys.argv)
    concise = any("-c" in arg.lower() for arg in sys.argv)
    search = any("-s" in arg.lower() for arg in sys.argv)
    browser = any("-b" in arg.lower() for arg in sys.argv)
    debug = any("-d" in arg.lower() for arg in sys.argv)



    # Combine anything that isn't a flag into a search string
    search_string = ""
    for arg in sys.argv[1:]:
        if arg[0] != '-':
            search_string += arg + "_"

    # Searching different wikis
    # This is really hit or miss based on different mediawiki versions
    wiki = 'https://en.wikipedia.org/w/api.php?'


    if browser:
        webbrowser.open(wiki + 'wiki/' + search_string)
        exit(0)

    if search:
        # Using opensearch because it seems to be more broadly supported
        search_request = wiki + 'action=opensearch&search=' + search_string + '&limit=10&namespace=0'
        data = json.loads(requests.get(search_request).text)
        titles = data[1]
        if len(titles) == 0:
            print("No results found")
            exit(0)

        for i in range(0, len(titles)):
            print(str(i) + ". " + titles[i] + ": ", end='')
            # Some wikis provide snippet summaries with the search and it is much faster than grabbing the page
            if len(data) > 2:
                print(data[2][i])
            else:
                print(re.sub('\n', "", getData(wiki + '&action=parse&page=' + titles[i] + '&redirects=&format=json')['text']['*'][:80]))

        if debug:
            print(search_request)
            print("Completed in %s seconds" % (time.time() - start_time))


        index = input('Select the page by pressing a number and then enter: ')
        start_time = time.time()
        if index.isdigit() and int(index) >= 0 and int(index) < len(titles):
            # This can lead to redundant requests if program had to grab all the search pages
            search_string = titles[int(index)]
        else:
            exit(0)

    args = '&action=parse&page=' + search_string + '&redirects=&format=json'

    data = getData(wiki + args)

    # TODO: get proper sections
    length = 250
    if verbose:
        length = 100000000
    if concise:
        length = 100


    print(data['title'] + ': ' + data['text']['*'][:length])


if debug:
    print(wiki + args)
    print("Completed in %s seconds" % (time.time() - start_time))
