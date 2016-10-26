#!/usr/bin/python3

import json
import re
import requests
import sys
import time
import webbrowser


def get_data(request_string):
    request_data = requests.get(request_string).json()
    if "parse" not in request_data.keys():
        print("No results found")
        exit(0)
    request_data = request_data['parse']
    # Regexes to pull out most of the html and multiple newlines
    request_data['text']['*'] = re.sub("<[^>]*>", "", str(request_data['text']['*']))
    request_data['text']['*'] = re.sub('\n+', '\n', request_data['text']['*'])
    return request_data


start_time = time.time()

# Searching different wikis
# This is really hit or miss based on different mediawiki versions
wiki = 'https://en.wikipedia.org/w/api.php?'
search_string = ""

if len(sys.argv) == 1:
    print("Enter a topic to search about, Grok will print the wikipedia summary")
    print("-Verbose flag prints whole article")
    print("-Concise flag prints a short summary")
    print("-Search flag searches wikipedia")
    print("-Browser flag opens page in web browser")
    print("-Debug flag prints debug info")
    print("-----USE CASES-----")
    print("$grok <search_string> [flags]")
    print("$grok [flags] <search_string>")
    print("$grok <search_string> [flags] <--other> <wiki_url>")
    print("/nNOTE: search string and flags order does not matter.")
    print("NOTE: when using -o, last argument MUST be the wiki's url.")
    exit(0)

for arg in sys.argv[1:]:
	if arg[0] == '-':
	    arg = arg.lower()
	    # Flags
	    """
	look for flag only if arg is not a search string
	resolving issues with search subject containing '-'
	ex: 'arc-en-ciel'
	last version using 'any' to find flags would have
	seen the -c flag in 'arc-en-ciel'
	    """
	    verbose = arg in ["-v","--verbose"]
	    concise = arg in ["-c","--concise"]
	    search = arg in ["-s","--search"]
	    browser = arg in ["-b","--browser"]
	    debug = arg in ["-d","--debug"]
	    other = arg in ["-o","--other"]

# TODO: get proper sections
length = 250
if verbose:
    length = 100000000
if concise:
    length = 100


# Combine anything that isn't a flag into a search string
# And use last arg as wiki url IF --other is used (last arg won't be in search_string)
if other:
    wiki = sys.argv[-1] #new wiki url
    for arg in sys.argv[1:-1]:
	if arg[0] != '-':
	search_string += arg + "_"
else:
    for arg in sys.argv[1:]:
	if arg[0] != '-':
	search_string += arg + "_"

	

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
            summary = get_data(wiki + '&action=parse&page=' + titles[i] + '&redirects=&format=json')['text']['*']
            print(re.sub('\n', "", summary[:length]))

    if debug:
        print(search_request)
        print("Completed in %s seconds" % (time.time() - start_time))


    index = input('Select the page by pressing a number and then enter: ')
    start_time = time.time()
    if index.isdigit() and 0 <= int(index) < len(titles):
        # This can lead to redundant requests if program had to grab all the search pages
        search_string = titles[int(index)]
    else:
        exit(0)

args = '&action=parse&page=' + search_string + '&redirects=&format=json'
data = get_data(wiki + args)
print(data['title'] + ': ' + data['text']['*'][:length])


if debug:
    print(wiki + args)
    print("Completed in %s seconds" % (time.time() - start_time))
