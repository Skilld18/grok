pip install wikipedia
gzip < grok.1 > grok.1.gz
cp grok.1.gz /usr/share/man/man1
mandb

chmod 755 grok.py
cp grok.py /usr/bin/grok
