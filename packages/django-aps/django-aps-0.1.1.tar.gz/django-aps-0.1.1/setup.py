from setuptools import find_packages, setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django-aps",
    version="0.1.1",
    description="APScheduler Register for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cuidingyong/django-aps",
    author="Dillon",
    author_email="cuidingyong@yeah.net",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
    ],
    keywords="django apscheduler django-django_aps register",
    packages=find_packages(exclude=["django_aps1", "django_aps1.*", "test", "test.*"]),
    install_requires=[
        "django>=3.2",
        "apscheduler>=3.2,<4.0",
        "djangorestframework>=3.14",
        "django-apscheduler>=0.6.2",
        "pydantic>=2.0"
    ],
    zip_safe=False,
)
