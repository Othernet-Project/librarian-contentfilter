import json
import logging
import os

from librarian_core.exts import ext_container as exts


def load_data_source(source_path):
    """
    Return content filter data read from the passed in ``source_path``.
    """
    if not os.path.exists(source_path):
        return None
    try:
        with open(source_path, 'r') as ds_file:
            return json.load(ds_file)
    except Exception:
        logging.exception("Failed to load content filter data source.")
        return None


def get_saved_filters(config):
    """
    Return region and language information from passed in ``config``.
    """
    region = config.get('contentfilter.region')
    languages = config.get('contentfilter.languages')
    return (region, languages)


def get_languages_of(region, config):
    """
    Return list of languages belonging to passed in ``region``.
    """
    data_source = config['contentfilter.data_source']
    try:
        return data_source[region]
    except KeyError:
        return []


def set_fsal_whitelist(config):
    """
    Construct paths from the retrieved region and languages (if found)
    and publish an ``FSAL_WHITELIST`` event with the constructed paths
    as payload. The paths will be stored in the global config as well.
    """
    (region, languages) = get_saved_filters(config)
    if region and languages:
        paths = [os.path.join(region, lang) for lang in languages]
        config['fsal.whitelist'] = paths
        exts.events.publish('FSAL_WHITELIST', paths)
