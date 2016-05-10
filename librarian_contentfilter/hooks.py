from .dashboard_plugin import ContentFilterDashboardPlugin
from .helpers import load_data_source, set_fsal_whitelist


def initialize(supervisor):
    source_path = supervisor.config['contentfilter.data_source']
    data_source = load_data_source(source_path)
    # do not register dashboard plugin if there is not data source
    if data_source:
        supervisor.config['contentfilter.data_source'] = data_source
        supervisor.exts.dashboard.register(ContentFilterDashboardPlugin)
        set_fsal_whitelist(supervisor.config)
