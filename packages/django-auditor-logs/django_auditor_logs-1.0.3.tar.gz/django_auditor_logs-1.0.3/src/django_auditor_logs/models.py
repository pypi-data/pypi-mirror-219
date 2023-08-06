from django.db import models
from django.conf import settings
# import models of installed apps
from django.apps import apps
import os 
# import MetadataManager
from django_auditor_logs.metadata import MetadataManager
# json
import json

# configure MIGRATION_MODULES setting
create_auditor_migrations_module = False
if not hasattr(settings, 'MIGRATION_MODULES'):
    settings.MIGRATION_MODULES = {
        'django_auditor_logs': 'auditor_migrations',
    }
    create_auditor_migrations_module = True
else:
    if 'django_auditor_logs' not in settings.MIGRATION_MODULES:
        settings.MIGRATION_MODULES['django_auditor_logs'] = 'auditor_migrations'
        create_auditor_migrations_module = True
    else:
        if settings.MIGRATION_MODULES['django_auditor_logs'] == 'auditor_migrations':
            create_auditor_migrations_module = True
# create auditor_migrations module if it set on auditor_migrations module
if create_auditor_migrations_module:
    # Create auditor_migration module if it doesn't exist on file system
    if not os.path.exists(os.path.join(settings.BASE_DIR, 'auditor_migrations')):
        os.makedirs(os.path.join(settings.BASE_DIR, 'auditor_migrations'))
    # create __init__.py file if it doesn't exist on file system
    if not os.path.exists(os.path.join(settings.BASE_DIR, 'auditor_migrations', '__init__.py')):
        open(os.path.join(settings.BASE_DIR, 'auditor_migrations', '__init__.py'), 'a').close()
# get the AUDIT_APPS from settings
AUDIT_APPS = settings.AUDIT_APPS if hasattr(settings, 'AUDIT_APPS') else []
# iterate over installed apps
audits_models = {}
for app in apps.get_app_configs():
    if app.label in AUDIT_APPS:
        # iterate over models of each app
        if app.models!=None:
            initial_models = app.models.copy()
            for model in initial_models:
                if not model.startswith('audit'):
                    # create a new AuditModel class for each model and add it to the module
                    audits_models['Audit'+model]=type('Audit' + model, (models.Model,), {
                        'id_model': models.IntegerField(),
                        'user_metadata': models.TextField(null=True, blank=True),
                        'request_metadata': models.TextField(null=True, blank=True),
                        'model_metadata': models.TextField(null=True, blank=True),
                        'action': models.CharField(max_length=255),
                        'date': models.DateTimeField(auto_now_add=True),
                        '__module__': 'django_auditor_logs.models',
                    })
                    # create methods for  post_save, post_delete signals
                    def post_save(sender, instance, created, **kwargs):
                        # create a new AuditModel instance
                        model_obj=audits_models['Audit'+sender.__name__.lower()]
                        if model_obj.objects.filter(id_model=instance.id).exists():
                            last_audit = model_obj.objects.filter(id_model=instance.id).order_by('-date')[0]
                            if last_audit.action == 'delete':
                                action = 'create'
                            else:
                                action = 'update'
                        else:
                            action = 'create'
                        model_metadata = {}
                        # iterate over fields of the model except foreign keys and many to many fields and add them to the model_metadata
                        for field in instance._meta.get_fields():
                            if not field.is_relation:
                                model_metadata[field.name] = str(getattr(instance, field.name))         
                        model_obj.objects.create(
                            id_model=instance.id,
                            user_metadata=json.dumps(MetadataManager.get_user_metadata()),
                            request_metadata=json.dumps(MetadataManager.get_request_metadata()),
                            model_metadata=model_metadata,
                            action=action,
                        )
                    def post_delete(sender, instance, **kwargs):
                        # create a new AuditModel instance
                        model_obj=audits_models['Audit'+sender.__name__.lower()]
                        model_metadata = {}
                        # iterate over fields of the model except foreign keys and many to many fields and add them to the model_metadata
                        for field in instance._meta.get_fields():
                            if not field.is_relation:
                                model_metadata[field.name] = str(getattr(instance, field.name) )
                        model_obj.objects.create(
                            id_model=instance.id,
                            user_metadata=json.dumps(MetadataManager.get_user_metadata()),
                            request_metadata=json.dumps(MetadataManager.get_request_metadata()),
                            model_metadata=model_metadata,
                            action='delete',
                        )
                    # connect the methods to the signals
                    models.signals.post_save.connect(post_save, sender=f'{app.label}.{model}', weak=False, dispatch_uid=f'{app.label}.{model}.post_save')
                    models.signals.post_delete.connect(post_delete, sender=f'{app.label}.{model}', weak=False, dispatch_uid=f'{app.label}.{model}.post_delete')