Django Auditor Logs is a Django app that provides a simple way to log events CREATE, UPDATE AND DELETE in your Django project. It is designed to be used with the Graphene Django package or Django Graphbox, but can be used with any Django project.

Installation
--------------------------------
    .. code-block:: bash

        pip install django-auditor-logs

Quick start
--------------------------------
1. Add "django_auditor_logs" to your INSTALLED_APPS setting like this::
    .. code-block:: python3

        INSTALLED_APPS = [
            ...
            'django_auditor_logs',
        ]

2. Configure AUDIT_APPS in your settings.py file like this::
    .. code-block:: python3
        
        AUDIT_APPS = [
            'app1',
            'app2',
        ]

3. Run `python manage.py migrate` to create the django_auditor_logs models.

4. Optionally you can change MIGRATION_MODULES in your settings.py file like this::
    .. code-block:: python3

        MIGRATION_MODULES = {
            'django_auditor_logs': 'app1.migrations',
        }

5. User and request metadata is set by a middleware. Add the middleware to your MIDDLEWARE setting like this::
    .. code-block:: python3

        MIDDLEWARE = [
            ...
            'django_auditor_logs.middleware.metadata_middleware.MetadataMiddleware',
        ]


Release notes
--------------------------------

    * 1.0.0
        - Initial release.
    * 1.0.1
        - Replace decorator and __user_metadata__ and __request_metadata__ fields by a MetadataManager class used in a Middleware.
    * 1.0.2
        - Fix documentation of the middleware.
    * 1.0.3
        - Fix WARNING default_auto_field.