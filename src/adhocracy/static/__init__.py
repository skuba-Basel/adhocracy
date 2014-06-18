import os

from fanstatic import Library, Group, Resource
# external libraries
from js.jquery import jquery
from js.jquery_joyride import joyride
from js.socialshareprivacy import socialshareprivacy
from adhocracy.i18n import LOCALES


js_i18n = dict()

static_path = os.path.dirname(os.path.abspath(__file__))


# --[ twitter bootstrap ]---------------------------------------------------

bootstrap_library = Library('bootstrap', 'bootstrap', version="2.1.1")
bootstrap_js = Resource(bootstrap_library, 'js/bootstrap.js',
                        minified='js/bootstrap.min.js',
                        depends=[jquery])
bootstrap = Group([bootstrap_js])


# --[ stylesheets ]---------------------------------------------------------

stylesheets_library = Library('stylesheets', 'stylesheets')
style = Resource(stylesheets_library, 'adhocracy.css',
                 minified='min/adhocracy.css')
stylesheets = Group([style])

instance_stylesheets = {}
instance_themes = {}


def instance_stylesheet(key):
    if key not in instance_stylesheets:
        instance_stylesheets[key] = Resource(
            stylesheets_library,
            str('adhocracy_%s.css' % key),
            minified=str('min/adhocracy_%s.css' % key))
    return instance_stylesheets[key]


def instance_theme(key):
    if key not in instance_themes:
        instance_themes[key] = Resource(
            stylesheets_library,
            str('adhocracy_theme_%s.css' % key),
            minified=str('min/adhocracy_theme_%s.css' % key))
    return instance_themes[key]


# --[ jquery.autocomplete ]-------------------------------------------------

autocomplete_library = Library('autocomplete', 'javascripts', version="1.2.2")
autocomplete_js = Resource(autocomplete_library, 'jquery.autocomplete.min.js',
                           depends=[jquery])
autocomplete_css = Resource(autocomplete_library, 'jquery.autocomplete.css')
autocomplete = Group([autocomplete_js, autocomplete_css])


# --[ jquery.i18n ]---------------------------------------------------------

jquery_i18n_library = Library('jquery_i18n', 'javascripts', version='0.9.2')

jquery_i18n_js = Resource(jquery_i18n_library, 'jquery.i18n.js',
                          minified='jquery.i18n.min.js',
                          depends=[jquery])


# --[ other versioned libraries ]-------------------------------------------

placeholder_library = Library('placeholder', 'javascripts', version="2.0.7")
placeholder = Resource(placeholder_library, 'jquery.placeholder.js',
                       minified='jquery.placeholder.min.js',
                       depends=[jquery])

jquerytools_library = Library('jquerytools', 'javascripts', version="1.2.7")
jquerytools = Resource(jquerytools_library, 'jquery.tools.min.js',
                       depends=[jquery])


# --[ moment ]-------------------------------------------------------------

moment_library = Library('moment', 'javascripts/moment', version="2.7.0")
moment = Resource(moment_library, 'moment.js',
                  minified='moment.min.js')
js_i18n['moment'] = dict()
for _locale in LOCALES:
    moment_path = os.path.join(static_path, 'javascripts', 'moment')
    for locale in (str(_locale), _locale.language):
        filename = locale.lower().replace('_', '-') + '.js'
        if locale not in js_i18n['moment']:
            if os.path.exists(os.path.join(moment_path, filename)):
                js_i18n['moment'][locale] = Resource(
                    moment_library, filename, depends=[moment])


# --[ misc javascripts ]----------------------------------------------------

misc_library = Library('misc', 'javascripts')
elastic = Resource(misc_library, 'jquery.elastic.js',
                   depends=[jquery])
cycle = Resource(misc_library, 'jquery.multipleelements.cycle.min.js',
                 depends=[jquery])
modernizr = Resource(misc_library, 'modernizr.js',
                     depends=[jquery])
spectrum_css = Resource(misc_library, 'spectrum/spectrum.css')
spectrum = Resource(misc_library, 'spectrum/spectrum.js',
                    minified='spectrum/spectrum.min.js',
                    depends=[jquery, spectrum_css])
select_hierarchy = Resource(misc_library, 'jquery.select-hierarchy.js',
                            minified='jquery.select-hierarchy.min.js',
                            depends=[jquery])
openid_selector = Resource(misc_library, 'openid.js',
                           depends=[jquery])
js_uri = Resource(misc_library, 'Uri.min.js')


# --[ adhocracy ]-----------------------------------------------------------

adhocracy_library = Library('adhocracy', 'javascripts')
adhocracy = Resource(adhocracy_library, 'adhocracy.js',
                     depends=[jquery, bootstrap_js, elastic,
                              placeholder, modernizr, jquerytools,
                              openid_selector, js_uri, moment])


# --[ knockout ]------------------------------------------------------------

knockout_library = Library('knockoutjs', 'javascripts', version="2.2.1")
knockout_js = Resource(knockout_library, 'knockout.debug.js',
                       minified='knockout.js',
                       depends=[jquery])
knockout_mapping_js = Resource(knockout_library, 'knockout.mapping.debug.js',
                               minified='knockout.mapping.js',
                               depends=[knockout_js])
knockout = Group([knockout_js, knockout_mapping_js])
adhocracy_ko = Resource(adhocracy_library, 'adhocracy.ko.js',
                        depends=[adhocracy, knockout])


# --[ openlayers ]----------------------------------------------------------

openlayers_library = Library('openlayers', 'openlayers', version='2.13.1')
openlayers_js = Resource(openlayers_library, 'openlayers.js',
                         minified='openlayers.min.js',
                         depends=[jquery],
                         bottom=True)
openlayers_css = Resource(openlayers_library, 'theme/default/style.css')

openlayers = Group([openlayers_js, openlayers_css])


# --[ openlayers editor ]---------------------------------------------------

ole_library = Library('openlayers-editor', 'openlayers-editor',
                      version='1.0-beta3')
ole_lang_js = Resource(ole_library, 'lib/Editor/Lang/en.js',
                       depends=[openlayers_js])
ole_loader_js = Resource(ole_library, 'lib/loader.js',
                         depends=[openlayers_js])
ole_js = Resource(ole_library, 'ole.min.js',
                  depends=[openlayers_js],
                  bottom=True)
ole_css = Resource(ole_library, 'theme/geosilk/geosilk.css')
ole = Group([ole_js, ole_css])


# --[ misc geo branch only ]------------------------------------------------

jquery_ui_library = Library('jqueryui', 'jqueryui', version='1.8.21.1')

jquery_ui_js = Resource(jquery_ui_library, 'jquery-ui.custom.min.js',
                        depends=[jquery])
jquery_ui_css = Resource(jquery_ui_library, 'jquery-ui.custom.css')
jquery_ui = Group([jquery_ui_js, jquery_ui_css])

adhocracy_geo_js = Resource(adhocracy_library, 'adhocracy.geo.js',
                            depends=[adhocracy, knockout_js, openlayers_js],
                            bottom=True)


js_i18n['geo'] = dict()
js_path = os.path.join(static_path, 'javascripts')
for _locale in LOCALES:
    for locale in (str(_locale), _locale.language):
        filename = ('adhocracy.geo.i18n-%s.js' %
                    locale.lower().replace('_', '-'))
        if locale not in js_i18n['geo']:
            if os.path.exists(os.path.join(js_path, filename)):
                js_i18n['geo'][locale] = Resource(
                    adhocracy_library, filename, depends=[jquery_i18n_js],
                    bottom=True)
