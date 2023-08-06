import json
import os
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn
from rich.prompt import Confirm
from rich.table import Table

from quicklab import defaults, dotenv, jupyter, utils
from quicklab.types import ProjectSettings, UserSettings
from quicklab.utils import get_class, get_user_setting, user_settings_path

console = Console()
progress = Progress(
    SpinnerColumn(),
    "[progress.description]{task.description}",
)

dotenv.default()


@click.group()
def cli():
    """
    quicklab command line
    """
    pass


@cli.command(name="configure")
@click.option(
    "--project-id",
    prompt=True,
    default=lambda: get_user_setting("project_id"),
    help="Project Id on cloud provider",
)
@click.option(
    "--dns-zone-id",
    prompt=True,
    default=lambda: get_user_setting("dns_zone_id", "main"),
    help="DNS Zone Id on cloud provider",
)
@click.option(
    "--state-bucket-name",
    help="Bucket name on cloud provider for remotely storing state",
)
@click.option(
    "--location",
    help="Default compute location on cloud provider",
)
def configure(
    project_id: Optional[str],
    dns_zone_id: str,
    state_bucket_name: Optional[str],
    location: Optional[str],
):
    """Configure Quicklab globally"""
    settings = utils.load_user_settings()

    if not state_bucket_name:
        # Prompt for state bucket name
        state_bucket_name = click.prompt(
            "State bucket name",
            default=get_user_setting("state_bucket_name", f"{project_id}-state"),
            type=str,
        )

    if not location:
        # Get locations
        click.echo(f"Listing locations...")
        provider = jupyter.VM_PROVIDERS["gce"]
        driver = get_class(provider)(defaults.QL_COMPUTE_KEY)
        locs = driver.driver.list_locations()
        locs = sorted(locs, key=lambda l: l.name)

        default_location = get_user_setting("location", "us-central1-a")
        default_country = default_location.split("-")[0]

        # Prompt for country to filter locations
        countries = sorted(set(loc.country for loc in locs))
        country = click.prompt(
            "Filter locations by country:",
            default=default_country,
            type=click.Choice(countries, case_sensitive=False),
        )

        locs = [loc for loc in locs if loc.country == country]

        # Build locations table and print
        table = Table()
        table.add_column("#", justify="right")
        table.add_column("location", justify="left")
        table.add_column("country", justify="right")
        for i, loc in enumerate(locs):
            table.add_row(str(i), loc.name, loc.country)
        console.print(table)

        # Prompt with a default location
        location_names = [loc.name for loc in locs]
        default_loc_id = (
            location_names.index(default_country)
            if default_country in location_names
            else 0
        )
        loc_id = click.prompt(
            "Location",
            type=click.IntRange(0, len(locs) - 1),
            default=default_loc_id,
            show_choices=False,
        )
        location = locs[loc_id].name

    settings = UserSettings(
        project_id=project_id,
        dns_zone_id=dns_zone_id,
        state_bucket_name=state_bucket_name,
        location=location,
    )

    # Print settings to confirm
    click.echo()
    console.print(utils.build_table_from_dict(settings.dict()))

    if click.confirm("Do you confirm?", default=True):
        utils.save_user_settings(settings)
        console.print(f"[green]Settings saved on {user_settings_path}[/]")


