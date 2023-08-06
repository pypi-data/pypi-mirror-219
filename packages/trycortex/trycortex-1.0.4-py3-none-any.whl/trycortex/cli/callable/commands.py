import click

@click.group(help="Callable-related commands")
def callable():
    pass

@callable.command("init", help="Creates an callable.yaml file.")
def init_callable():
    click.echo("init callable")