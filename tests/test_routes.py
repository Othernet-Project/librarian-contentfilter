import mock
import pytest

import librarian_contentfilter.routes as mod

from helpers import strip_wrappers


@mock.patch.object(mod, 'get_languages_of')
@mock.patch.object(mod, 'get_region_form')
@mock.patch.object(mod, 'get_saved_filters')
@mock.patch.object(mod, 'request')
def test_regions_handler(request, get_saved_filters, get_region_form,
                         get_languages_of):
    unwrapped = strip_wrappers(mod.regions_handler)
    get_saved_filters.return_value = ('region1', ['l1'])
    form = get_region_form.return_value.return_value
    assert unwrapped() == dict(region='region1',
                               region_languages=get_languages_of.return_value,
                               selected_languages=['l1'],
                               form=form)


@mock.patch.object(mod, 'get_languages_of')
@mock.patch.object(mod, 'get_region_form')
@mock.patch.object(mod, 'get_saved_filters')
@mock.patch.object(mod, 'request')
def test_regions_handler_form(request, get_saved_filters, get_region_form,
                              get_languages_of):
    unwrapped = strip_wrappers(mod.regions_handler)
    get_saved_filters.return_value = ('region1', ['l1'])
    region_languages = get_languages_of.return_value
    form = 'test'
    assert unwrapped(form) == dict(region='region1',
                                   region_languages=region_languages,
                                   selected_languages=['l1'],
                                   form=form)


@mock.patch.object(mod, 'regions_handler')
@mock.patch.object(mod, 'get_region_form')
@mock.patch.object(mod, 'request')
def test_validate_region_fail(request, get_region_form, regions_handler):
    form = get_region_form.return_value.return_value
    form.is_valid.return_value = False
    with pytest.raises(mod.HTTPResponse):
        mod.validate_region()
    regions_handler.assert_called_once_with(form=form)


@mock.patch.object(mod, 'get_languages_of')
@mock.patch.object(mod, 'get_region_form')
@mock.patch.object(mod, 'request')
def test_validate_region_success(request, get_region_form, get_languages_of):
    form = get_region_form.return_value.return_value
    form.processed_data = {'region': 'region1'}
    expected = (form, 'region1', get_languages_of.return_value)
    assert mod.validate_region() == expected
    get_languages_of.assert_called_once_with('region1', request.app.config)


@mock.patch.object(mod, 'validate_region')
def test_languages_list(validate_region):
    form = mock.Mock()
    validate_region.return_value = (form, 'region1', ['l1', 'l2'])
    unwrapped = strip_wrappers(mod.languages_list)
    ret = unwrapped()
    assert ret['region'] == 'region1'
    assert ret['region_languages'] == ['l1', 'l2']
    assert ret['selected_languages'] == []
    assert ret['form'] is form


@mock.patch.object(mod, 'validate_region')
@mock.patch.object(mod, 'request')
def test_languages_save_invalid(request, validate_region):
    form = mock.Mock()
    validate_region.return_value = (form, 'region1', ['English', 'Russian'])
    request.forms.getall.return_value = ['Quoted%20Value', 'English']
    unwrapped = strip_wrappers(mod.languages_save)
    ret = unwrapped()
    assert ret['region'] == 'region1'
    assert ret['region_languages'] == ['English', 'Russian']
    assert ret['selected_languages'] == ['Quoted Value', 'English']
    assert ret['form'] is form


@mock.patch.object(mod, 'set_fsal_whitelist')
@mock.patch.object(mod, 'validate_region')
@mock.patch.object(mod, 'exts')
@mock.patch.object(mod, 'request')
def test_languages_handler_saved(request, exts, validate_region,
                                 set_fsal_whitelist):
    form = mock.Mock()
    validate_result = (form, 'region1', ['English', 'Quoted Value'])
    validate_region.return_value = validate_result
    request.forms.getall.return_value = ['Quoted%20Value', 'English']
    unwrapped = strip_wrappers(mod.languages_save)
    ret = unwrapped()
    exts.setup.append.assert_called_once_with({
        'contentfilter.region': 'region1',
        'contentfilter.languages': [u'Quoted Value', u'English']
    })
    set_fsal_whitelist.assert_called_once_with(request.app.config)
    assert ret['region'] == 'region1'
    assert ret['region_languages'] == ['English', 'Quoted Value']
    assert ret['selected_languages'] == ['Quoted Value', 'English']
    assert 'redirect_url' in ret
