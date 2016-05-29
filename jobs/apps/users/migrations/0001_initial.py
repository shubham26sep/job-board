# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.auth.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', error_messages={'unique': 'A user with that username already exists.'}, unique=True, max_length=75)),
                ('name', models.CharField(verbose_name='name', max_length=60)),
                ('email', models.EmailField(verbose_name='email address', unique=True, max_length=254)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active.  Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('resume', models.BooleanField(default=False)),
                ('mobile_number', models.CharField(null=True, blank=True, verbose_name='mobile number', max_length=15)),
                ('work_experience', models.DecimalField(null=True, max_digits=4, blank=True, decimal_places=2)),
                ('ctc', models.DecimalField(null=True, max_digits=4, blank=True, decimal_places=1)),
                ('current_designation', models.CharField(null=True, blank=True, verbose_name='current designation', max_length=100)),
                ('current_employer', models.CharField(null=True, blank=True, verbose_name='current employer', max_length=100)),
                ('user_type', models.CharField(default='recruiter', max_length=20, choices=[('recruiter', 'Recruiter'), ('candidate', 'Candidate')])),
                ('ug_course', models.CharField(default='none', max_length=20, choices=[('none', 'NA'), ('B.Tech/B.E.', 'B.Tech/B.E.'), ('B.Sc', 'B.Sc'), ('B.C.A', 'B.C.A')])),
                ('ug_institute_name', models.CharField(null=True, blank=True, verbose_name='ug institute name', max_length=100)),
                ('ug_tier1', models.BooleanField(default=False)),
                ('ug_passing_year', models.PositiveSmallIntegerField(null=True, blank=True, max_length=4)),
                ('pg_course', models.CharField(default='none', max_length=20, choices=[('none', 'NA'), ('M.Tech', 'M.Tech'), ('M.C.A', 'M.C.A')])),
                ('pg_institute_name', models.CharField(null=True, blank=True, verbose_name='pg institute name', max_length=100)),
                ('pg_tier1', models.BooleanField(default=False)),
                ('pg_passing_year', models.PositiveSmallIntegerField(null=True, blank=True, max_length=4)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'ordering': ['username'],
                'swappable': 'AUTH_USER_MODEL',
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('location', models.CharField(null=True, blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=60)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='corrected_location',
            field=models.ForeignKey(null=True, blank=True, related_name='corrected_location', to='users.Location'),
        ),
        migrations.AddField(
            model_name='user',
            name='current_location',
            field=models.ForeignKey(null=True, blank=True, related_name='current_location', to='users.Location'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_name='user_set', blank=True, related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='nearest_city',
            field=models.ForeignKey(null=True, blank=True, related_name='nearest_city', to='users.Location'),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_location',
            field=models.ManyToManyField(null=True, blank=True, to='users.Location'),
        ),
        migrations.AddField(
            model_name='user',
            name='skills',
            field=models.ManyToManyField(null=True, related_name='skills', blank=True, to='users.Skill'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_name='user_set', blank=True, related_query_name='user', help_text='Specific permissions for this user.', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
