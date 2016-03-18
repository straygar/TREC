import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','trec.settings')

import django
django.setup()

from rango.models import Researcher, Genre, Track, Task, Run

def populate():
    #need to add in pictures!
    jill_researcher = addUser(username='jill',
                               email='jill@gmail.com',
                               password='jill',
                               website='http://jsonmyfeet@tumblr.com',
                               display_name='Jill',
                               organization = 'University of Glasgow')

    jen_researcher = addUser(username='jen',
                               email='jen@gmail.com',
                               password='jen',
                               website='http://allthispurple@tumblr.com',
                               display_name='Jen',
                               organization = 'University of Strathclyde')

    bob_researcher = addUser(username='bob',
                               email='bob@gmail.com',
                               password='bob',
                               website='http://youknowit@tumblr.com',
                               display_name='Bob',
                               organization = 'University of Glasgow')

    news_genre = addGenre('News')

    robust_track = addTrack(title='Robust2004',
                               track_url='http://trec.nist.gov/data/t13_robust.html',
                               description = 'News Retrieval',
                               genre=news_genre)
    #add in file!
    robust_task = addTask(track=robust_track,
                             title = 'Robust2005',
                             description='Ad Hoc Topic Retrieval',
                             task_url='http://trec.nist.gov/data/t14_robust.html',
                             year=2005
                             )

    first_run = addRun(name='first',
                          description='first run ever',
                          run_type='AU',
                          query_type='AF',
                          feedback_type='RF')

    def addUser(username,email,password,display_name,website,organization):
        u = Researcher.objects.get_or_create(username=username,password=password,email=email)
        u.display_name=display_name
        u.website=website
        u.organization=organization
        u.save()
        return u

    def addGenre(title):
        g = Genre.objects.get_or_create(title=title)
        g.save()
        return g

    def addTrack(title,track_url,description,genre):
        track = Track.objects.get_or_create(title=title)
        track.description=description
        track.genre=genre
        track.track_url=track_url
        track.save()
        return track

    def addTask(track,title,description,task_url,year):
        task = Task.objects.get_or_create(title=title)
        task.track=track
        task.description=description
        task.task_url=task_url
        task.year=year
        task.save()
        return task

    def addRun(name,description,run_type,query_type,feedback_type):
        r = Run.objects.get_or_create(name=name)
        r.description=description
        r.run_type=run_type
        r.query_type=query_type
        r.feedback_type=feedback_type
        r.save()
        return r

if __name__ == '__main__':
    populate()

