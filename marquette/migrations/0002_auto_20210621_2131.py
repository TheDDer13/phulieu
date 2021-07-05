# Generated by Django 3.2.4 on 2021-06-21 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marquette', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sosanh',
            name='thongbao',
        ),
        migrations.AddField(
            model_name='sosanh',
            name='loai',
            field=models.CharField(choices=[('Cầu', 'Cầu'), ('Hộp nhỏ', 'Hộp nhỏ'), ('Hộp trung gian', 'Hộp trung gian'), ('Khay cài', 'Khay cài'), ('Màng co', 'Màng co'), ('Màng nhôm', 'Màng nhôm'), ('Màng viên đặt', 'Màng viên đặt'), ('Tem chính', 'Tem chính'), ('Tem phụ', 'Tem phụ'), ('Toa', 'Toa'), ('Tuýp', 'Tuýp'), ('Túi', 'Túi')], default='', max_length=64, verbose_name='Loại'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sosanh',
            name='thaydoi',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='thaydoi', to='marquette.thaydoi', verbose_name='Thay đổi'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='thaydoi',
            name='thongbao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='thongbao', to='marquette.thongbao', verbose_name='Thông báo'),
        ),
    ]
