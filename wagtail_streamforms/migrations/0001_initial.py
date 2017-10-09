# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-09 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import multi_email_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('template_name', models.CharField(choices=[('streamforms/form_block.html', 'Default Form Template')], max_length=255, verbose_name='template')),
                ('submit_button_text', models.CharField(default='Submit', max_length=100)),
                ('store_submission', models.BooleanField(default=False)),
                ('add_recaptcha', models.BooleanField(default=False, help_text='Add a reCapcha field to the form.')),
                ('success_message', models.CharField(blank=True, help_text='An optional success message to show when the form has been successfully submitted', max_length=255)),
            ],
            options={
                'verbose_name': 'form',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices')),
                ('default_value', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('multiselect', 'Multiple select'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time'), ('regexfield', 'Regex validated field')], max_length=16, verbose_name='field type')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FormSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_data', models.TextField()),
                ('submit_time', models.DateTimeField(auto_now_add=True, verbose_name='submit time')),
            ],
            options={
                'verbose_name': 'form submission',
                'ordering': ['-submit_time'],
            },
        ),
        migrations.CreateModel(
            name='RegexFieldValidator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('regex', models.TextField()),
                ('error_message', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'regex validator',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BasicForm',
            fields=[
                ('baseform_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtail_streamforms.BaseForm')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtail_streamforms.baseform',),
        ),
        migrations.CreateModel(
            name='EmailForm',
            fields=[
                ('baseform_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtail_streamforms.BaseForm')),
                ('subject', models.CharField(max_length=255)),
                ('from_address', models.EmailField(max_length=254)),
                ('to_addresses', multi_email_field.fields.MultiEmailField()),
                ('message', models.TextField()),
                ('fail_silently', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtail_streamforms.baseform', models.Model),
        ),
        migrations.AddField(
            model_name='formsubmission',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtail_streamforms.BaseForm'),
        ),
        migrations.AddField(
            model_name='formfield',
            name='form',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='wagtail_streamforms.BaseForm'),
        ),
        migrations.AddField(
            model_name='formfield',
            name='regex_validator',
            field=models.ForeignKey(blank=True, help_text="Applicable only for the field type 'regex validated field'.", null=True, on_delete=django.db.models.deletion.PROTECT, to='wagtail_streamforms.RegexFieldValidator'),
        ),
    ]