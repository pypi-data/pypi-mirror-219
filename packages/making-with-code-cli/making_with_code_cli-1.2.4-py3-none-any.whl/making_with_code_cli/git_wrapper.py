from subprocess import run, CalledProcessError
from making_with_code_cli.helpers import cd

def in_repo():
    """Checks whether currently in repo"""
    try:
        run("git status", shell=True, capture_output=True, check=True)
        return True
    except CalledProcessError:
        return False


    
