To Set Up tFeed:

IMPORTANT: Only the user bob (password bob) is an "Admin", so bob is the only one that can edit tasks, tracks... All the other users are not
Please see whats_new.txt to see what we have added since the day of our presentation.

- Git clone the repo.
- Install requirements: pip install -r reqs.txt
- Compile trec_eval: simply download the trec_eval.tar.gz from https://github.com/leifos/wad/blob/master/projects/trec/trec_eval_latest.tar.gz -- then extract it, cd into its directory and run the command "make". You will get the output file, probably called trec_eval. The one we have on our root is for X64 OS X. You might have to chmod +x it
- Copy this file onto the root of our web app (where manage.py is)
- Create a fresh database: python manage.py migrate and python manage.py makemigrations
    OR use our own db.sqlite3 -- it is a "clean" DB with only the information on the population script

- If you opt for the first option, then you will need to run the population script: python populate_trec.py
- Take into account that for the population script to work you will need to have the trec_eval executable working.


Developed by:

Maria-Luiza Koleva - 2127555k - mKoleva
Shaun Macdonald - 1005872M - Torquoal
Aigars Reiters - 2148261R - nastyguard
Pablo Arteaga - 2144641A  -- I got commits with 3 different usernames, sorry about that. pablo96@gmail.com , pablo@pabloarteaga.es and another one without email address. All of them have "Pablo Arteaga" as the commiter's name

The form is in the root folder as Participation-form.jpg