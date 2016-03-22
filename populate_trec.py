import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','trec.settings')

import django
django.setup()

from main.models import Researcher, Genre, Track, Task, Run, User, RunFile
from django.core.files import File

from util import trec

def populate():

    def addUser(username,email,password,display_name,website,organization):
        u = User.objects.create_user(username,email,password)
        up = Researcher.objects.get_or_create(user=u,display_name=display_name,website=website,organization=organization)[0]

        return up

    def addRunFile(result_file):
        file = File(open(result_file,"r"))
        r = RunFile(result_file=file)
        r.save()
        return r

    def addGenre(title):
        g = Genre.objects.get_or_create(title=title)[0]
        return g

    def addTrack(title,track_url,description,genre):
        track = Track.objects.get_or_create(title=title,description=description,genre=genre,track_url=track_url)[0]
        return track

    def addTask(track,title,description,task_url,year,judgement_file):
        task = Task.objects.get_or_create(title=title, track=track, description = description, task_url=task_url,year=year)[0]
        file = File(open(judgement_file,"r"))
        task.judgement_file.save(judgement_file,file,save=True)
        return task

    def addRun(name,description,run_type,query_type,feedback_type,researcher,task,run_file,judgement_file,result_file):
        results = trec.getRating(judgement_file,result_file)
        r = Run.objects.get_or_create(name=name,description=description,run_type=run_type,query_type=query_type,
                                      feedback_type=feedback_type,researcher=researcher,task=task,
                                      map=results['map'],p10=results['P_10'],p20=results['P_20'],result_file=run_file)[0]
        return r
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

    web_genre = addGenre('Web')

    aq_run_file = addRunFile(result_file='aq.trec.bm25.0.50.res')

    ap_run_file = addRunFile(result_file='ap.trec.bm25.0.70.res')

    ap1_run_file = addRunFile(result_file='ap.trec.bm25.0.50.res')

    ap2_run_file = addRunFile(result_file = 'ap.trec.pl2.2.00.res')

    ap3_run_file = addRunFile(result_file = 'ap.trec.pl2.5.00.res')

    aq1_run_file=addRunFile(result_file='aq.trec.bm25.0.70.res')

    aq2_run_file=addRunFile(result_file='aq.trec.pl2.2.00.res')

    aq3_run_file=addRunFile(result_file='aq.trec.pl2.5.00.res')

    dg_run_file=addRunFile(result_file='dg.trec.bm25.0.50.res')

    dg1_run_file=addRunFile(result_file='dg.trec.bm25.0.70.res')

    dg2_run_file=addRunFile(result_file='dg.trec.pl2.2.00.res')



    robust_track = addTrack(title='Robust2004',
                               track_url='http://trec.nist.gov/data/t13_robust.html',
                               description = 'News Retrieval',
                               genre=news_genre)

    million_query_track = addTrack(title='Million Query',
                               track_url='http://ciir.cs.umass.edu/research/million/',
                               description = 'Million Query',
                               genre=web_genre)

    terabyte_track = addTrack(title='Terabyte',
                               track_url=' http://www-nlpir.nist.gov/projects/terabyte/',
                               description = 'Terabyte',
                               genre=web_genre)

    ap_news_track = addTrack(title='APNews',
                               track_url=' http://www-nlpir.nist.gov/projects/terabyte/',
                               description = 'APNews',
                               genre=news_genre)


    robust_task = addTask(track=robust_track,
                             title = 'Robust2005',
                             description='Ad Hoc Topic Retrieval',
                             task_url='http://trec.nist.gov/data/t14_robust.html',
                             year=2005,
                             judgement_file='aq.trec2005.qrels'
                             )

    web_task = addTask(track=million_query_track,
                             title = 'Web2005',
                             description='Ad Hoc Topic Retrieval',
                             task_url='http://www-nlpir.nist.gov/projects/terabyte/',
                             year=2005,
                             judgement_file='dg.trec.qrels'
                             )
    news_task = addTask(track=ap_news_track,
                        title = 'APNews',
                        description='Ad Hoc Topic Retrieval',
                        task_url='http://www-nlpir.nist.gov/projects/terabyte/',
                        year=2005,
                        judgement_file='ap.trec.qrels'
                        )


    first_run = addRun(name='first',
                          description='first run',
                          run_type='AU',
                          query_type='AF',
                          feedback_type='RF',
                          researcher=jill_researcher,
                          task=robust_task,
                          run_file=aq_run_file,
                          result_file='aq.trec.bm25.0.50.res',
                          judgement_file ='aq.trec2005.qrels' )
    second_run = addRun(name='second',
                          description='second',
                          run_type='MA',
                          query_type='TD',
                          feedback_type='RF',
                          researcher=jill_researcher,
                          task=news_task,
                          run_file=ap_run_file,
                          result_file = 'ap.trec.bm25.0.70.res',
                          judgement_file = 'ap.trec.qrels')
    third_run = addRun(name='third',
                          description='third',
                          run_type='MA',
                          query_type='TO',
                          feedback_type='RF',
                          researcher=jill_researcher,
                          task=news_task,
                          run_file=ap1_run_file,
                          result_file = 'ap.trec.bm25.0.50.res',
                          judgement_file='ap.trec.qrels')
    forth_run = addRun(name='forth',
                          description='forth',
                          run_type='AU',
                          query_type='TO',
                          feedback_type='RF',
                          researcher=jill_researcher,
                          task=news_task,
                          run_file=ap2_run_file,
                          result_file = 'ap.trec.pl2.2.00.res',
                          judgement_file = 'ap.trec.qrels')
    fifth_run = addRun(name='fifth',
                          description='fifth',
                          run_type='MA',
                          query_type='TD',
                          feedback_type='RF',
                          researcher=jill_researcher,
                          task=news_task,
                          run_file=ap3_run_file,
                          result_file = 'ap.trec.pl2.5.00.res',
                          judgement_file='ap.trec.qrels')
    sixth_run = addRun(name='sixth',
                          description='sixth',
                          run_type='MA',
                          query_type='TD',
                          feedback_type='RF',
                          researcher=bob_researcher,
                          task=robust_task,
                          run_file=aq1_run_file,
                          result_file = 'aq.trec.bm25.0.70.res',
                          judgement_file ='aq.trec2005.qrels' )
    seventh_run = addRun(name='seventh',
                          description='seventh',
                          run_type='AU',
                          query_type='TD',
                          feedback_type='RF',
                          researcher=jen_researcher,
                          task=robust_task,
                          run_file=aq2_run_file,
                          result_file = 'aq.trec.pl2.2.00.res',
                          judgement_file ='aq.trec2005.qrels' )
    eight_run = addRun(name='eight',
                          description='eight',
                          run_type='MA',
                          query_type='TO',
                          feedback_type='RF',
                          researcher=jen_researcher,
                          task=robust_task,
                          run_file=aq3_run_file,
                          result_file = 'aq.trec.pl2.5.00.res',
                          judgement_file ='aq.trec2005.qrels' )
    ninth_run = addRun(name='ninth',
                          description='ninth',
                          run_type='AU',
                          query_type='TD',
                          feedback_type='RF',
                          researcher=bob_researcher,
                          task=web_task,
                          run_file=dg_run_file,
                          result_file = 'dg.trec.bm25.0.50.res',
                          judgement_file = 'dg.trec.qrels')
    tenth_run = addRun(name='tenth',
                          description='tenth',
                          run_type='MA',
                          query_type='AF',
                          feedback_type='RF',
                          researcher=jen_researcher,
                          task=web_task,
                          run_file=dg1_run_file,
                          result_file = 'dg.trec.bm25.0.70.res',
                          judgement_file = 'dg.trec.qrels')
    eleventh_run = addRun(name='eleventh',
                          description='eleventh',
                          run_type='AU',
                          query_type='AF',
                          feedback_type='RF',
                          researcher=bob_researcher,
                          task=web_task,
                          run_file=dg2_run_file,
                          result_file='dg.trec.pl2.2.00.res',
                          judgement_file = 'dg.trec.qrels')


if __name__ == '__main__':
    populate()

