# Generated by Django 2.1.3 on 2018-12-02 18:29
# If you delete this there will be hell to pay

from __future__ import unicode_literals
from django.db import migrations
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.management import create_permissions

PERMISSIONS_Default = ["can_view_section",
                       "can_view_course",
                       "can_view_user"]

PERMISSIONS_Ta = ["can_view_course",
                  "can_view_section",
                  "can_edit_self",
                  "can_view_user"]

PERMISSIONS_Instructor = ["can_view_course",
                          "can_edit_self",
                          "can_view_user",
                          "can_view_private",
                          "can_assign_ta",
                          "can_email_tas"]

PERMISSIONS_Admin = ["can_create_course",
                     "can_edit_course",
                     "can_delete_course",
                     "can_view_course",
                     "can_create_section",
                     "can_edit_section",
                     "can_delete_section",
                     "can_view_section",
                     "can_create_user",
                     "can_edit_user",
                     "can_edit_self",
                     "can_delete_user",
                     "can_view_user",
                     "can_view_private",
                     "can_email_all"]

PERMISSIONS_Supervisor = ["can_create_course",
                          "can_edit_course",
                          "can_delete_course",
                          "can_view_course",
                          "can_create_section",
                          "can_edit_section",
                          "can_delete_section",
                          "can_view_section",
                          "can_create_user",
                          "can_edit_user",
                          "can_edit_self",
                          "can_delete_user",
                          "can_view_user",
                          "can_view_private",
                          "can_assign_ta",
                          "can_assign_ins",
                          "can_email_all"]


def create_group(apps, schema_editor):
    groups = {'Default': PERMISSIONS_Default,  # Add to this dict if another group needs to be created
              'TA': PERMISSIONS_Ta,
              'Instructor': PERMISSIONS_Instructor,
              'Admin': PERMISSIONS_Admin,
              'Supervisor': PERMISSIONS_Supervisor}

    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    for key in groups:
        group, created = Group.objects.get_or_create(name=key)

        if created:
            permissions = []
            for perm in groups[key]:
                print("Adding permission %s to group %s" % (perm, key))
                permissions.append(Permission.objects.get(codename=perm))

            group.permissions.add(*permissions)
            print("%s group created" % key)

        else:
            print("%s group failed to create" % key)


class Migration(migrations.Migration):
    dependencies = [('TAServer', '0001_initial'), ]
    operations = [migrations.RunPython(create_group), ]