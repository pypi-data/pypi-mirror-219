import setuptools

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

__version__ = 0.1

SRC_REPO = "Python_Package_Project"
REPO_NAME = "new_test"
AUTHOR_USER_NAME = "APLonly"
AUTHOR_EMAIL = "aplonly2018@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package",
    long_description=LONG_DESCRIPTION,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
