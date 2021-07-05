# Generated by Django 3.2.4 on 2021-06-23 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marquette', '0002_auto_20210621_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sosanh',
            name='thaydoi',
        ),
        migrations.AddField(
            model_name='sosanh',
            name='thongbao',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='thongbaochitiet', to='marquette.thaydoi', verbose_name='Thay đổi'),
            preserve_default=False,
        ),
    ]
