from django.test import TestCase

from .models import Article
from slugify import slugify

class ArticleTestCase(TestCase):

    def setUp(self):
        self.number_of_articles = 5
        for i in range(0,self.number_of_articles):
            Article.objects.create(title="hello world",content="some content of article")


    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_first_article_title(self):
        obj = Article.objects.all().order_by('id').first()
        title = obj.title
        slug = obj.slug
        slugified_title = slugify(title)
        self.assertEqual(slug,slugified_title)

    def test_rest_article_titles(self):
        qs = Article.objects.exclude(id=1)
        for obj in qs:            
            title = obj.title
            slug = obj.slug
            slugified_title = slugify(title)
            self.assertNotEqual(slug,slugified_title)

    def test_slugify_title_unique(self):
        slug_list = Article.objects.values_list('slug',flat=True)
        unique_slug_list = list(set(slug_list))
        self.assertEqual(len(slug_list),len(unique_slug_list))

    def test_articles_search(self):
        articles = Article.objects.filter(title="hello world")
        self.assertEqual(len(articles),self.number_of_articles)
        articles1 = Article.objects.filter(content="some content of article")
        self.assertEqual(len(articles1),self.number_of_articles)
