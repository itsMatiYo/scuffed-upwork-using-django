# Generated by Django 3.2 on 2021-10-27 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects_api', '0002_alter_projectrequestvisitor_options'),
        ('itapi', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetablevisitor',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='timetoproject', to='projects_api.project'),
        ),
    ]