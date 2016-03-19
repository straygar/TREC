from django.test import TestCase

from main.models import Run, Task, Track, Genre, Researcher

class GenreModelTests(TestCase):
    def create_genre(self, title="testGenre"):
        return Genre.objects.create(title=title)

    def test_genre_creation(self):
        g = self.create_genre()
        self.assertTrue(isinstance(g, Genre))
        self.assertEqual(g.__unicode__(),"testGenre")

class ResearcherMoelTests(TestCase):
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


