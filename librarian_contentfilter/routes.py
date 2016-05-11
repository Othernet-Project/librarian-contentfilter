from bottle import request
from bottle_utils.ajax import roca_view
from bottle_utils.html import urlunquote
from bottle_utils.i18n import lazy_gettext as _, i18n_url

from librarian_core.contrib.templates.renderer import template
from librarian_core.exts import ext_container as exts

from .forms import get_region_form
from .helpers import get_languages_of, get_saved_filters, set_fsal_whitelist


@roca_view('contentfilter/regions',
           'contentfilter/_regions',
           template_func=template)
def regions_handler(form=None):
    (region, _) = get_saved_filters(request.app.config)
    form_cls = get_region_form(request.app.config)
    form = form_cls(dict(region=region)) if form is None else form
    return dict(form=form, region=region)


@roca_view('contentfilter/languages',
           'contentfilter/_languages',
           template_func=template)
def languages_handler():
    # TODO: when class based route handlers enter the game, convert this too
    # region must be set for both get and post requests
    form_cls = get_region_form(request.app.config)
    form = form_cls(request.params)
    if not form.is_valid():
        # invalid region selected, go back to region selection form
        return regions_handler(form=form)
    # get list of languages for selected region
    region = form.processed_data['region']
    region_languages = get_languages_of(region, request.app.config)
    if request.method == 'GET':
        # initial language form load, requests the list of available languages
        return dict(region=region,
                    region_languages=region_languages,
                    selected_languages=[],
                    # Translators, message displayed as help text for
                    # language selection
                    message=_("Please select languages from the list below."))
    # languages were chosen for the selected region
    selected_languages = map(urlunquote, request.forms.getall('language'))
    has_invalid = any(lang not in region_languages
                      for lang in selected_languages)
    if not selected_languages or has_invalid:
        # some of the chosen languages were invalid or no languages were chosen
        return dict(region=region,
                    region_languages=region_languages,
                    selected_languages=selected_languages,
                    # Translators, message displayed as help text for
                    # language selection
                    message=_("Please select languages from the list below."))
    # languages are valid, store them in setup file and inform other about it
    exts.setup.append({'contentfilter.region': region,
                       'contentfilter.languages': selected_languages})
    set_fsal_whitelist(request.app.config)
    return dict(region=region,
                region_languages=region_languages,
                selected_languages=selected_languages,
                message=_("Content filter has been set."),
                redirect_url=i18n_url('dashboard:main'))


def routes(config):
    if not config['contentfilter.data_source']:
        return ()
    return (
        ('contentfilter:regions', regions_handler,
         'GET', '/contentfilter/regions/', {}),
        ('contentfilter:languages', languages_handler,
         ['GET', 'POST'], '/contentfilter/languages/', {}),
    )
