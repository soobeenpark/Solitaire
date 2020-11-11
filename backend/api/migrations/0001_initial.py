# Generated by Django 3.1.3 on 2020-11-10 18:16

import api.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('city', models.CharField(default='', max_length=200)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('color', models.CharField(default='red', max_length=50)),
                ('draw_count', models.IntegerField(default=1)),
                ('score', models.IntegerField(default=0)),
                ('won', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KlondikeState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pile1', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('pile2', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('pile3', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('pile4', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('pile5', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('pile6', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('pile7', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('stack1', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('stack2', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('stack3', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('stack4', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('discard', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('draw', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cards', django.contrib.postgres.fields.ArrayField(base_field=api.fields.CardField(), size=None)),
                ('src', models.CharField(max_length=100)),
                ('dst', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moves', to='api.game')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='state',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.klondikestate'),
        ),
    ]