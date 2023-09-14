from .models import Commune,MyUser
from django.contrib.auth.models import Group, Permission

# Créer un groupe pour les commune
commune_group, created = Group.objects.get_or_create(name='CommuneGroup')
#créer un groupe pour les hopitals
hospital_group, created = Group.objects.get_or_create(name='HospitalGroup')

# Créer un groupe pour les administrateurs
admin_group, created = Group.objects.get_or_create(name='Administrateur')


# Autorisations pour les commune
commune_permissions = Permission.objects.filter(codename__in=['can_view_profile', 'can_edit_profile'])
commune_group.permissions.add(*commune_permissions)
# Autorisations pour les hopitaux
hospital_permissions = Permission.objects.filter(codename__in=['can_edit_profile'])
hospital_group.permissions.add(*hospital_permissions)


# Autorisations pour les administrateurs
admin_permissions = Permission.objects.filter(codename__in=['view_user', 'add_user'])
admin_group.permissions.add(*admin_permissions)
"""


from django.contrib.auth.models import User
from .models import Client, Administrateur

# Créer un utilisateur client
user_client = User.objects.create_user(username='alice', password='password')
client = Client.objects.create(user=user_client, phone_number='0123456789', address='123 rue de la Paix')
user_client.groups.add(client_group)  # Ajoutez l'utilisateur au groupe "Client"

# Créer un utilisateur administrateur
user_admin = User.objects.create_user(username='bob', password='password')
admin = Administrateur.objects.create(user=user_admin, department='IT', role='Manager')
user_admin.groups.add(admin_group)  # Ajoutez l'utilisateur au groupe "Administrateur"
"""