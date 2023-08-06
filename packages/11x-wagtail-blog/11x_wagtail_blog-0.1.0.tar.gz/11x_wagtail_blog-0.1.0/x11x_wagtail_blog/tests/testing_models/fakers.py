from django.utils.timezone import make_aware
from faker.providers import BaseProvider

from x11x_wagtail_blog.tests.testing_models.models import TestingArticlePage


class TestingModelProvider(BaseProvider):
    def testing_article_page(self, *, owner=None) -> TestingArticlePage:
        return TestingArticlePage(
            title=self.generator.sentence().title(),
            summary=self.generator.sentence(),
            body=[("text", self.generator.paragraph())],
            date=make_aware(self.generator.date_time()),
            owner=owner,
        )
