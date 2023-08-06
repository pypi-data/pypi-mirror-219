from io import BytesIO

from django.core.files.images import ImageFile
from faker.providers import BaseProvider

from x11x_wagtail_blog.models import AboutTheAuthor


class X11XWagtailBlogProvider(BaseProvider):
    """
    Provider for the wonderful faker library. Add `X11XWagtailBlogProvider` to a standard faker to generate data for your test
    code.

    >>> from faker import Faker
    >>> fake = Faker()
    >>> fake.add_provider(X11XWagtailBlogProvider)
    >>> fake.avatar_image_content()  # doctest: +NORMALIZE_QUOTES
    b'\\x89PNG...
    """

    def avatar_image_content(self, *, size=(32, 32)) -> bytes:
        """
        Generate an avatar image of the given size. By default, the image
        will be a PNG 32 pixels by 32 pixels.

        The use of the image generation functions require the PIL library to be installed.

        :param tuple[int, int] size: The width and height of the image to generate.
        :return bytes: Returns the binary content of the PNG.

        >>> fake.avatar_image_content(size=(4, 4))  # doctest: +NORMALIZE_QUOTES
        b'\\x89PNG...
        """
        return self.generator.image(
            size=size,
            image_format="png",
        )

    def avatar_image_file(self) -> ImageFile:
        """
        Generates a `django.core.files.images.ImageFile` that can be assigned to a user's profile.

        The use of the image generation functions require the PIL library to be installed.

        >>> fake.avatar_image_file()
        <ImageFile: ....png>
        """
        return ImageFile(
            BytesIO(self.avatar_image_content()),
            self.generator.file_name(extension="png"),
        )

    def about_the_author(self, author) -> AboutTheAuthor:
        """
        Generates an AboutTheAuthor snippet.
        """
        return AboutTheAuthor(
            author=author,
            body=self.generator.paragraph(),
        )

    def title_image_content(self, *, size=(2, 2)) -> bytes:
        """
        Generates image content suitable for the 'title_image'. Unless ``size`` is given, a 2x2 pixel image will be generated.

        >>> fake.title_image_content()  # doctest: +NORMALIZE_QUOTES
        b'\\x89PNG...

        :param tuple[int, int] size: The width and height of the image to generate.
        :return bytes: Returns the content of the title image.
        """
        return self.generator.image(
            size=size,
            image_format="png",
        )

    def title_image_file(self, *, name=None) -> ImageFile:
        """
        Generates a `django.core.files.images.ImageFile` that can be assigned to a user's profile.

        >>> fake.title_image_file(name="this-name.png")
        <ImageFile: this-name.png>

        :param str name: The name of the image file to generate.
        :return ImageFile: Returns an `ImageFile`
        """
        name = name or self.generator.file_name(extension="png")
        return ImageFile(
            BytesIO(self.title_image_content()),
            name,
        )
