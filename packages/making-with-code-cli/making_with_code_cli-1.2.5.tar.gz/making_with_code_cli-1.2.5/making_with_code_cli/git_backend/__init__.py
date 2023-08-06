from .github_backend import GithubBackend
from .github_org_backend import GithubOrgBackend
from .mwc_backend import MWCBackend

def get_backend(name):
    return {
        'github': GithubBackend,
        'github_org': GithubOrgBackend,
        'mwc': MWCBackend,
    }[name]
