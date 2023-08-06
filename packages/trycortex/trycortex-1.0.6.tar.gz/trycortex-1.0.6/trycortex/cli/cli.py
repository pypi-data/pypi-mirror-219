import click
import trycortex.cli.callable.commands as callable_commands

@click.group()
@click.pass_context
def cortex(ctx):
    pass

# subcommands
cortex.add_command(callable_commands.callable)

# aliases
cortex.add_command(callable_commands.init_callable, "init")

if __name__ == '__main__':
    cortex()