@cli.command(name="init")
@click.option("--name", "-n", help="Name of your project")
@click.option("--location", "-l", help="Compute location to be used")
def init(
    name,
    location,
):
    """Initialize a new project"""
    project_settings_path = utils.get_project_settings_path()
    if project_settings_path.is_file():
        console.print(
            (
                f"[red]A {defaults.QUICKLAB_CONF} already exist in the project. "
                "If you want to re-initialize it, delete the file first.[/]"
            )
        )
        raise click.Abort()

    user_settings = utils.load_user_settings()

    compute_provider = "gce"
    dns_provider = "gce"
    logs_provider = "gce"

    location = location or user_settings.location
    if not location:
        console.print(
            (
                f"[red]No location was specified nor configured as a user setting."
                "Please try running `configure` again or specify a location with --location/-l[/]"
            )
        )
        raise click.Abort()

    # Prompt for project name, with root dirname as default
    if not name:
        root_dirname = utils.slugify(utils.get_project_root_path().name)
        name = click.prompt("Project name", default=root_dirname)
    else:
        name = utils.slugify(name)

    project_settings = ProjectSettings(
        name=name,
        location=location,
        project_id=user_settings.project_id,
        dns_zone_id=user_settings.dns_zone_id,
        state_bucket_name=user_settings.state_bucket_name,
    )

    click.echo()
    console.print(utils.build_table_from_dict(project_settings.dict()))
    if not click.confirm("Do you confirm?", default=True):
        return

    utils.save_project_settings(project_settings)

    state_path = jupyter.get_project_state_path(
        state_bucket_name=user_settings.state_bucket_name, name=name
    )
    if jupyter.has_state(state_path):
        console.print(f"[red]{name} already exists on remote state bucket[/]")
        raise click.Abort()

    jupyter.init(
        name,
        compute_provider,
        dns_provider,
        location,
        user_settings.dns_zone_id,
        state_path,
        logs_provider=logs_provider,
    )
    console.print(
        f":smile_cat: Congratulations! [green]Quicklab project initialized[/]"
    )


@cli.command(name="up")
@click.option("--from-module", "-m", default=None, help="Create lab from module")
@click.option(
    "--from-file", "-f", default=None, help="Create lab from file [EXPERIMENTAL]"
)
# @click.option("--debug", "-d", default=False, is_flag=True, help="flag debug")
@click.option("--wait-timeout", default=None, help="Waiting timeout (in seconds)")
def up(from_module, from_file, wait_timeout):
    """Create a new session"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)

    if from_module:
        cfg = jupyter.load_conf_module(from_module)
    elif from_file:
        cfg = jupyter.load_conf_file(from_file)
    else:
        console.print(
            "[bold red]You should provide --from-file or --from-module param[/]"
        )
        raise click.Abort()

    with progress:
        task = progress.add_task("Creating a new session...")
        rsp = jup.create_lab(cfg.INSTANCE, volume=cfg.VOLUME)
        jup.push()

    console.print("=> [green]Session created[/]")
    console.print("Go to: ")
    console.print(f"\t [magenta]https://{rsp.url}[/]")
    console.print(f"\t Token: [red]{rsp.token}[/]")

    if wait_timeout:
        console.print("=> Waiting until the service is available...")
        code = -1
        with progress:
            task = progress.add_task("Checking readiness of Jupyter service")
            code = utils.check_readiness(rsp.url, int(wait_timeout))

        if code == 200:
            console.print("=> [green]Congratulations! Session is ready[/]")
        else:
            console.print(f"[orange] {rsp.url} still not available, code {code}[/]")


@cli.command(name="down")
def down():
    """Stop and destroy the current session"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    _confirm = Confirm.ask(
        f"Do you want to destroy this session? (Volumes will NOT be deleted)",
        default=False,
    )
    if _confirm:
        with progress:
            task = progress.add_task(f"[red]Destroying session at {jup._state.url}[/]")
            jup.destroy_lab()
            jup.push()


@cli.command(name="wait")
@click.option("--timeout", "-t", default=10 * 60, help="Timeout (in seconds)")
def wait_for_jupyter(timeout):
    """Wait for Jupyter to be ready"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    url = jup._state.url
    with progress:
        task = progress.add_task("Waiting for jupyter lab")
        code = utils.check_readiness(url, timeout)
    if code == 200:
        console.print(f"[green]{url} Ready[/]")
    else:
        console.print(f"[orange] {url} not avaialable, code: {code}[/]")


@cli.command(name="status")
@click.option("--output", "-o", default=None, help="Path to record state")
def show_state(output):
    """Shows state"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    state_dict = jup._state.dict()
    console.print_json(data=state_dict)
    if output:
        with open(output, "w") as f:
            f.write(json.dumps(state_dict))


@cli.command(name="logs")
@click.option("--lines", "-l", default=5, help="Max lines")
def logs(lines):
    """Show logs"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    logs = jup.list_logs(lines=lines)
    for log in logs:
        console.print(f"{log.timestamp} - {log.payload}")


if os.getenv("QL_OPS"):
    from quicklab.cli.ops import ops

    cli.add_command(ops)


if __name__ == "__main__":
    cli()
