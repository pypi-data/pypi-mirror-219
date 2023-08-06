"""Updates the `README.rst` at the root of the repository with the latest documentation."""
from dataclasses import dataclass
from pathlib import Path
import sys

import jinja2

PACKAGE_NAME = "11x-wagtail-blog"
GITHUB_ORGANIZATION = "11x-engineering"


@dataclass
class Badge:
    link_to: str
    badge: str
    label: str

    def as_rst_declaration(self):
        return f"|{self.label}|"

    def as_rst_definition(self):
        return f".. |{self.label}| image:: {self.badge}\n   :target: {self.link_to}"

    def as_markdown(self):
        return f"[![{self.label}]({self.badge})]({self.link_to})"


class Badges:
    PYPI = Badge(
        f"https://pypi.org/project/{PACKAGE_NAME}/",
        f"https://img.shields.io/pypi/v/{PACKAGE_NAME}",
        "PyPI",
    )
    VERSIONS = Badge(
        PYPI.link_to,
        f"https://img.shields.io/pypi/pyversions/{PACKAGE_NAME}.svg",
        "Supported Python versions",
    )
    RTFM = Badge(
        f"https://{PACKAGE_NAME}.readthedocs.io/en/latest/?badge=latest",
        f"https://readthedocs.org/projects/{PACKAGE_NAME}/badge/?version=latest",
        "Documentation",
    )
    STATS = Badge(
        f"https://pepy.tech/project/{PACKAGE_NAME}/",
        f"https://pepy.tech/badge/{PACKAGE_NAME}/month",
        "Downloads",
    )
    CI = Badge(
        f"https://github.com/{GITHUB_ORGANIZATION}/{PACKAGE_NAME}/actions/workflows/package.yml",
        f"https://github.com/{GITHUB_ORGANIZATION}/{PACKAGE_NAME}/actions/workflows/package.yml/badge.svg",
        "Build",
    )


def main():
    base_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(base_dir))

    import x11x_wagtail_blog

    badges = [
        Badges.PYPI,
        Badges.CI,
        Badges.VERSIONS,
        Badges.RTFM,
        Badges.STATS,
    ]

    template_path = base_dir / "README.j2.rst"
    with open(template_path) as f:
        content = f.read()

    template = jinja2.Template(content)
    result = template.render(
        **globals(),
        **locals(),
    )

    readme_path = base_dir / "README.rst"
    with open(readme_path, "w") as f:
        f.write(result)


if __name__ == '__main__':
    main()
