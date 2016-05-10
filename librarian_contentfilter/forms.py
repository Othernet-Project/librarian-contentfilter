from bottle_utils import form
from bottle_utils.html import urlquote, urlunquote
from bottle_utils.i18n import lazy_gettext as _


def get_region_form(config):
    data_source = config['contentfilter.data_source']
    regions = data_source.keys()
    choices = zip(map(urlquote, regions), regions)

    class RegionForm(form.Form):
        region = form.SelectField(
            _("Region"),
            # Translators, error message when LNB type is incorrect
            validators=[form.Required(messages={
                'required': _('Invalid choice for region')
            })],
            choices=choices,
        )

        def postprocess_region(self, value):
            return urlunquote(value)

    return RegionForm
