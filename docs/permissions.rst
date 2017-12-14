Permissions
===========

Setting the level of access to administer your different types of forms is the
same as it is for any page. Your types of forms will appear in the groups section of
the wagtail admin > settings area.

Here you can assign the usual add, change and delete permissions.

.. note::
   Its worth noting here that if you do delete a form it will also delete all submissions
   for that form.

Form submission permissions
---------------------------

Because the form submission models are not listed in the admin area the following statement applies.

.. important::
   If you can either add, change or delete a form type then you can view all of its submissions.
   However to be able to delete the submissions, it requires that you can delete the form type.