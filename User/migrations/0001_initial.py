# Generated by Django 5.0.6 on 2024-10-23 01:44

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificat_Desc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medecin_traitant', models.CharField(blank=True, max_length=120)),
                ('nom_defunt', models.CharField(blank=True, max_length=40)),
                ('post_nom_defunt', models.CharField(blank=True, max_length=40)),
                ('prenom_defunt', models.CharField(blank=True, max_length=40)),
                ('sexe_defunt', models.CharField(blank=True, choices=[('m', 'Masculin'), ('f', 'Feminin')], max_length=1)),
                ('lieu_naissance', models.CharField(blank=True, max_length=120)),
                ('date_naissance_defunt', models.DateField()),
                ('profession_defunt', models.CharField(blank=True, max_length=40)),
                ('cause_desc', models.CharField(blank=True, max_length=30)),
                ('date_desc', models.DateField()),
                ('date_deliv_cert', models.DateField(auto_now_add=True)),
                ('url_qrcode', models.CharField(blank=True, max_length=2000, null=True)),
                ('cod_qr', models.ImageField(blank=True, null=True, upload_to='certificat_desces')),
            ],
            options={
                'verbose_name': 'Certificat de Décès',
                'verbose_name_plural': 'Certificats de Décès',
            },
        ),
        migrations.CreateModel(
            name='CertificatNaissance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_medecin', models.CharField(blank=True, max_length=40)),
                ('nom_enfant', models.CharField(blank=True, max_length=40)),
                ('post_nom_enfant', models.CharField(blank=True, max_length=40)),
                ('prenom_enfant', models.CharField(blank=True, max_length=40)),
                ('sexe_enfant', models.CharField(blank=True, choices=[('m', 'Masculin'), ('f', 'Feminin')], max_length=1)),
                ('poid_enfant', models.FloatField()),
                ('date_nais_enfant', models.DateField(auto_now_add=True)),
                ('date_deliv_cert', models.DateField(auto_now=True)),
                ('nom_complet_pere', models.CharField(blank=True, max_length=120)),
                ('profession_pere', models.CharField(blank=True, max_length=20)),
                ('date_nais_pere', models.DateField()),
                ('lieu_nais_pere', models.CharField(blank=True, max_length=20)),
                ('nationalite_pere', models.CharField(blank=True, max_length=20)),
                ('nom_complet_mere', models.CharField(blank=True, max_length=120)),
                ('profession_mere', models.CharField(blank=True, max_length=20)),
                ('date_nais_mere', models.DateField()),
                ('lieu_nais_mere', models.CharField(blank=True, max_length=20)),
                ('nationalite_mere', models.CharField(max_length=20)),
                ('localite_parent', models.CharField(blank=True, max_length=20)),
                ('collectiv_parent', models.CharField(blank=True, max_length=20)),
                ('url_qrcode', models.CharField(blank=True, max_length=2000, null=True)),
                ('cod_qr', models.ImageField(blank=True, null=True, upload_to='certificat_naissance')),
            ],
            options={
                'verbose_name': 'Certificat de Naissance',
                'verbose_name_plural': 'Certificats de Naissance',
            },
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denom', models.CharField(blank=True, max_length=70)),
                ('nom_bour', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Commune',
                'verbose_name_plural': 'Communes',
            },
        ),
        migrations.CreateModel(
            name='Hopital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='email@gmail.com', max_length=254, unique=True)),
                ('boite_postal', models.CharField(blank=True, max_length=9)),
                ('denom', models.CharField(blank=True, max_length=70)),
                ('numeros_id', models.CharField(max_length=40, unique=True)),
            ],
            options={
                'verbose_name': 'Hopital',
                'verbose_name_plural': 'Hopitaux',
            },
        ),
        migrations.CreateModel(
            name='province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denom', models.CharField(max_length=70, unique=True)),
            ],
            options={
                'verbose_name': 'Province',
                'verbose_name_plural': 'Provinces',
            },
        ),
        migrations.CreateModel(
            name='ActeNaiss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeros_volume', models.CharField(blank=True, max_length=15)),
                ('numeros_folio', models.CharField(blank=True, max_length=5, null=True)),
                ('nom_declarant', models.CharField(blank=True, max_length=120)),
                ('qualite_declarant', models.CharField(blank=True, max_length=20)),
                ('profession_declarant', models.CharField(max_length=20)),
                ('date_enregistrement', models.DateField(auto_now_add=True)),
                ('langue_redaction', models.CharField(blank=True, max_length=20)),
                ('url_qrcode', models.CharField(blank=True, max_length=2000, null=True)),
                ('cod_qr', models.ImageField(blank=True, null=True, upload_to='acte_naissance')),
                ('certNais_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='User.certificatnaissance')),
                ('commune', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.commune')),
            ],
            options={
                'verbose_name': 'Acte  de Naissance',
                'verbose_name_plural': 'Actes de Naissance',
            },
        ),
        migrations.CreateModel(
            name='ActeDesc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeros_volume', models.CharField(blank=True, max_length=15)),
                ('nom_declarant', models.CharField(blank=True, max_length=120)),
                ('qualite_declarant', models.CharField(blank=True, max_length=20)),
                ('profession_declarant', models.CharField(blank=True, max_length=20)),
                ('residence_principale', models.CharField(blank=True, max_length=220)),
                ('residence_temporaire', models.CharField(blank=True, default=None, max_length=220, null=True)),
                ('nationalite', models.CharField(blank=True, max_length=40)),
                ('etat_civile', models.CharField(blank=True, choices=[('m', 'Marié'), ('c', 'Celibataire')], max_length=1)),
                ('conjoint_identite', models.CharField(blank=True, max_length=120, null=True)),
                ('nom_complet_pere', models.CharField(blank=True, max_length=120)),
                ('nom_complet_mere', models.CharField(blank=True, max_length=120)),
                ('date_enregistrement', models.DateField(auto_now_add=True)),
                ('langue_redaction', models.CharField(blank=True, max_length=20)),
                ('url_qrcode', models.CharField(blank=True, max_length=2000, null=True)),
                ('cod_qr', models.ImageField(blank=True, null=True, upload_to='acte_desc')),
                ('cert_desc_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='User.certificat_desc')),
                ('commune', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.commune')),
            ],
            options={
                'verbose_name': 'Acte  de Descès',
                'verbose_name_plural': 'Actes de Descès',
            },
        ),
        migrations.AddField(
            model_name='certificatnaissance',
            name='hospital_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.hopital'),
        ),
        migrations.AddField(
            model_name='certificat_desc',
            name='hopital_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.hopital'),
        ),
        migrations.AddField(
            model_name='hopital',
            name='prov',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.province'),
        ),
        migrations.AddField(
            model_name='commune',
            name='prov',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.province'),
        ),
        migrations.CreateModel(
            name='TerriVille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denom', models.CharField(max_length=70, unique=True)),
                ('prov', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.province')),
            ],
            options={
                'verbose_name': 'Ville ou Territoire',
                'verbose_name_plural': 'Villes ou Territoires',
            },
        ),
        migrations.AddField(
            model_name='hopital',
            name='TerriVi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.terriville'),
        ),
        migrations.AddField(
            model_name='commune',
            name='TerriVi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.terriville'),
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('commune', 'Commune'), ('hopital', 'Hopital')], max_length=10)),
                ('groups', models.ManyToManyField(blank=True, related_name='myuser_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='myuser_set', to='auth.permission')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='hopital',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commune',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='certificatnaissance',
            unique_together={('nom_enfant', 'post_nom_enfant', 'prenom_enfant', 'sexe_enfant', 'date_nais_enfant')},
        ),
        migrations.AlterUniqueTogether(
            name='certificat_desc',
            unique_together={('nom_defunt', 'post_nom_defunt', 'prenom_defunt')},
        ),
    ]
