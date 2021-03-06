import logging

import formencode
from formencode import htmlfill, validators, Invalid

from pylons import request, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons.i18n import _

from adhocracy import forms
from adhocracy import i18n
from adhocracy.lib import helpers
from adhocracy.lib.auth import guard, csrf
from adhocracy.lib.base import BaseController
from adhocracy.lib.staticpage import (get_static_page, get_backend,
                                      render_body)
from adhocracy.lib.templating import render, ret_abort

log = logging.getLogger(__name__)

guard_perms = guard.perm("global.admin")


class EditForm(formencode.Schema):
    allow_extra_fields = True

    title = validators.String()
    body = validators.String()


class NewForm(EditForm):
    key = forms.StaticPageKey()
    lang = validators.OneOf(set(i18n.all_languages()))


class StaticController(BaseController):

    identifier = "staticpages"

    @guard_perms
    def index(self):
        try:
            data = {
                'static_pages': get_backend().all()
            }
            return render('/static/index.html', data)
        except NotImplementedError:
            abort(404)

    @guard_perms
    def new(self, errors=None, format=u'html'):
        data = {
            'all_language_infos': list(i18n.all_language_infos())
        }
        defaults = dict(request.params)
        defaults['_tok'] = csrf.token_id()
        return htmlfill.render(render('/static/new.html', data,
                                      overlay=format == u'overlay'),
                               defaults=defaults, errors=errors)

    @guard_perms
    @csrf.RequireInternalRequest(methods=['POST'])
    def make_new(self):
        try:
            form_result = NewForm().to_python(request.params)
        except Invalid as i:
            return self.new(errors=i.unpack_errors())

        key = form_result.get('key')
        lang = form_result.get('lang')

        backend = get_backend()
        if backend.get(key, lang) is not None:
            msg = _('Page does already exist. Select another key or language.')
            helpers.flash(msg, 'error')
            return self.new()

        backend.create(key,
                       lang,
                       form_result.get('body'),
                       form_result.get('title'))
        helpers.flash(_('Page updated'), 'notice')
        return redirect(helpers.base_url('/static'))

    @guard_perms
    def edit(self, key, lang, errors=None, format=u'html'):
        backend = get_backend()
        sp = backend.get(key, [lang])
        if not sp:
            return ret_abort(_('Cannot find static page to edit'), code=404)
        data = {'staticpage': sp}
        defaults = {
            'title': sp.title,
            'body': sp.body,
        }
        defaults.update(dict(request.params))
        defaults['_tok'] = csrf.token_id()
        return htmlfill.render(render('/static/edit.html', data,
                                      overlay=format == u'overlay'),
                               defaults=defaults, errors=errors)

    @guard_perms
    @csrf.RequireInternalRequest(methods=['POST'])
    def update(self, key, lang):
        backend = get_backend()
        sp = backend.get(key, [lang])
        if not sp:
            return ret_abort(_('Cannot find static page to edit'), code=404)

        try:
            form_result = EditForm().to_python(request.params)
        except Invalid as i:
            return self.edit(errors=i.unpack_errors())

        sp.title = form_result.get('title')
        sp.body = form_result.get('body')
        sp.commit()
        helpers.flash(_('Page updated'), 'notice')
        return redirect(helpers.base_url('/static'))

    @guard.perm('static.show')
    def serve(self, key, format='html'):
        page = get_static_page(key)
        if page is None:
            return abort(404, _('The requested page was not found'))
        c.body_css_classes += page.css_classes
        if page.redirect_url != u'':
            return redirect(page.redirect_url)
        data = {
            'static': page,
            'body_html': render_body(page.body),
            'active_global_nav': key,
        }

        if format == 'simple':
            return render('/plain_doc.html', data)
        elif format == 'overlay':
            return render('/static/show.html', data, overlay=True)
        else:
            return render('/static/show.html', data)
