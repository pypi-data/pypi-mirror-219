from typing import List
import click
from click.core import Context as ClickContext


@click.group()
def auth():
    """View configured Gable authentication information"""
    pass


@auth.command()
@click.pass_context
def key(ctx: ClickContext):
    """Print the API Key gable is currently configured to use"""
    click.echo("API Key in use: " + ctx.obj.client.api_key)
    click.echo("To see your account's API Keys, visit your /settings page")
