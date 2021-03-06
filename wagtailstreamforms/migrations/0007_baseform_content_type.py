# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 00:20
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import migrations, models
from django.db.models.fields.related import OneToOneRel
import wagtailstreamforms.models.form


def set_content_types(apps, schema_editor):
    BaseForm = apps.get_model("wagtailstreamforms", "BaseForm")
    db_alias = schema_editor.connection.alias

    all_classes = [f for f in BaseForm._meta.get_fields() if isinstance(f, OneToOneRel)]

    for klass in all_classes:
        model_class = klass.related_model
        if hasattr(model_class, 'content_type'):
            content_type = ContentType.objects.get_for_model(model_class)
            model_class.objects.using(db_alias).all().update(content_type=content_type)


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailstreamforms', '0006_emailform_to_addresses_help_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseform',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=models.SET(wagtailstreamforms.models.form.get_default_form_content_type), related_name='streamforms', to='contenttypes.ContentType', verbose_name='content type'),
            preserve_default=False,
        ),
        migrations.RunPython(set_content_types)
    ]
