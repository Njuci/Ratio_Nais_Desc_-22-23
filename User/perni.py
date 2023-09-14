from django.contrib.auth.models import Group
admin_group, created = Group.objects.get_or_create(name='Administrateurs')
commune_group, created = Group.objects.get_or_create(name='Communes')
hopital_group, created = Group.objects.get_or_create(name='Hopitaux')
from django.contrib.auth.models import Permission

commune_permissions = Permission.objects.filter(codename__in=['add_actenaiss', 'change_actenaiss','delete_actenaiss','view_actenaiss'])

add_acte_permission =commune_permissions
commune_group.permissions.add(*add_acte_permission)

hospital_permissions=Permission.objects.filter(codename_in=['add_certificatnaissance','view_certificatnaissance',
                                                           'change_certificatnaissance','delete_certificatnaissance'])
hopital_group.permissions.add(*hospital_permissions)