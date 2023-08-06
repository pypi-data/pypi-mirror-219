from mobicontrol.scripts.fetch_token import fetch_token
from mobicontrol.scripts.upload_apk import get_apk_upload_data, get_package_upload_data
from mobicontrol.utils import get_file_contents, get_filename_from_path
import click
import json
import os
import requests


class Storage(object):
    def __init__(self):
        self.access_token = None
        self.url = None

    @classmethod
    def unserialize(cls, obj):
        inst = cls()
        inst.access_token = obj["access_token"]
        inst.url = obj["url"]
        return inst

    def _serialize(self):
        return {"access_token": self.access_token, "url": self.url}

    def store(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(f"{path}/store.json", "w") as file:
            file.write(json.dumps(self._serialize()))


@click.group(invoke_without_command=True)
@click.option("--url", envvar="MC_URL")
@click.pass_context
def mobicontrol(ctx, url):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        with open(f"{path}/store.json", "r") as file:
            obj = json.loads(file.read())
            ctx.obj = Storage.unserialize(obj)
    except Exception:
        ctx.obj = Storage()

    if ctx.invoked_subcommand is None:
        if url:
            ctx.obj.url = url

        ctx.obj.store()

        click.echo(f"Welcome to Mobicontrol CLI")
        click.echo(f"Your deployment server is located at {url}")

    if ctx.obj.url is None:
        click.echo("Sorry, you need to configure the URL before using the CLI")


@mobicontrol.command()
@click.option("--client_id", envvar="CLIENT_ID")
@click.option("--client_secret", envvar="CLIENT_SECRET")
@click.option("--username", envvar="MC_USERNAME")
@click.option("--password", envvar="MC_PASSWORD")
@click.pass_context
def login(ctx, client_id, client_secret, username, password):
    click.echo(f"Logging in as {username}")
    try:
        url = ctx.obj.url
        token = fetch_token(url, client_id, client_secret, username, password)
        ctx.obj.access_token = token
        ctx.obj.store()
    except Exception as e:
        click.echo("Could not log in")
        click.echo(e)
        return

    click.echo("Successfully logged in!")


@mobicontrol.command()
@click.option("--file")
@click.pass_context
def package(ctx, file):
    click.echo("Uploading package")
    token = ctx.obj.access_token
    url = ctx.obj.url
    try:
        filename = get_filename_from_path(file)
        content = get_file_contents(file)
        message = get_package_upload_data(token, content, filename)

        headers = dict(message.items())
        body = message.as_string().split("\n\n", 1)[1]
        body = body.replace("\n", "\r\n")

        with open(f"./package-body.txt", "w") as file:
            file.write(body)

        response = requests.post(
            f"{url}/packages",
            headers={
                "Authorization": headers["Authorization"],
                "Content-Type": headers["Content-Type"],
            },
            data=body.encode("utf-8"),
        )

        print(response.request.headers)

        if "ErrorCode" in response:
            click.echo(f"Failed with error {response['ErrorCode']}")
            click.echo(response["Message"])
        elif response.status_code != 200:
            raise click.ClickException(
                f"Upload failed with status code {response.status_code}. {response.text}."
            )
        else:
            click.echo("Upload successful")

    except FileNotFoundError:
        click.echo(f"File {file} does not exist")


@mobicontrol.command()
@click.option("--file")
@click.pass_context
def enterprise_app(ctx, file):
    # click.echo("Uploading enterprise app")
    token = ctx.obj.access_token
    url = ctx.obj.url

    try:
        filename = get_filename_from_path(file)
        content = get_file_contents(file)
        message = get_package_upload_data(token, content, filename)

        body = message.as_string().split("\n\n", 1)[1]
        body = body.replace("\n", "\r\n")

        with open(f"./body.txt", "w") as file:
            file.write(body)

        headers = dict(message.items())

        response = requests.post(
            f"{url}/appManagement/android/apps/enterprise/internal",
            headers={
                "Authorization": headers["Authorization"],
                "Content-Type": headers["Content-Type"],
            },
            data=body.encode("utf-8"),
        )

        if response.status_code != 200:
            raise click.ClickException(
                f"Upload failed with status code {response.status_code}. {response.text}."
            )

        response_body = response.json()

        app_reference = response_body["ReferenceId"]

        if "ErrorCode" in response_body:
            click.echo(f"Failed with error {response['ErrorCode']}")
            click.echo(response["Message"])
            raise click.ClickException(f"Upload failed with message: {response['Message']}")

    except FileNotFoundError:
        raise click.ClickException(f"File {file} does not exist")

    click.echo(app_reference)


@mobicontrol.command()
@click.option("--name", type=str, required=True)
@click.option("--kind", type=str, required=True)
@click.option("--description", type=str)
@click.pass_context
def create_policy(ctx, name: str, kind: str, description: str = ""):
    token = ctx.obj.access_token
    url = ctx.obj.url

    response = requests.get(
        f"{url}/appManagement/policies",
        headers={"Authorization": f"Bearer {token}"},
        params={"nameContains": name},
    )

    if response.status_code != 200:
        raise click.ClickException(
            f"Could not fetch policies. Error code: {response.status_code}. {response.text}"
        )

    data = response.json()

    if len(data) == 1:
        click.echo(data[0]["ReferenceId"])
        return
    elif len(data) > 1:
        raise click.ClickException(f"Found more than one policy with name {name}")

    response = requests.post(
        f"{url}/appManagement/android/policies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "Name": name,
            "Description": description,
            "RuleKind": kind,
        },
    )

    if response.status_code != 200:
        raise click.ClickException(
            f"Could not create policy. Error code: {response.status_code}. {response.text}"
        )

    data = response.json()

    click.echo(data["ReferenceId"])


@mobicontrol.command()
@click.option("--policy-reference")
@click.option("--app-reference")
@click.option("--app-config")
@click.pass_context
def enterprise_app_assign(ctx, policy_reference: str, app_reference: str, app_config: str = ""):
    token = ctx.obj.access_token
    url = ctx.obj.url

    response = requests.put(
        f"{url}/appManagement/android/policies/{policy_reference}/apps/enterprise",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        json=[
            {
                "ReferenceId": app_reference,
                "IsMandatory": True,
                "AppPriority": 1,
                "AppConfiguration": app_config,
            }
        ],
    )

    if response.status_code != 204:
        data = response.json()

        if "ErrorCode" in data:
            click.echo(f"Failed with error {data['ErrorCode']}")
            click.echo(data["Message"])
            raise click.ClickException(f"Upload failed with message: {data['Message']}")

        raise click.ClickException(
            f"Upload failed with status code {response.status_code}. {response.text}."
        )

    click.echo(f"Successfully assigned app {app_reference} to policy {policy_reference}.")
