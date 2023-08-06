import requests
import json
from making_with_code_cli.errors import CurriculumSiteNotAvailable

LIVE_RELOAD = '<script src="/livereload.js?port=1024&amp;mindelay=10"></script>'

def get_curriculum(settings):
    """Fetches curriculum metadata from the site url specified in settings.
    """
    url = settings["mwc_site_url"] + "/manifest"
    response = requests.get(url)
    if response.ok:
        text = response.text.strip(LIVE_RELOAD)
        return json.loads(text)
    else:
        raise CurriculumSiteNotAvailable(settings["mwc_site_url"])
