import re
from django.conf.urls.defaults import *

__author__ = 'darvin'

from views import *



def get_crud_url_for_model(prefix, model_name, model, form_class=None, create_view=None, list_view=None, update_view=None, delete_view=None, create_ajax_view=None, update_ajax_view=None):
    if create_view is None:
        create_view = CRUDCreateView.as_view(model=model, form_class=form_class)
    if list_view is None:
        list_view = CRUDListView.as_view(model=model)
    if delete_view is None:
        delete_view = CRUDDeleteView.as_view(model=model)
    if update_view is None:
        update_view = CRUDUpdateView.as_view(model=model, form_class=form_class)

    if create_ajax_view is None:
        create_ajax_view = CRUDCreateAjaxView.as_view(model=model, form_class=form_class)

    if update_ajax_view is None:
        update_ajax_view = CRUDUpdateAjaxView.as_view(model=model, form_class=form_class)

    #fixme
    dump_view = CRUDDumpView.as_view(model=model)
    load_view = CRUDLoadView.as_view(model=model)
    return (
            url(r'%s%s/create/$' % (re.escape(prefix.lstrip('/')), model_name), create_view, name='crud_%s_create'%model_name),
            url(r'%s%s/(?P<pk>\w+)/update/$' % (re.escape(prefix.lstrip('/')), model_name), update_view, name='crud_%s_update'%model_name),
            url(r'%s%s/create.ajax/$' % (re.escape(prefix.lstrip('/')), model_name), create_ajax_view, name='crud_%s_create.ajax'%model_name),
            url(r'%s%s/(?P<pk>\w+)/update.ajax/$' % (re.escape(prefix.lstrip('/')), model_name), update_ajax_view, name='crud_%s_update.ajax'%model_name),

            url(r'%s%s/(?P<pk>\w+)/delete/$' % (re.escape(prefix.lstrip('/')), model_name), delete_view, name='crud_%s_delete'%model_name),
            url(r'%s%s/$' % (re.escape(prefix.lstrip('/')), model_name) , list_view, name='crud_%s_list'%model_name),
            url(r'%s%s/dump.(?P<format>\w+)$' % (re.escape(prefix.lstrip('/')), model_name) , dump_view, name='crud_%s_dump'%model_name),
            url(r'%s%s/load_(?P<format>\w+)$' % (re.escape(prefix.lstrip('/')), model_name) , load_view, name='crud_%s_load'%model_name),
            )


def django_class_generic_crud_url_patterns(prefix, models):
    res = ['']
    for model in models:
        model_name = model.__name__.lower()
        res += get_crud_url_for_model(prefix, model_name, model)


    return patterns(*res)





def crud_url_pattern(prefix, model, form_class=None, create_view=None, list_view=None, update_view=None, delete_view=None):
    res = ['']




    model_name = model.__name__.lower()
    registered_cruds.add(model_name)

    res += get_crud_url_for_model(prefix, model_name, model, form_class, create_view, list_view, update_view, delete_view)

    return patterns(*res)

