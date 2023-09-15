from django.contrib.auth.models import Group
admin_group, created = Group.objects.get_or_create(name='Administrateurs')
commune_group, created = Group.objects.get_or_create(name='Communes')
hopital_group, created = Group.objects.get_or_create(name='Hopitaux')
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
"""
content_type = ContentType.objects.get(app_label='User', model='actenaiss')
permission_codename = 'add'
permission = Permission.objects.get(codename=permission_codename, content_type=content_type)

commune_permissions =permission

commune_group.permissions.add(commune_permissions)

hospital_permissions=Permission.objects.filter(codename_in=['add_certificatnaissance','view_certificatnaissance',  'change_certificatnaissance','delete_certificatnaissance'])
hopital_group.permissions.add(*hospital_permissions)"""