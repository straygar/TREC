from django.test import TestCase
from django.core.files import File
import datetime

from main.models import Run, Task, Track, Genre, Researcher, RunFile

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
#
# class RunModelTests(TestCase):
#
#     def create_run(self, name="testRun", description="test", run_type="AU",query_type="TO",
#                    feedback_type="NF", map=0.5, p10=0.5, p20=0.5):
#
#         researcher = Researcher.objects.create(display_name="basicHuman",organization="Uni", website="test")
#         result_file = RunFile.objects.create()
#         time = datetime.date.today()
#
#         genre = Genre.objects.create(title="testGenre3")
#         track = Track.objects.create(title="test", track_url="testURL",description="test", genre=genre)
#         task = Task.objects.create(title="test", task_url="test",description=description, year=2016,judgement_file=result_file, track=track)
#
#         return Run.objects.create(name=name, researcher=researcher, datetime = time,
#                                   result_file=result_file, description=description, run_type=run_type,
#                                   query_type=query_type, feedback_type=feedback_type, map=map,
#                                   p10=p10, p20=p20, task=task)
#
#     def test_run_creation(self):
#         r = self.create_run()
#         self.assertTrue(isinstance(r,Run))

