=======================
librarian-contentfilter
=======================

For the content filter to populate it's fields, it needs a data source to fetch
the entries from. The data source is a simple JSON file with the following
structure:

    {
        "Region 1": ["Language 1", "Language 2"],
        "Region 2": ["Language 1", "Language 3", "Language 7"]
    }

The path of this JSON file needs to be specified in librarian's configuration
file under the `contentfilter.data_source_path` key, e.g.:

    [contentfilter]
    data_source_path = /path/to/filter.json

contentfilter will read this data source on application startup, and populate
the widgets in dashboard with the values found in it. When the configuration
is saved through the UI, the chosen options will be stored in the setup file
(`librarian.json`) and merged immediately into the global application
configuration under the `fsal.whitelist` key in the appropriate form required
by FSAL. The composed form of the chosen regions and languages is list of
relative paths, e.g.: `["Region 1/Language 1", "Region 1/Language 2"]`, which
is used by FSAL to whitelist file system entries.
