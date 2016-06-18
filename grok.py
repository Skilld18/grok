#!/usr/bin/python
import sys
import wikipedia

if len(sys.argv) ==1:
	print("How to use grok")
	exit(0)


print(wikipedia.summary(sys.argv[1]))
