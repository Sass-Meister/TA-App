# Generated by Django 2.1.3 on 2018-11-27 20:19

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnum', models.CharField(max_length=4)),
                ('dept', models.CharField(max_length=10)),
                ('name', models.CharField(blank=True, default='', max_length=40)),
                ('description', models.CharField(blank=True, default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='InsGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snum', models.CharField(max_length=4)),
                ('stype', models.CharField(blank=True, choices=[('lab', 'Lab'), ('lecture', 'Lecture')], max_length=10, null=True)),
                ('room', models.IntegerField(blank=True, default=-1, null=True)),
                ('days', models.CharField(blank=True, choices=[('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('H', 'Thursday'), ('F', 'Friday'), ('MW', 'Monday Wednesday'), ('TH', 'Tuesday Thursday'), ('MWF', 'Monday Wednesday Friday')], default='', max_length=5, null=True)),
                ('time', models.CharField(blank=True, max_length=15)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TAServer.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(choices=[('T', 'TA'), ('I', 'Instructor'), ('A', 'Administrator'), ('S', 'Supervisor')], default='', max_length=13)),
                ('phonenum', models.CharField(default='', max_length=10)),
                ('address', models.CharField(default='', max_length=30)),
                ('courses', models.ManyToManyField(blank=True, to='TAServer.Course')),
                ('sections', models.ManyToManyField(blank=True, to='TAServer.Section')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SupGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='TAGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='sections',
            field=models.ManyToManyField(blank=True, null=True, related_name='sec', to='TAServer.Section'),
        ),
    ]
