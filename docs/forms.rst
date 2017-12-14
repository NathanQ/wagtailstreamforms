Form Customisation
==================

Currently we have defined two different types of forms, one which just
enables saving the submission and one to additionally email the results of
the submission.

Custom basic form
-----------------

You can easily add your own all you have to do is create a model that
inherits from ``wagtailstreamforms.models.BaseForm`` add any additional fields or properties and
this will be added to the cms admin area.

Example:

.. code-block:: python

    from wagtailstreamforms.models import BaseForm

    class CustomForm(BaseForm):

        def process_form_submission(self, form):
            super().process_form_submission(form) # handles the submission saving
            # do your own stuff here

Custom email form
-----------------

If you want to inherit the additional email sending functionality then inherit from
``wagtailstreamforms.models.AbstractEmailForm``. The saving of the submission and sending of the email
is handled in the ``process_form_submission`` so be sure to call ``super`` if overriding that method.

Example:

.. code-block:: python

    from wagtailstreamforms.models import AbstractEmailForm

    class CustomEmailForm(AbstractEmailForm):
         """ As above with email sending. """

         def process_form_submission(self, form):
             super().process_form_submission(form) # handles the submission saving and emailing
             # do your own stuff here

Custom email form with content
------------------------------

Here is an example of an email form that has an additional ``RichTextField`` rendered with the form.
This is especially useful if your form is being rendered from the template tag and you dont want to slot it in a streamfield.

Model:

.. code-block:: python

   from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, FieldPanel
   from wagtail.wagtailcore.fields import RichTextField
   from wagtailstreamforms.models import AbstractEmailForm, BaseForm


   class EmailFormWithContent(AbstractEmailForm):
       """ A form with content that sends and email. """

       content = RichTextField(blank=True)

       content_panels = [
           FieldPanel('content', classname='full'),
       ]

       edit_handler = TabbedInterface([
           ObjectList(AbstractEmailForm.settings_panels, heading='General'),
           ObjectList(AbstractEmailForm.field_panels, heading='Fields'),
           ObjectList(AbstractEmailForm.email_panels, heading='Email Submission'),
           ObjectList(content_panels, heading='Content'),
       ])

Template:

.. code-block:: html

   {% load wagtailcore_tags %}
   <h2>{{ value.form.name }}</h2>
   {% if value.form.content %}
      <div class="form-content">{{ value.form.content|richtext }}</div>
   {% endif %}
   <form action="{{ value.form_action }}" method="post" novalidate>
       {% csrf_token %}
       {% for hidden in form.hidden_fields %}{{ hidden }}{% endfor %}
       {% for field in form.visible_fields %}
           {% include 'streamforms/partials/form_field.html' %}
       {% endfor %}
       <input type="submit" value="{{ value.form.submit_button_text }}">
   </form>

Custom form submission model
----------------------------

If you need to save additional data, you can use a custom form submission model. To do this, you need to:

* Define a model that extends ``wagtailstreamforms.models.AbstractFormSubmission``.
* Override the ``get_submission_class`` and ``process_form_submission`` methods in your form model.

Example:

.. code-block:: python

   import json

   from django.core.serializers.json import DjangoJSONEncoder
   from django.db import models
   from django.utils.translation import ugettext_lazy as _

   from wagtail.wagtailcore.models import Page
   from wagtailstreamforms.models import AbstractFormSubmission, BaseForm


   class CustomForm(BaseForm):
       """ A form that saves the current user and page. """

       def get_data_fields(self):
           data_fields = super().get_data_fields()
           data_fields += [
               ('user', _('User')),
               ('page', _('Page'))
           ]
           return data_fields

       def get_submission_class(self):
           return CustomFormSubmission

       def process_form_submission(self, form):
           if self.store_submission:
               self.get_submission_class().objects.create(
                   form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
                   form=self,
                   page=form.page,
                   user=form.user if not form.user.is_anonymous() else None
               )


   class CustomFormSubmission(AbstractFormSubmission):
       user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
       page = models.ForeignKey(Page)

       def get_data(self):
           form_data = super().get_data()
           form_data.update({
               'page': self.page,
               'user': self.user
           })
           return form_data

.. note:: Its important to note here that the ``form.page`` and ``form.user`` seen above are passed in via the
   ``before_serve_page`` hook ``wagtailstreamforms.wagtail_hooks.process_form``.

   If you want to use a different method of saving the form and you require these you will need to pass
   them in yourself when adding ``request.POST`` to the form.

   Example usage can be seen in :ref:`rst_provide_own_submission`

Reference
---------

.. autoclass:: wagtailstreamforms.models.BaseForm
   :members:


.. autoclass:: wagtailstreamforms.models.AbstractEmailForm
   :members:


.. autoclass:: wagtailstreamforms.models.AbstractFormSubmission
   :members:
