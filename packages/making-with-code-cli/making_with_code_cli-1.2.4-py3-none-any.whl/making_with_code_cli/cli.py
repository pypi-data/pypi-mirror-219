import click
from pprint import pprint
from pathlib import Path
from subprocess import run, CalledProcessError
from importlib.metadata import metadata
import yaml
import toml
import os
import traceback
from making_with_code_cli.mwc_accounts_api import MWCAccountsAPI
from making_with_code_cli.styles import (
    address,
    question,
    info,
    debug as debug_fmt,
    confirm,
    error,
)
from making_with_code_cli.settings import (
    get_settings_path,
    read_settings, 
    iter_settings,
    write_settings,
)
from making_with_code_cli.cli_setup import (
    INTRO_MESSAGE,
    INTRO_NOTES,
    WORK_DIR_PERMISSIONS,
    Platform,
    choose_mwc_username,
    prompt_mwc_password,
    choose_work_dir,
    choose_mwc_site_url,
    choose_course,
    choose_editor,
    MWCShellConfig,
    InstallCurl,
    InstallHomebrew,
    InstallXCode,
    WriteShellConfig,
    InstallPython3,
    InstallPoetry,
    InstallGit,
    InstallTree,
    InstallVSCode,
    InstallImageMagick,
    InstallHttpie,
    InstallScipy,
    GitConfiguration,
)
from making_with_code_cli.curriculum import (
    get_curriculum,
)
from making_with_code_cli.git_backend import (
    get_backend,
)
from making_with_code_cli.git_wrapper import (
    in_repo,
)

@click.group()
def cli():
    "Command line interface for Making with Code"

@cli.command()
def version():
    "Print MWC version"
    version = metadata('making-with-code-cli')['version']
    click.echo(address("MWC " + version, preformatted=True))

@cli.command()
@click.option("--yes", is_flag=True, help="Automatically answer 'yes' to setup prompts")
@click.option("--teacher", is_flag=True, help="Install in teacher mode")
@click.option("--config", help="Path to config file (default: ~/.mwc)")
@click.option("--debug", is_flag=True, help="Show debug-level output")
@click.pass_context
def setup(ctx, yes, teacher, config, debug):
    """Set up the MWC command line interface"""
    settings = read_settings(config)
    if debug:
        sp = get_settings_path(config)
        click.echo(debug_fmt(f"Reading settings from {sp}"))
    rc_tasks = []
    click.echo(address(INTRO_MESSAGE))
    for note in INTRO_NOTES:
        click.echo(address(note, list_format=True))
    click.echo()
    settings['mwc_username'] = choose_mwc_username(settings.get("mwc_username"))
    api = MWCAccountsAPI()
    if settings.get('mwc_accounts_token'):
        try:
            status = api.get_status(settings['mwc_accounts_token'])
        except api.RequestFailed as bad_token:
            token = prompt_mwc_password(settings['mwc_username'])
            settings['mwc_accounts_token'] = token
            status = api.get_status(token)
    else:
        token = prompt_mwc_password(settings['mwc_username'])
        settings['mwc_accounts_token'] = token
        status = api.get_status(token)
    settings['mwc_git_token'] = status['git_token']
    settings['role'] = "teacher" if teacher else "student"
    settings['work_dir'] = str(choose_work_dir(settings.get("work_dir")).resolve())
    settings['mwc_site_url'] = choose_mwc_site_url(settings.get('mwc_site_url'))
    curriculum = get_curriculum(settings)
    settings['course'] = choose_course(
        [course['name'] for course in curriculum['courses']], 
        default=settings.get('course')
    )
    course = [c for c in curriculum['courses'] if c['name'] == settings['course']][0]
    if Platform.detect() & (Platform.MAC | Platform.UBUNTU):
        settings['editor'] = choose_editor(settings.get('editor', 'code'))
    G = get_backend(course['git_backend'])
    settings = G.extend_settings(settings)
    if yes:
        click.echo(info("Updated settings:"))
        click.echo(info(yaml.dump(settings), preformatted=True))
    else:
        click.echo(info(yaml.dump(settings), preformatted=True))
        click.confirm(
            question("Do these settings look ok?"),
            abort=True
        )
    write_settings(settings, config)

    tasks = [
        MWCShellConfig(settings),
        InstallCurl(settings),
        InstallHomebrew(settings),
        InstallXCode(settings),
        InstallPoetry(settings),
        WriteShellConfig(settings),
        InstallPython3(settings),
        InstallGit(settings),
        InstallTree(settings),
        InstallVSCode(settings),
        InstallImageMagick(settings),
        InstallHttpie(settings),
        InstallScipy(settings),
        GitConfiguration(settings),
    ]
    errors = []
    for task in tasks:
        try:
            task.run_task_if_needed()
        except Exception as e:
            errors.append((task, traceback.format_exc()))
    if errors:
        click.echo(error(f"{len(errors)} setup tasks failed:"))
        for task, tb in errors:
            click.echo(error(task.description))
            if debug:
                click.echo(debug_fmt(tb, preformatted=True))
    else:
        ctx.invoke(update, config=config)

