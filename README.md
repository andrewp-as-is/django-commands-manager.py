<!--
https://readme42.com
-->


[![](https://img.shields.io/pypi/v/django-commands-manager.svg?maxAge=3600)](https://pypi.org/project/django-commands-manager/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![](https://github.com/andrewp-as-is/django-commands-manager.py/workflows/tests42/badge.svg)](https://github.com/andrewp-as-is/django-commands-manager.py/actions)

### Installation
```bash
$ [sudo] pip install django-commands-manager
```

##### `settings.py`
```python
INSTALLED_APPS+=['django_commands_manager']
```

##### migrate
```bash
$ python manage.py migrate
```

#### Examples
Queue
```python
from django_postgres_refresh_matviews.models import Matview
from django_postgres_refresh_matviews.utils import refresh_matviews_queue

Matview.objects.get_or_create(schemaname='public',matviewname='matview1')
Matview.objects.get_or_create(schemaname='public',matviewname='matview2')

refresh_matviews()

Matview.objects.filter(schemaname='public').update(is_completed=False)
```

Log
```python
from django_commands_manager.models import Log

for l in Log.objects.filter(schemaname='public',matviewname='matview1'):
    l.started_at, l.completed_at
```

Exc
```python
from django_commands_manager.models import Exc

for l in Log.objects.filter(schemaname='public',matviewname='matview1'):
    l.started_at, l.completed_at
```

cli
```bash
$ python manage.py run_commands "group1"
$ python manage.py run_commands "group2"
```

<p align="center">
    <a href="https://readme42.com/">readme42.com</a>
</p>
