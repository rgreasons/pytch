## Pytch - tools for Pitchfork web scraping.

this repo contains tools and files related to my work scraping [Pitchfork](www.pitchfork.com) music reviews in Python.

The September 2018 update of this repository is largely a refactor of my previous work, updated to follow the suggestions of [David Eads](http://www.recoveredfactory.net/) from his [blog post for the NPR Tech Blog](http://blog.apps.npr.org/2016/06/17/scraping-tips.html).

Below are the steps to replicate the scraping yourself. I recommend doing so in a python virtual environment since these scripts use pretty common packages (csvkit, requests) that may create api version conflicts in other projects if installed into your root python folder.

1. Run ```python reviewlist.py```, which will create a csv in the folder named reviewlist.csv
2. Run ```csvcut -c 1 reviewlist.csv | parallel ./PitchforkReview.py {} > pitchforkreviews.csv```, which will create a csv file in the folder named pitchforkreviews.csv