# Django Mailersend (Djmailer)

[![tests](https://github.com/neamaddin/djmailer/actions/workflows/tests.yml/badge.svg)](https://github.com/neamaddin/djmailer/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/neamaddin/djmailer/branch/main/graph/badge.svg?token=EQSB3CD7LM)](https://codecov.io/gh/neamaddin/djmailer)
[![python-versions](https://img.shields.io/static/v1?logo=python&label=python&message=3.8+&color=success)](https://pypi.org/project/djmailer/)
[![PyPI](https://img.shields.io/pypi/v/djmailer?color=success)](https://pypi.org/project/djmailer/)
[![GitHub](https://img.shields.io/pypi/l/djmailer?color=success)](https://github.com/neamaddin/djmailer/blob/master/LICENSE)

Djmailer 

### Content

- [Requirements](#requirements)
- [Installation](#installation)
- [Testing](#testing)
- [License](#license)

## Requirements

Python 3.8+<br>
The package has 2 required dependencies:
- [Django>=3](https://github.com/django/django).
- [Mailersend](https://pypi.org/project/mailersend/).

## Installation

> This project uses celery to send emails, so you need to set up celery for your project first.

If you have already configured celery and a broker for it, it will be enough to run the following command to install:
```sh
pip install djmailer
```
If you are going to install and configure celery to use redis run the following command:
```sh
pip install djmailer[redis]
```
Then add 'djmailer' to your INSTALLED_APPS.
```python
INSTALLED_APPS = [
    ...
    'djmailer',
]
```
Django project `settings.py` file might include following constants:

```python
# djmailer settings

EMAIL_BACKEND = 'djmailer.backend.EmailBackend'
DJMAILER_FROM_EMAIL = 'verified@mail.com'
DJMAILER_FROM_NAME = 'Verified Name'
MAILERSEND_API_KEY = 'YOUR_MAILERSEND_API_KEY'
```
In order for celery to be able to detect tasks in django-mailsend, you need to add package to the task detection function in the configuration file (usually celery.py).
```python

...
app.autodiscover_tasks(packages=['djmailer', ])

```

> Also in the [repository](https://github.com/neamaddin/djmailer) on GitHub there is an example of a Django project on which everything is already configured.

## Testing

To run tests in your project environment just run following command:
```sh
python manage.py test djmailer
```

[Tox](https://tox.wiki/en/latest/) is used to test this package.

> For run tests with python 3.8, 3.9, 3.10 and 3.11 must be installed

> You can use [pyenv](https://github.com/pyenv/pyenv) for dynamic managing python versions

To run tests, install and run tox with the following commands:
```sh
# install tox
pip install tox
# run tox
tox
```
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
