from django.utils import timezone
from django.test import override_settings
from faker import Faker
from wagtail.test.utils import WagtailPageTestCase
from wagtail.models import Page
from wagtail.images import get_image_model
from wagtail.users.models import UserProfile

from x11x_wagtail_blog.fakers import X11XWagtailBlogProvider
from x11x_wagtail_blog.tests.testing_models.fakers import TestingModelProvider
from x11x_wagtail_blog.tests.testing_models.models import TestingArticlePage

Image = get_image_model()

fake = Faker()
fake.add_provider(X11XWagtailBlogProvider)
fake.add_provider(TestingModelProvider)


@override_settings(
    X11X_WAGTAIL_BLOG_ARTICLE_TEMPLATE="x11x_wagtail_blog/tests/testing_models/testing_article_page.html"
)
class TestArticlePages(WagtailPageTestCase):
    def setUp(self):
        super().setUp()
        self.home = Page.objects.get(slug="home")

    def test_blog_articles_have_the_basic_fields(self):
        content = fake.paragraph()
        title = fake.sentence().title()
        username = fake.user_name()
        publishing_date = timezone.make_aware(fake.date_time())
        summary_text = fake.sentence()

        author = self.create_user(
            username,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

        page = TestingArticlePage(
            title=title,
            body=[("text", content)],
            owner=author,
            summary=summary_text,
            date=publishing_date
        )
        self.publish(page)

        response = self.client.get(page.full_url)
        self.assertContains(response, content)
        self.assertContains(response, author.first_name)
        self.assertContains(response, author.last_name)
        self.assertContains(response, str(publishing_date.year))
        self.assertContains(response, str(publishing_date.month))
        self.assertContains(response, str(publishing_date.day))
        self.assertTemplateUsed(
            response,
            "x11x_wagtail_blog/tests/testing_models/testing_article_page.html",
        )

    def test_model_has_authors_returns_fals_when_not_configured_with_authors(self):
        page = fake.testing_article_page()
        self.publish(page)

        self.assertFalse(page.has_authors())

    def test_model_has_authors_returns_true_when_configured_with_authors(self):
        author = self.create_user("username")

        snippet = fake.about_the_author(author)
        snippet.save()

        page = fake.testing_article_page()
        page.authors = [("about_the_authors", snippet)]
        self.publish(page)

        self.assertTrue(page.has_authors())

    def test_blog_has_title_image(self):
        author = self.create_user("username")

        image_base_name = "test-image"
        image_extension = "png"

        header_image = Image.objects.create(
            title=fake.word(),
            file=fake.title_image_file(
                name=f"{image_base_name}.{image_extension}",
            )
        )
        page = fake.testing_article_page(owner=author)
        page.title_image = header_image
        self.publish(page)

        response = self.client.get(page.full_url)
        self.assertContains(response, page.title_image.title)
        self.assertContains(response, image_base_name)
        self.assertContains(response, image_extension)

    def test_related_articles_are_rendered_properly(self):
        owner = self.create_user("username")

        related_page_a = fake.testing_article_page(owner=owner)
        related_page_b = fake.testing_article_page(owner=owner)

        self.home.add_child(instance=related_page_a)
        self.home.add_child(instance=related_page_b)

        page = TestingArticlePage(
            title="Page",
            body=[("text", "Content")],
            owner=owner,
        )
        page.related_articles = [related_page_a, related_page_b]
        self.publish(page)

        response = self.client.get(page.full_url)
        for related_page in [related_page_a, related_page_b]:
            self.assertContains(response, f"<a href=\"{related_page.url}\">{related_page.title}</a>")

    def test_about_the_author_content(self):
        owner = self.create_user("username")

        owner.wagtail_userprofile = UserProfile()
        owner.wagtail_userprofile.avatar = fake.avatar_image_file()
        owner.wagtail_userprofile.save()

        snippet = fake.about_the_author(owner)
        snippet.save()

        page = fake.testing_article_page(owner=owner)
        page.authors = [("about_the_authors", snippet)]

        self.publish(page)

        response = self.client.get(page.url)
        self.assertContains(response, snippet.body)
        self.assertContains(response, owner.wagtail_userprofile.avatar.url)

    def test_model_is_extensible(self):
        owner = self.create_user("username")

        content = fake.sentence()

        page = TestingArticlePage(
            title="Page",
            body=[("text", content)],
            owner=owner,
        )
        self.publish(page)

        response = self.client.get(page.full_url)
        self.assertContains(response, content)

    def publish(self, page):
        self.home.add_child(instance=page)
