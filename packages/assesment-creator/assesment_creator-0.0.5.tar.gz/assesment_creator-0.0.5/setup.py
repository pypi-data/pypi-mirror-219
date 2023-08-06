import setuptools
import io

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.5"

REPO_NAME = "assesment_creator"
AUTHOR_USER_NAME = "SachinMishra-ux"
SRC_REPO = "assesment_creator"
AUTHOR_EMAIL = "sachin19566@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="assesment creator python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
