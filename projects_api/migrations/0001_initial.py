# Generated by Django 3.2 on 2021-10-20 17:32

from django.db import migrations, models
import django.db.models.deletion
import projects_api.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('itapi', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=80)),
                ('customer_deadline', models.DateTimeField()),
                ('customer_description', models.TextField(blank=True)),
                ('file', models.FileField(blank=True, upload_to='')),
                ('customer_approve', models.BooleanField(default=False)),
                ('customer_price', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('not_approved', 'تایید نشده'), ('not_started', 'شروع نشده'), ('doing', 'درحال انجام'), ('done', 'انجام شد'), ('stopped', 'متوقف شده')], default='not_approved', max_length=15)),
                ('price_paid', models.BooleanField(default=False)),
                ('paid_money', models.PositiveIntegerField(default=0)),
                ('pre_price_paid', models.BooleanField(default=False, null=True)),
                ('pre_price', models.PositiveIntegerField(blank=True, null=True)),
                ('need_visitor', models.BooleanField(default=False)),
                ('experts_approve', models.BooleanField(default=False)),
                ('price_expert', models.PositiveBigIntegerField(null=True)),
                ('time_expert', models.DateTimeField(null=True)),
                ('description_expert', models.TextField(null=True)),
                ('categories', models.ManyToManyField(related_name='projects', to='itapi.Category')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='itapi.city')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='users.customer')),
                ('employees', models.ManyToManyField(blank=True, related_name='projects', to='users.Employee')),
                ('visitor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='users.visitor')),
            ],
        ),
        migrations.CreateModel(
            name='VerifyExpert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ns', 'not seen'), ('ok', 'ok'), ('nk', 'not ok')], default='ns', max_length=3)),
                ('count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('salary', models.PositiveBigIntegerField(blank=True, null=True)),
                ('time', models.DurationField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='itapi.category')),
                ('expert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verifies', to='users.expert')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verifies', to='projects_api.project')),
            ],
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=None)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='timer', to='projects_api.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectRequestVisitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectrequests', to='users.visitor')),
                ('city', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='itapi.city')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects_api.project')),
                ('visitor', models.ManyToManyField(to='users.Visitor')),
            ],
            options={
                'ordering': ('visitor__yellow_cards',),
            },
        ),
        migrations.CreateModel(
            name='ProjectRequestEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pointer', models.IntegerField(default=1)),
                ('active_employee', models.ManyToManyField(related_name='projectrequests', to='users.Employee')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itapi.category')),
                ('employee', models.ManyToManyField(to='users.Employee')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects_api.project')),
            ],
            options={
                'ordering': ('employee__yellow_cards',),
            },
        ),
        migrations.CreateModel(
            name='PayDateTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateTimeField()),
                ('amount', models.PositiveBigIntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paytimes', to='projects_api.project')),
            ],
        ),
        migrations.CreateModel(
            name='Parts',
            fields=[
                ('id', models.CharField(max_length=80, primary_key=True, serialize=False)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='part', to='projects_api.project')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField()),
                ('attrib', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empcounts', to='itapi.category', validators=[projects_api.models.validate_attrib])),
                ('ve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empcounts', to='projects_api.verifyexpert')),
            ],
        ),
    ]
