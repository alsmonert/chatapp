# Generated by Django 4.2 on 2023-04-06 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenericFileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_upload', models.FileField(upload_to='')),
                ('createed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
