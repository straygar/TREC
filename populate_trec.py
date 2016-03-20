import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','trec.settings')

import django
django.setup()

from main.models import Researcher, Genre, Track, Task, Run, User, RunFile
from django.core.files import File
from django.core.files.images import ImageFile
from django.contrib.staticfiles.templatetags.staticfiles import static

def populate():

    def addUser(username,email,password,display_name,website,organization,profile_pic):
        u = User.objects.create_user(username,email,password)
        up = Researcher.objects.get_or_create(user=u,display_name=display_name,website=website,organization=organization)[0]
        pic = ImageFile(open(profile_pic,"r"))
        up.profile_picture.save("jill.jpg",pic,save=True)
        return up

    # def addRunFile(result_file):
    #     file = File(open(result_file,"r"))
    #     r = RunFile.objects.get_or_create()
    #     r.result_file.save("aq.trec.bm25.0.50.res",r,save=True)

    def addGenre(title):
        g = Genre.objects.get_or_create(title=title)[0]
        return g

    def addTrack(title,track_url,description,genre):
        track = Track.objects.get_or_create(title=title,description=description,genre=genre,track_url=track_url)[0]
        return track

    def addTask(track,title,description,task_url,year):
        task = Task.objects.get_or_create(title=title, track=track, description = description, task_url=task_url,year=year)[0]
        return task

    def addRun(name,description,run_type,query_type,feedback_type,researcher,task,result_file_id,map,p10,p20):
        r = Run.objects.get_or_create(name=name,description=description,run_type=run_type,query_type=query_type,
                                      feedback_type=feedback_type,researcher=researcher,task=task,result_file_id=result_file_id,
                                      map=map,p10=p10,p20=p20)[0]
        return r
    #need to add in pictures!
    jill_researcher = addUser(username='Jill2',
                               email='jill@gmail.com',
                               password='jill',
                               website='http://jsonmyfeet@tumblr.com',
                               display_name='Jill',
                               organization = 'University of Glasgow',
                               profile_pic='jill.jpg')

    jen_researcher = addUser(username='Jen2',
                               email='jen@gmail.com',
                               password='jen',
                               website='http://allthispurple@tumblr.com',
                               display_name='Jen',
                               organization = 'University of Strathclyde',
                               profile_pic='jill.jpg')

    bob_researcher = addUser(username='Bob2',
                               email='bob@gmail.com',
                               password='bob',
                               website='http://youknowit@tumblr.com',
                               display_name='Bob',
                               organization = 'University of Glasgow',
                               profile_pic='jill.jpg')

    news_genre = addGenre('News')

    # aq_run_file = addRunFile('aq.trec.bm25.0.50.res')

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
                          feedback_type='RF',
                          researcher=bob_researcher,
                          task=robust_task,
                          result_file_id=1,
                          map=0.1,
                          p10=0.3,
                          p20=0.4)


if __name__ == '__main__':
    populate()

