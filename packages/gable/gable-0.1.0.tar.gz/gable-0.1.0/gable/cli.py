import os
from typing import Optional
import click
from gable.client import GableClient
from gable.helpers.repo_interactions import GitInfo, get_git_info

from .commands.auth import auth
from .commands.contract import contract
from .commands.data_asset import data_asset
from .commands.ping import ping


class Context:
    def __init__(self):
        self.client: Optional[GableClient] = None
        self.git_info: Optional[GitInfo] = None


@click.group()
@click.option(
    "--endpoint",
    default=os.environ.get("GABLE_API_ENDPOINT"),
    help="Customer API endpoint for Gable, in the format https://api.company.gable.ai/",
)
@click.option(
    "--api-key",
    default=os.environ.get("GABLE_API_KEY"),
    help="API Key for Gable",
)
@click.pass_context
def cli(ctx, endpoint, api_key):
    ctx.obj = Context()
    ctx.obj.client = GableClient(endpoint, api_key)
    ctx.obj.git_info = get_git_info()


cli.add_command(auth)
cli.add_command(contract)
cli.add_command(data_asset)
cli.add_command(ping)


if __name__ == "__main__":
    cli()  # type: ignore
