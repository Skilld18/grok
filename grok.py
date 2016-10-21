#!/usr/bin/python3
import sys
import webbrowser
import wikipedia


if len(sys.argv) == 1:
    print("Enter a topic to search about, Grok will print the wikipedia summary")
    print("-Verbose flag prints whole article")
    print("-Concise flag prints a short summary")
    print("-Search flag searches wikipedia")
    print("-Browser flag opens page in web browser")
else:
    verbose = any("-v" in arg.lower() for arg in sys.argv)
    concise = any("-c" in arg.lower() for arg in sys.argv)
    search = any("-s" in arg.lower() for arg in sys.argv)
    browser = any("-b" in arg.lower() for arg in sys.argv)

    search_string = ""
    for arg in sys.argv[1:]:
        if arg[0] != '-':
            search_string += arg


    if verbose:
        print(wikipedia.page(search_string))
    elif concise:
        print(wikipedia.summary(search_string, sentences=1))
    elif browser:
        webbrowser.open((wikipedia.page(search_string)).url)
    elif search:
        results = wikipedia.search(search_string)
        for i in range(0, len(results)):
            print(str(i) + " " + results[i])
        print(wikipedia.page(results[int(input("Choose a number and press enter: "))]).summary)
    else:
        print(wikipedia.summary(search_string))

