#!/usr/bin/python3

import json
import re
import requests
import sys
import time
import webbrowser

start_time = time.time()

if len(sys.argv) == 0:
    print("Enter a topic to search about, Grok will print the wikipedia summary")
    print("-Verbose flag prints whole article")
    print("-Concise flag prints a short summary")
    print("-Search flag searches wikipedia")
    print("-Browser flag opens page in web browser")
    print("-Debug flag prints debug info")
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
            search_string += arg
    wiki = 'https://en.wikipedia.org/w/'
    # wiki = 'http://crawl.chaosforge.org/'
    api = 'api.php?'
    args = ''


    if browser:
        webbrowser.open(wiki + 'wiki/' + search_string)
    else:
        args += 'format=json&redirects=&prop=extracts'

    # Length of text printed
    if concise:
        args += '&exchars=80'
    elif verbose:
        args += '&explaintext'
    else:
        args += '&exintro'

    if search:
        acopy = wiki + api + args
        acopy += '&action=query&list=search&srsearch=' + search_string + '&srwhat=text'
        dat = json.loads(requests.get(acopy).text)
        data = dat['query']['search']
        for i in range(0, len(data)):
            print(str(i) + ". " + data[i]['title'], end='')
            print(re.sub('<[^>]*>', '', data[i]['snippet']))
        if debug:
            print(acopy)
            print("Completed in %s seconds" % (time.time() - start_time))
        index = input('Select the page by pressing 0-9 and then enter: ')
        if index.isdigit() and int(index) >= 0 and int(index) <=9:
            dat = list(data)[int(index)]
            print(dat['title'] + ': ' + re.sub('<[^>]*>', '', dat['snippet']))
            exit(0)
        else:
            exit(0)
    args += '&action=query&titles=' + search_string


    dat = json.loads(requests.get(wiki + api + args).text)
    print(wiki + api + args)
    dat = dat['query']['pages']
    key = list(dat.keys())[0]
    dat = dat[key]
    print(dat['title'] + ': ' + re.sub('<[^>]*>', '', dat['extract']))

if debug:
    print(wiki + api + args)
    print("Completed in %s seconds" % (time.time() - start_time))
