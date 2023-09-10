from .models import Commune,MyUser
user=MyUser.objects.create_user(username="mec",password="mec")
com=Commune.objects.create(user=user,prov=1,TerriVi=1,nom_bour='damiel')

 

from django.contrib.auth.models import Group, Permission

# Créer un groupe pour les clients
client_group, created = Group.objects.get_or_create(name='Client')

# Créer un groupe pour les administrateurs
admin_group, created = Group.objects.get_or_create(name='Administrateur')


# Autorisations pour les clients
client_permissions = Permission.objects.filter(codename__in=['can_view_profile', 'can_edit_profile'])
client_group.permissions.add(*client_permissions)

# Autorisations pour les administrateurs
admin_permissions = Permission.objects.filter(codename__in=['can_manage_users', 'can_edit_settings'])
admin_group.permissions.add(*admin_permissions)



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
