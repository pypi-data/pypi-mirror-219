from optim_esm_tools.config import config

_SECONDS_TO_YEAR = int(config['constants']['seconds_to_year'])
_FOLDER_FMT = config['CMIP_files']['folder_fmt'].split()
_CMIP_HANDLER_VERSION = config['versions']['cmip_handler']
