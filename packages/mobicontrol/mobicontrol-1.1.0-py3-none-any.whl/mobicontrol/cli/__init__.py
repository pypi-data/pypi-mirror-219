from mobicontrol.client.auth import authenticate
from mobicontrol.client import MobicontrolClient
import click


@click.group(invoke_without_command=True, name="mc")
@click.option("--url", envvar="MC_URL")
@click.pass_context
def mobicontrol(ctx, url: str):
    ctx.obj = MobicontrolClient.load(url)

    if ctx.invoked_subcommand is None:
        ctx.obj.save()
        click.echo("Welcome to Mobicontrol CLI")
        click.echo(f"Your deployment server is located at {ctx.obj.base_url}")

    if ctx.obj.base_url is None:
        click.echo("Sorry, you need to configure the URL before using the CLI")


@mobicontrol.command()
@click.option("--client_id", envvar="MC_CLIENT_ID")
@click.option("--client_secret", envvar="MC_CLIENT_SECRET")
@click.option("--username", envvar="MC_USERNAME")
@click.option("--password", envvar="MC_PASSWORD")
@click.pass_context
def login(ctx, client_id, client_secret, username, password):
    click.echo(f"Logging in as {username}")
    try:
        authenticate(ctx.obj, client_id, client_secret, username, password)
        ctx.obj.save()
    except Exception as e:
        click.echo(e)
        return

    click.echo("Successfully logged in!")


from . import apps, policies, apply
