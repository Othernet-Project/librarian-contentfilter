import mock

import librarian_contentfilter.routes as mod

from helpers import strip_wrappers


@mock.patch.object(mod, 'get_region_form')
@mock.patch.object(mod, 'get_saved_filters')
@mock.patch.object(mod, 'request')
def test_regions_handler(request, get_saved_filters, get_region_form):
    unwrapped = strip_wrappers(mod.regions_handler)
    get_saved_filters.return_value = ('region1', ['l1'])
    form = get_region_form.return_value.return_value
    assert unwrapped() == dict(region='region1', form=form)


@mock.patch.object(mod, 'get_region_form')
@mock.patch.object(mod, 'get_saved_filters')
@mock.patch.object(mod, 'request')
def test_regions_handler_form(request, get_saved_filters, get_region_form):
    unwrapped = strip_wrappers(mod.regions_handler)
    get_saved_filters.return_value = ('region1', ['l1'])
    form = 'test'
    assert unwrapped(form) == dict(region='region1', form=form)


@mock.patch.object(mod, 'regions_handler')
@mock.patch.object(mod, 'get_region_form')
@mock.patch.object(mod, 'request')
def test_languages_handler_invalid_region(request, get_region_form,
                                          regions_handler):
    # set up mocked form
    get_region_form.return_value.return_value.is_valid.return_value = False
    unwrapped = strip_wrappers(mod.languages_handler)
    assert unwrapped() == regions_handler.return_value


@mock.patch.object(mod, 'get_languages_of')
@mock.patch.object(mod, 'get_region_form')
@mock.patch.object(mod, 'request')
def test_languages_handler_get_languages(request, get_region_form,
                                         get_languages_of):
    request.method = 'GET'
    unwrapped = strip_wrappers(mod.languages_handler)
    form = get_region_form.return_value.return_value
    form.processed_data = {'region': 'region1'}
    ret = unwrapped()
    assert ret['region'] == 'region1'
    assert ret['region_languages'] == get_languages_of.return_value
    assert ret['selected_languages'] == []


@mock.patch.object(mod, 'get_languages_of')
@mock.patch.object(mod, 'get_region_form')
@mock.patch.object(mod, 'request')
def test_languages_handler_invalid(request, get_region_form, get_languages_of):
    request.forms.getall.return_value = ['Quoted%20Value', 'English']
    get_languages_of.return_value = ['English', 'Russian']
    form = get_region_form.return_value.return_value
    form.processed_data = {'region': 'region1'}
    unwrapped = strip_wrappers(mod.languages_handler)
    ret = unwrapped()
    assert ret['region'] == 'region1'
    assert ret['region_languages'] == get_languages_of.return_value
    assert ret['selected_languages'] == ['Quoted Value', 'English']


@mock.patch.object(mod, 'set_fsal_whitelist')
@mock.patch.object(mod, 'exts')
@mock.patch.object(mod, 'get_languages_of')
@mock.patch.object(mod, 'get_region_form')
@mock.patch.object(mod, 'request')
def test_languages_handler_saved(request, get_region_form, get_languages_of,
                                 exts, set_fsal_whitelist):
    request.forms.getall.return_value = ['Quoted%20Value', 'English']
    get_languages_of.return_value = ['English', 'Quoted Value']
    form = get_region_form.return_value.return_value
    form.processed_data = {'region': 'region1'}
    unwrapped = strip_wrappers(mod.languages_handler)
    ret = unwrapped()
    exts.setup.append.assert_called_once_with({
        'contentfilter.region': 'region1',
        'contentfilter.languages': [u'Quoted Value', u'English']
    })
    set_fsal_whitelist.assert_called_once_with(request.app.config)
    assert ret['region'] == 'region1'
    assert ret['region_languages'] == get_languages_of.return_value
    assert ret['selected_languages'] == ['Quoted Value', 'English']
    assert 'redirect_url' in ret

