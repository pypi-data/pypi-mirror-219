# Django APScheduler Register

Django-aps adds the task registration discovery function on the basis of A,
which is more convenient for users to realize the configuration of scheduled tasks.

## Installation

```commandline
pip install django-aps
```

## Quick start

- Add ``aps`` to your ``INSTALLED_APPS`` setting like this:

```python
INSTALLED_APPS = (
    # ...
    "django_aps",
)
```

- django-aps comes with sensible configuration defaults out of the box. The defaults can be overridden by adding
  the following settings to your Django `settings.py` file:

```python
DEFAULT_DISCOVER_SCHEMA = 'pkg'
```

- Run `python manage.py migrate` to create the django_apscheduler models.

- Register a APScheduler function in your project

```python

```