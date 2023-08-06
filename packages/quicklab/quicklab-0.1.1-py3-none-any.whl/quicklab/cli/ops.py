import click
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

from quicklab import defaults, jupyter, utils
from quicklab.utils import get_class

console = Console()


@click.group()
def ops():
    """Commands for DevOps administration"""
    pass


@ops.group()
def volumes():
    """Volumes operations"""
    pass


@ops.group()
def snapshots():
    """Snapshots operations"""
    pass


@ops.command(name="list-containers")
@click.option("--project", "-p", default=None, help="cloud project id")
@click.option("--repo-name", "-n", default="repo", help="repo name")
@click.option("--location", "-l", default=None, help="location")
def list_containers(project, repo_name, location):
    """List containers"""
    from quicklab.providers.google.artifacts import Artifacts

    project_settings = utils.load_project_settings()
    user_settings = utils.load_user_settings()
    settings = project_settings or user_settings

    project = project or settings.project_id
    repo_name = repo_name or settings.repo_name
    location = location or settings.location

    if not project:
        console.print(
            f"[red]project is missing. Try re-configuring Quicklab or specify --project/-p."
        )
        raise click.Abort()

    if not repo_name:
        console.print(
            f"[red]repo_name is missing. Try re-configuring Quicklab or specify --repo-name/-n."
        )
        raise click.Abort()

    if not location:
        console.print(
            f"[red]location is missing. Try re-configuring Quicklab or specify --location/-l."
        )
        raise click.Abort()

    art = Artifacts(keyvar=defaults.QL_COMPUTE_KEY)
    containers = art.list_docker_images(
        repo_name=repo_name, project=project, location=location
    )

    table = Table(title=f"Containers")

    table.add_column("name", justify="left")
    table.add_column("tags", justify="right")
    table.add_column("size", justify="right")
    table.add_column("uri", justify="right")
    for con in containers:
        table.add_row(
            con.name,
            ",".join(con.tags),
            utils.convert_size(con.image_size_bytes),
            con.uri,
        )
    console.print(table)


@ops.command(name="list-instances")
@click.option(
    "--compute-provider",
    "-C",
    default="gce",
    help="Provider to be used for vm creation",
)
def list_instances(compute_provider):
    """List instances"""
    driver = get_class(jupyter.VM_PROVIDERS[compute_provider])()
    instances = driver.list_vms()
    table = Table(title=f"{compute_provider}'s nodes")

    table.add_column("instance", justify="left")
    table.add_column("status", justify="right")

    for vm in instances:
        table.add_row(vm.vm_name, vm.state)

    console.print(table)


@ops.command(name="list-providers")
@click.argument("kind", default="all", type=click.Choice(["dns", "compute", "all"]))
def list_provs(kind):
    """list compute and dns providers"""

    table = Table(title="Providers list")
    table.add_column("code", justify="left")
    table.add_column("kind", justify="right")

    if kind == "dns":
        for key in jupyter.DNS_PROVIDERS.keys():
            table.add_row(key, "dns")

    elif kind == "compute":
        for key in jupyter.VM_PROVIDERS.keys():
            table.add_row(key, "compute")
    elif kind == "all":
        for key in jupyter.VM_PROVIDERS.keys():
            table.add_row(key, "compute")
        for key in jupyter.DNS_PROVIDERS.keys():
            table.add_row(key, "dns")

    console.print(table)


@ops.command(name="list-dns")
@click.option("--dns-provider", "-D", default="gce", help="Provider to be used for dns")
def list_dns(dns_provider):
    """List DNS available by provider"""
    driver = get_class(jupyter.DNS_PROVIDERS[dns_provider])()
    zones = driver.list_zones()
    table = Table(title=f"DNS zones")

    table.add_column("dns id", justify="left")
    table.add_column("domain", justify="right")
    table.add_column("type", justify="right")

    for zone in zones:
        table.add_row(zone.id, zone.domain, zone.zone_type)

    console.print(table)


@ops.command(name="list-images")
@click.option(
    "--compute-provider",
    "-C",
    default="gce",
    help="Provider to be used for vm creation",
)
def list_images(compute_provider):
    """List images to be used as boot disk"""
    driver = get_class(jupyter.VM_PROVIDERS[compute_provider])()

    images = driver.driver.list_images()
    table = Table(title=f"{compute_provider}'s images")
    table.add_column("name", justify="left")

    for img in images:
        table.add_row(img.name)

    console.print(table)


@ops.command(name="list-vm-types")
@click.option(
    "--compute-provider",
    "-C",
    default="gce",
    help="Provider to be used for vm creation",
)
@click.option("--location", "-l", default=None, help="by location")
def list_vm_types(compute_provider, location):
    """List vm types"""
    driver = get_class(jupyter.VM_PROVIDERS[compute_provider])()

    types = driver.driver.list_sizes(location=location)
    table = Table(title=f"{compute_provider}'s vm types")
    table.add_column("name", justify="left")
    table.add_column("ram", justify="right")
    table.add_column("cpu", justify="right")

    for vm in types:
        _cpu = vm.extra["guestCpus"]
        _ram = f"{round(vm.ram/1024)} GB"
        table.add_row(vm.name, _ram, str(_cpu))

    console.print(table)


