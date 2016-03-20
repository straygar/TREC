from django.test import TestCase

from main.models import Run, Task, Track, Genre, Researcher

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
                     description="test",genre = Genre.objects.create(title="testGenre")):
        return Track.objects.create(title=title, track_url=track_url,
                                    description=description, genre=genre)

    def test_track_creation(self):
        t = self.create_track()
        self.assertTrue(isinstance(t,Track))
        self.assertEqual(t.__unicode__(), "testTrack")
        self.assertEqual(t.track_url, "www.google.com")
        self.assertEqual(t.description, "test")
        self.assertEqual(t.genre.__unicode__(), "testGenre")

# class TaskModelTests(TestCase):
#     def create_task(selfself, title="testTask", task_url="www.google.com",
#                     description="test", year=2016):
#          return Task.objects.create(title=title, task_url=task_url,
#                                     description=description, year=year)
#
#     def test_task_creation(self):
#         t = self.create_task()
#         self.assertTrue(isinstance(t,Task))
#         self.assertEqual(t.__unicode__(), "testTask")
#         self.assertEqual(t.track_url, "www.google.com")
#         self.assertEqual(t.description, "test")
#         self.assertEqual(t.year, 2016)

# class RunModelTests(TestCase):


