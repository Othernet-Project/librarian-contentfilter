from bottle import request
from bottle_utils.i18n import lazy_gettext as _

from librarian_dashboard.dashboard import DashboardPlugin

from .forms import get_region_form
from .helpers import get_languages_of, get_saved_filters


class ContentFilterDashboardPlugin(DashboardPlugin):
    # Translators, used as dashboard section title
    heading = _('Content Filter')
    name = 'contentfilter'

    def get_template(self):
        return '{}/dashboard'.format(self.name)

    def get_context(self):
        (region, languages) = get_saved_filters(request.app.config)
        region_languages = get_languages_of(region, request.app.config)
        form_cls = get_region_form(request.app.config)
        return dict(form=form_cls(dict(region=region)),
                    region=region,
                    region_languages=region_languages,
                    selected_languages=languages)
