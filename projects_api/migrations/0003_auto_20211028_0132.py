# Generated by Django 3.2 on 2021-10-27 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects_api', '0002_alter_projectrequestvisitor_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description_expert',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='price_expert',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='time_expert',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
