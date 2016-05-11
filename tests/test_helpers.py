try:
    import __builtin__ as builtins
except ImportError:
    import builtins

import mock
import pytest

import librarian_contentfilter.helpers as mod


@mock.patch.object(builtins, 'open')
@mock.patch.object(mod.os.path, 'exists')
def test_load_data_source_missing(exists, open_fn):
    exists.return_value = False
    assert mod.load_data_source('path') is None
    assert not open_fn.called


@mock.patch.object(builtins, 'open')
@mock.patch.object(mod.os.path, 'exists')
def test_load_data_source_failed(exists, open_fn):
    exists.return_value = True
    open_fn.side_effect = IOError()
    assert mod.load_data_source('path') is None


@mock.patch.object(builtins, 'open')
@mock.patch.object(mod.json, 'load')
@mock.patch.object(mod.os.path, 'exists')
def test_load_data_source(exists, load, open_fn):
    exists.return_value = True
    load.return_value = {'region1': ['lang1', 'lang2'],
                         'region2': ['lang3', 'lang4']}
    assert mod.load_data_source('path') == load.return_value
    open_fn.assert_called_once_with('path', 'r')


def test_get_saved_filters():
    config = {'contentfilter.region': 'region1',
              'contentfilter.languages': ['lang2']}
    assert mod.get_saved_filters(config) == ('region1', ['lang2'])


@pytest.mark.parametrize('region,config,expected', [
    (
        'region1',
        {'contentfilter.data_source': {'region1': ['l1', 'l2']}},
        ['l1', 'l2']
    ), (
        'regionx',
        {'contentfilter.data_source': {}},
        []
    ),
])
def test_get_languages_of(region, config, expected):
    assert mod.get_languages_of(region, config) == expected


@pytest.mark.parametrize('ret_val', [
    (None, None),
    (None, 1),
    (1, None),
])
@mock.patch.object(mod, 'exts')
@mock.patch.object(mod, 'get_saved_filters')
def test_set_fsal_whitelist_noop(get_saved_filters, exts, ret_val):
    get_saved_filters.return_value = ret_val
    mod.set_fsal_whitelist({})
    assert not exts.events.publish.called


@mock.patch.object(mod, 'exts')
@mock.patch.object(mod, 'get_saved_filters')
def test_set_fsal_whitelist(get_saved_filters, exts):
    config = {}
    get_saved_filters.return_value = ('region', ['l1', 'l2'])
    mod.set_fsal_whitelist(config)
    expected = ['region/l1', 'region/l2']
    exts.events.publish.assert_called_once_with('FSAL_WHITELIST', expected)
    assert config['fsal.whitelist'] == expected