@ops.command(name="list-locations")
@click.option(
    "--compute-provider",
    "-C",
    default="gce",
    help="Provider to be used for vm creation",
)
@click.option("--filter-country", "-c", default=None, help="filter by country")
def list_locs(compute_provider, filter_country):
    """List locations related to a compute provider"""
    driver = get_class(jupyter.VM_PROVIDERS[compute_provider])()
    locs = driver.driver.list_locations()
    table = Table(title=f"{compute_provider}'s locations")

    table.add_column("location", justify="left")
    table.add_column("country", justify="right")

    for loc in locs:
        if filter_country:
            if loc.country == filter_country:
                table.add_row(loc.name, loc.country)
        else:
            table.add_row(loc.name, loc.country)

    console.print(table)


@volumes.command(name="create")
@click.option("--size", "-S", default="10", help="Volume size")
@click.option("--name", "-n", required=True, help="Volume name")
@click.option("--kind", "-k", default="pd-standard", help="Volume type")
def volume_create(size, name, kind):
    """Create a volume"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    if not jup.check_volume(name):
        console.print("=> Creating new volume")
        jup.create_volume(name, size=size, storage_type=kind)
        jup.push()
        console.print("=> Volume created")
    else:
        console.print("[x] Volume already exists")


@volumes.command(name="list")
@click.option("--get-all", "-g", is_flag=True, default=False, help="Get all volumes")
def volume_list(get_all):
    """List volumes"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    if get_all:
        vols = jup.prov.list_volumes()
    else:
        vols = jup._state.volumes.values()
    table = Table(title=f"Volumes")

    table.add_column("name", justify="left")
    table.add_column("size", justify="right")
    table.add_column("location", justify="right")
    table.add_column("kind", justify="right")
    table.add_column("status", justify="right")
    for vol in vols:
        table.add_row(vol.name, vol.size, vol.location, vol.storage_type, vol.status)

    console.print(table)


@volumes.command(name="import")
@click.option("--name", "-n", required=True, help="Name of the volume")
def volume_import(name):
    """Import a volume from the provider into this project"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    jup.import_volume(name)
    jup.push()
    console.print(f"Volume {name} imported.")


@volumes.command(name="unlink")
@click.option("--name", "-n", required=True, help="Name of the volume")
def volume_unlink(name):
    """Unlink a volume from this project"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    if jup._state.volumes.get(name):
        del jup._state.volumes[name]
        jup.push()
        console.print(f"Volume {name} unlinked.")


@volumes.command(name="resize")
@click.option("--name", "-n", required=True, help="Name of the volume")
@click.option("--size", "-S", required=True, help="New size of the volume")
def volume_resize(name, size):
    """Resize a volume"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    res = jup.resize_volume(name, size)
    if res:
        jup.push()
        console.print(f"[green]Volume {name} resized.[/]")
    else:
        console.print(f"[red]Volume {name} resize fail.[/]")


@volumes.command(name="destroy")
@click.option("--name", "-n", required=True, help="Name of the volume")
def volume_destroy(name):
    """Destroy a volume"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    _confirm = Confirm.ask(
        f"Do you want to destroy volume named '{name}'?", default=False
    )
    if _confirm:
        res = jup.destroy_volume(name)
        if res:
            jup.push()
            console.print(f"[green]Volume {name} destroyed.[/]")
        else:
            console.print(f"[red]Volume {name} destroy failed.[/]")


@snapshots.command(name="list")
def snapshot_list():
    """List snapshots"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    snaps = jup.compute.list_snapshots()
    table = Table(title=f"Snapshots")

    table.add_column("name", justify="left")
    table.add_column("size", justify="right")
    table.add_column("source", justify="right")
    table.add_column("created", justify="right")
    for snap in snaps:
        table.add_row(snap.name, snap.size, snap.source_disk, snap.created_at)

    console.print(table)


@snapshots.command(name="create")
@click.option("--name", "-n", required=True, help="Snapshot name")
@click.option("--source", "-S", required=True, help="Volume name")
def snapshot_create(name, source):
    """Create a snapshot from a volume"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    console.print(f"=> Creating a snapshot from {source}")
    jup.compute.create_snapshot(source, snapshot_name=name)
    console.print("=> Snapshot created")


@snapshots.command(name="destroy")
@click.option("--name", "-n", required=True, help="Name of the snapshot to destroy")
def snapshot_destroy(name):
    """Destroy a snapshot"""
    state_path = jupyter.get_project_state_path()
    jup = jupyter.load(state_path)
    _confirm = Confirm.ask(
        f"Do you want to destroy snapshot named '{name}'?", default=False
    )
    if _confirm:
        res = jup.compute.destroy_snapshot(name)
        console.print(f"[green]Snapshot {name} destroyed.[/]")
