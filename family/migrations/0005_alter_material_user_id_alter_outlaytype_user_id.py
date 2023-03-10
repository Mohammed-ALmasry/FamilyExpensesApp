# Generated by Django 4.1.1 on 2022-10-08 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0004_material_user_id_outlaytype_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='outlaytype',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outlaytype_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
