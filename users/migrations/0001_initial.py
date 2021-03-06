# Generated by Django 3.2 on 2021-10-20 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('itapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commis',
            fields=[
                ('id', models.PositiveSmallIntegerField(default=1, editable=False, primary_key=True, serialize=False)),
                ('visitor', models.PositiveSmallIntegerField()),
                ('cityadmin', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yellow_cards', models.PositiveIntegerField(default=0)),
                ('approved', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='itapi.category')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employee', to='itapi.city')),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('status', models.CharField(choices=[('ns', 'noot_seen'), ('np', 'not_approved'), ('ap', 'approved')], default='ns', max_length=3)),
                ('reason', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.CharField(max_length=40, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yellow_cards', models.PositiveIntegerField(default=0)),
                ('approved', models.BooleanField(default=False)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='visitor', to='itapi.city')),
                ('resume', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visitor', to='users.resume')),
                ('wallet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.wallet')),
            ],
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yellow_cards', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='experts', to='itapi.category')),
                ('employee', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expert', to='users.employee')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='resume',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee', to='users.resume'),
        ),
        migrations.AddField(
            model_name='employee',
            name='wallet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='users.wallet'),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='customer', to='itapi.city')),
                ('wallet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.wallet')),
            ],
        ),
        migrations.CreateModel(
            name='CityAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission', models.PositiveSmallIntegerField(default=3)),
                ('city', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='city_admin', to='itapi.city')),
                ('wallet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.wallet')),
            ],
        ),
    ]
