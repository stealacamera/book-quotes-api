# Generated by Django 4.1.1 on 2022-09-14 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_alter_author_name_alter_book_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='book',
            new_name='source',
        ),
    ]
