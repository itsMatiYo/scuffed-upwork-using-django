# Generated by Django 3.2 on 2021-10-20 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('itapi', '0001_initial'),
        ('projects_api', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetablevisitor',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetoproject', to='projects_api.project'),
        ),
        migrations.AddField(
            model_name='timetablevisitor',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='timetotable', to='itapi.timetable'),
        ),
        migrations.AddField(
            model_name='timetablevisitor',
            name='visitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='timetovisitor', to='users.visitor'),
        ),
        migrations.AlterUniqueTogether(
            name='timetable',
            unique_together={('start', 'end', 'day')},
        ),
        migrations.AddField(
            model_name='reportemployee',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reportemps', to='users.employee'),
        ),
        migrations.AddField(
            model_name='reportemployee',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportemps', to='projects_api.project'),
        ),
        migrations.AddField(
            model_name='reportemployee',
            name='rep_cd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reportemps', to='users.cityadmin'),
        ),
        migrations.AddField(
            model_name='reportemployee',
            name='rep_customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reportemps', to='users.customer'),
        ),
        migrations.AddField(
            model_name='reportemployee',
            name='rep_expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reportemps', to='users.expert'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cities', to='itapi.province'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subcategories', to='itapi.category'),
        ),
        migrations.AlterUniqueTogether(
            name='timetablevisitor',
            unique_together={('time', 'visitor', 'date')},
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('name', 'province')},
        ),
    ]
