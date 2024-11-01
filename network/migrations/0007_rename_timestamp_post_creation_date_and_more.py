# Generated by Django 4.2 on 2024-11-01 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_post_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='timestamp',
            new_name='creation_date',
        ),
        migrations.AddField(
            model_name='post',
            name='last_edit_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]