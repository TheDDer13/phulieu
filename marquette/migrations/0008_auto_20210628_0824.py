# Generated by Django 3.2.4 on 2021-06-28 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marquette', '0007_alter_thongbao_ngayhethancv'),
    ]

    operations = [
        migrations.AddField(
            model_name='thongbao',
            name='link',
            field=models.URLField(default='', verbose_name='Link bản mềm'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='xuly',
            name='chotxuly',
            field=models.CharField(choices=[('Đã chốt', 'Đã chốt'), ('Chưa chốt', 'Chưa chốt')], max_length=64, null=True, verbose_name='Tình trạng chốt'),
        ),
        migrations.AlterField(
            model_name='xuly',
            name='xuly',
            field=models.TextField(null=True, verbose_name='Hướng xử lý'),
        ),
        migrations.CreateModel(
            name='tongket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trangthai', models.CharField(choices=[('Mã cũ', 'Mã cũ'), ('Mã mới', 'Mã mới')], max_length=64)),
                ('chotsudung', models.CharField(choices=[('Có', 'Có'), ('Không', 'Không')], max_length=64, null=True, verbose_name='Chốt sử dụng')),
                ('tinhtrang', models.CharField(choices=[('Đủ', 'Đủ'), ('Không đủ', 'Không đủ')], max_length=64, null=True, verbose_name='Tình trạng')),
                ('ghichu', models.TextField(null=True, verbose_name='Ghi chú')),
                ('dauma', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='daumabanhanh', to='marquette.phulieu')),
                ('huongxuly', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='xulypending', to='marquette.xuly')),
                ('sanpham', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sanpham', to='marquette.sanpham')),
                ('thaydoi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='thaydoipending', to='marquette.thaydoi')),
            ],
        ),
    ]
