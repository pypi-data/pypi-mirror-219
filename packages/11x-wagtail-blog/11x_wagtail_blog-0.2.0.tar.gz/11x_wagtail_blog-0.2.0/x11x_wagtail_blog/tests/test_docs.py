import doctest

from django.test import TestCase
from faker import Faker

import x11x_wagtail_blog
import x11x_wagtail_blog.models
import x11x_wagtail_blog.fakers

NORMALIZE_QUOTES = doctest.register_optionflag("NORMALIZE_QUOTES")


class QuoteNormalizingOutputChecker(doctest.OutputChecker):
    def check_output(self, want: str, got: str, optionflags: int) -> bool:
        if optionflags & NORMALIZE_QUOTES:
            want = want.replace('"', "'")
            got = got.replace('"', "'")
        return super().check_output(want, got, optionflags)


def run_doctests(m, optionflags=0, extraglobs=None):
    finder = doctest.DocTestFinder()
    runner = doctest.DocTestRunner(checker=QuoteNormalizingOutputChecker(), optionflags=optionflags)
    for test in finder.find(m, m.__name__, extraglobs=extraglobs):
        runner.run(test)
    runner.summarize()

    return doctest.TestResults(runner.failures, runner.tries)


class DocTests(TestCase):
    def test_docstrings(self):
        results = doctest.testmod(x11x_wagtail_blog)
        self.assertEqual(results.failed, 0)

        results = doctest.testmod(x11x_wagtail_blog.models)
        self.assertEqual(results.failed, 0)

        fake = Faker()
        fake.add_provider(x11x_wagtail_blog.fakers.X11XWagtailBlogProvider)

        results = run_doctests(
            x11x_wagtail_blog.fakers,
            extraglobs={
                "fake": fake,
            },
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.IGNORE_EXCEPTION_DETAIL,
        )
        self.assertEqual(results.failed, 0)
