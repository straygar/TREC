To Set Up tFeed:

Git clone the repo.
Install requirements: pip install -r reqs.txt
Compile trec_eval: simply download the trec_eval.tar.gz from https://github.com/leifos/wad/blob/master/projects/trec/trec_eval_latest.tar.gz -- then extract it, cd into its directory and run the command "make". You will get the output file, probably called trec_eval.
Copy this file onto the root of our web app (where manage.py is)
Create a fresh database: python manage.py migrate and python manage.py makemigrations
    OR use our own db.sqlite3

If you opt for the first option, then you will need to run the population script: python populate_trec.py


Developed by:

Pablo Arteaga - 2144641A
Maria-Luiza Koleva - 2127555k
Shaun Macdonald - 1005872M
Aigars Reiters - 2148261R