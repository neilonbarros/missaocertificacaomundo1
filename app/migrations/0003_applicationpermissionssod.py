# Generated by Django 4.2.3 on 2023-08-15 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_applicationdepartments_department_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationPermissionsSoD',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('permission_sod', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'app_permissions_sod',
            },
        ),
    ]