def get_course_by_name(name, courses):
    for course in courses:
        if course['name'] == name:
            return course

@cli.command()
@click.option("--config", help="Path to config file (default: ~/.mwc)")
def update(config):
    """Update the MWC work directory"""
    settings = read_settings(config)
    if not settings:
        click.echo(error(f"Please run mwc setup first."))
        return
    curr = get_curriculum(settings)
    course = [c for c in curr['courses'] if c['name'] == settings['course']][0]
    backend = course['git_backend']
    G = get_backend(backend)(settings)
    mwc_home = Path(settings["work_dir"])
    mwc_home.mkdir(mode=WORK_DIR_PERMISSIONS, parents=True, exist_ok=True)
    course = get_course_by_name(settings['course'], curr['courses'])
    if course is None:
        click.echo(error(f"Error: You are enrolled in {settings['course']}, but this course is not available. Please run mwc setup again."))
        return 
    course_dir = mwc_home / course['slug']
    course_dir.mkdir(mode=WORK_DIR_PERMISSIONS, exist_ok=True)
    for unit in course['units']:
        unit_dir = course_dir / unit['slug']
        unit_dir.mkdir(mode=WORK_DIR_PERMISSIONS, exist_ok=True)
        for module in unit['modules']:
            module_dir = unit_dir / module['slug']
            if module_dir.exists():
                try:
                    G.update(module, module_dir)
                except Exception as e:
                    msg =  traceback.format_exception(type(e), e, e.__traceback__)
                    print(error(''.join(msg)))
            else:
                rel_dir = module_dir.resolve().relative_to(mwc_home)
                click.echo(confirm(f"Initializing {module['slug']} at {rel_dir}."))
                click.echo(confirm(f"See {module['url']} for details."))
                try:
                    G.init_module(module, module_dir)
                except Exception as e:
                    msg =  traceback.format_exception(type(e), e, e.__traceback__)
                    click.echo(error(''.join(msg)))

@cli.command()
def submit():
    """Submit your work.
    (This is a wrapper for the basic git workflow.)
    """
    if in_repo():
        try:
            result = run("git diff", shell=True, capture_output=True, text=True, check=True)
            if not result.stdout:
                click.echo(info("Everything is already up to date."))
                return
            run("git diff", shell=True, check=True)
            if click.confirm(address("Here are the current changes. Looks OK?")):
                run("git add -A", shell=True, capture_output=True, check=True)
                click.echo(info("Write your commit message, then save and exit the window..."))
                run("git commit", shell=True, capture_output=True, check=True)
                run("git push", shell=True, capture_output=True, check=True)
                click.echo(address("Nice job! All your work in this module has been submitted."))
            else:
                click.echo(info("Cancelled the submit for now."))
        except CalledProcessError:
            click.echo(info("Everything is already up to date."))
    else:
        click.echo(error("You are not in a lab, problem set, or project folder."))





