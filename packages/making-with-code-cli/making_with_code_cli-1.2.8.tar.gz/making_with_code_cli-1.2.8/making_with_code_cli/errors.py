class MWCError(Exception):
    pass

class CurriculumSiteNotAvailable(MWCError):
    def __init__(self, site_url, *args, **kwargs):
        msg = f"Error reading curriculum metadata from {site_url}"
        super().__init__(msg)

class GitServerNotAvailable(MWCError):
    def __init__(self, server_url, *args, **kwargs):
        msg = f"Error connecting to the git server at {server_url}"
        super().__init__(msg)

class MissingSetting(MWCError):
    def __init__(self, missing_setting):
        msg = f"Required setting {missing_setting} is missing. Please run mwc setup."
        super().__init__(msg)

class NoCurriculaAvailable(MWCError):
    pass
