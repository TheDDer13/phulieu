# Generated by Django 3.2.4 on 2021-06-23 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marquette', '0004_alter_sosanh_noidung'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sosanh',
            name='thongbao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='thongbaochitiet', to='marquette.thongbao', verbose_name='Thay đổi'),
        ),
    ]
