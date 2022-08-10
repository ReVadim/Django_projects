# Generated by Django 3.2.15 on 2022-08-10 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0003_additionalimage_advertisement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=30, verbose_name='author')),
                ('content', models.CharField(max_length=300, verbose_name='content')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='show on display?')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='to publish?')),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.advertisement', verbose_name='advertisement')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'ordering': ['created_at'],
            },
        ),
    ]