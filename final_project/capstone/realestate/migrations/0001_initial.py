# Generated by Django 5.1.3 on 2024-12-03 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='development',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='developments')),
                ('brochurePaper', models.FileField(upload_to='developments_pdfs/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'development',
                'verbose_name_plural': 'developments',
            },
        ),
    ]
