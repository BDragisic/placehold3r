# placehold3r

A python script to detect default pages on a website. It will scrape every internal link present on the page you provide on the command line and search for default pages.

Currently can detect the Apache2 and Nginx default pages along with Microsoft IIS version 7 and 10. 

It will also search for any pages that have Lorem Ipsum present.


### Usage

##### Requirements
```
pip3 install -r requirements.txt
```

##### Execute
```
python3 placehold3r.py SITE.com
```
