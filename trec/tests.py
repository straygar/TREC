from django.test import TestCase
from django.core.files import File
import datetime
from util import trec

from main.models import Run, Task, Track, Genre, Researcher, RunFile, User

class TrecEvalTests(TestCase):
    def test_getRating(self):
        judgement_file = File(open("qrels/aq.trec2005.qrels"))
        result_file = File(open("qrels/aq.trec.bm25.0.50.res"))
        results = trec.getRating("qrels/aq.trec2005.qrels", "qrels/aq.trec.bm25.0.50.res")
        self.assertEqual(results["P_10"], 0.3469)
        self.assertEqual(results["P_20"], 0.3367)
        self.assertEqual(results["map"], 0.1764)


class GenreModelTests(TestCase):
    def create_genre(self, title="testGenre"):
        return Genre.objects.create(title=title)

    def test_genre_creation(self):
        g = self.create_genre()
        self.assertTrue(isinstance(g, Genre))
        self.assertEqual(g.__unicode__(),"testGenre")

class ResearcherModelTests(TestCase):
    def create_researcher(self, display_name = "tester", organization = "testUni",
                          website = "www.google.com"):
        return Researcher.objects.create(display_name=display_name,
                                         organization=organization, website=website)

    def test_researcher_creation(self):
        r = self.create_researcher()
        self.assertTrue(isinstance(r, Researcher))
        self.assertEqual(r.__unicode__(),"tester")
        self.assertEqual(r.organization, "testUni")
        self.assertEqual(r.website, "www.google.com")

class TrackModelTests(TestCase):
    def create_track(self, title="testTrack", track_url="www.google.com",
                     description="test"):
        genre = Genre.objects.create(title="testGenre2")
        return Track.objects.create(title=title, track_url=track_url,
                                    description=description, genre=genre)

    def test_track_creation(self):
        tr = self.create_track()
        self.assertTrue(isinstance(tr,Track))
        self.assertEqual(tr.__unicode__(), "testTrack")
        self.assertEqual(tr.track_url, "www.google.com")
        self.assertEqual(tr.description, "test")
        self.assertEqual(tr.genre.__unicode__(), "testGenre2")

class TaskModelTests(TestCase):
    def create_task(self, title="testTask", task_url="www.google.com",
                    description="test", year=2016):
         genre = Genre.objects.create(title="testGenre3")
         track = Track.objects.create(title="test", track_url="testURL",
                                    description="test", genre=genre)
         judgement_file= File(open("qrels/aq.trec2005.qrels"))
         return Task.objects.create(title=title, task_url=task_url,
                                    description=description, year=year,
                                    judgement_file=judgement_file, track=track)

    def test_task_creation(self):
        ta = self.create_task()
        self.assertTrue(isinstance(ta,Task))
        self.assertEqual(ta.__unicode__(), "testTask")
        self.assertEqual(ta.task_url, "www.google.com")
        self.assertEqual(ta.description, "test")
        self.assertEqual(ta.year, 2016)
        self.assertEqual(ta.track.__unicode__(),"test")

class RunFileModelTests(TestCase):
    def create_runfile(self, result_file=File(open("qrels/aq.trec.bm25.0.50.res"))):
        return RunFile.objects.create(result_file=result_file)

    def test_runfile_creation(self):
         rf = self.create_runfile()
         test_file=File(open("qrels/aq.trec.bm25.0.50.res"))
         self.assertTrue(isinstance(rf,RunFile))
         self.assertTrue(rf.result_file, test_file)

class RunModelTests(TestCase):

     def create_run(self,name,description,run_type,query_type,feedback_type,researcher,task,result_file,map,p10,p20):

        r = Run.objects.get_or_create(name=name,description=description,run_type=run_type,query_type=query_type,
                                      feedback_type=feedback_type,researcher=researcher,task=task,result_file=result_file,
                                      map=map,p10=p10,p20=p20)[0]
        return r

     def test_run_creation(self):

         run_file = RunFile.objects.create(result_file=File(open('qrels/aq.trec.bm25.0.50.res')))
         judgement_file= File(open("qrels/aq.trec2005.qrels"))
         genre = Genre.objects.create(title="testGenre3")
         track = Track.objects.create(title="test", track_url="testURL",description="test", genre=genre)
         task = Task.objects.create(title="test", task_url="test",description="test", year=2016,judgement_file=judgement_file, track=track)
         u = User.objects.create_user(username = "testUser",email = "test",password= "test")
         researcher = Researcher.objects.create(user=u,display_name="testUser",website="test",organization="test")

         testRun = self.create_run(name='test',description='test run',run_type='AU',query_type='AF',feedback_type='RF',
                              researcher=researcher,task=task,result_file=run_file,map=0.1,p10=0.3,p20=0.4)

         self.assertTrue(isinstance(testRun,Run))
         self.assertEqual(testRun.name, 'test')
         self.assertEqual(testRun.description, 'test run')
         self.assertEqual(testRun.run_type, 'AU')
         self.assertEqual(testRun.query_type, 'AF')
         self.assertEqual(testRun.feedback_type, 'RF')
         self.assertEqual(testRun.researcher.__unicode__(), "testUser")
         self.assertEqual(testRun.task, task)
         self.assertEqual(testRun.result_file, run_file)
         self.assertEqual(testRun.map, 0.1)
         self.assertEqual(testRun.p10,0.3)
         self.assertEqual(testRun.p20,0.4)

