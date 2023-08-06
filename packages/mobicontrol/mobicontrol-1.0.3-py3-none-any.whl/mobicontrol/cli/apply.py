from mobicontrol.cli import mobicontrol
import click
import yaml
import json
from mobicontrol.client.policies import (
    get_policies,
    create_policy,
    set_apps,
    set_assignments,
    delete_policy,
)


def apply_apps(ctx, policy_id: str, apps: list[dict]):
    payload = [
        {
            "ReferenceId": app["appId"],
            "IsMandatory": app.get("mandatory", True),
            "AppPriority": app.get("priority", 1),
            "AppConfiguration": json.dumps(app.get("config", {})),
        }
        for app in apps
    ]

    set_apps(ctx.obj, policy_id, payload)
    click.echo(f"Assigned {len(payload)} apps to policy.")


def apply_policy(ctx, manifest: dict):
    meta = manifest["metadata"]
    try:
        policies = get_policies(ctx.obj, meta["name"])

        for policy in policies:
            if policy["Name"] == meta["name"]:
                policy = policy
                click.echo(f"Found existing policy with name {meta['name']}.")
                break
        else:
            policy = create_policy(ctx.obj, meta["name"], meta["kind"], meta["description"])
            click.echo(f"Created new policy with name {meta['name']}.")
    except Exception as e:
        raise click.ClickException(str(e))

    apps = manifest.get("apps", [])

    try:
        apply_apps(ctx, policy["ReferenceId"], apps)

        assignment_groups = manifest.get("assignmentGroups", [])
        set_assignments(ctx.obj, policy["ReferenceId"], assignment_groups)
        click.echo(f"Assigned policy to {len(assignment_groups)} device groups.")
    except Exception as e:
        raise click.ClickException(str(e))


def delete_policy_manifest(ctx, manifest: dict):
    meta = manifest["metadata"]
    try:
        policies = get_policies(ctx.obj, meta["name"])

        for policy in policies:
            if policy["Name"] == meta["name"]:
                policy = policy
                break
        else:
            raise click.ClickException(f"Could not find policy with name {meta['name']}")
    except Exception as e:
        raise click.ClickException(str(e))

    try:
        delete_policy(ctx.obj, policy["ReferenceId"])
    except Exception as e:
        raise click.ClickException(str(e))


@mobicontrol.command()
@click.option("--file", type=click.Path(exists=True), required=True)
@click.pass_context
def apply(ctx, file: str):
    with open(file) as f:
        data = yaml.safe_load(f)

    if data["resourceType"] == "policy":
        apply_policy(ctx, data)


@mobicontrol.command()
@click.option("--file", type=click.Path(exists=True), required=True)
@click.pass_context
def delete(ctx, file: str):
    with open(file) as f:
        data = yaml.safe_load(f)

    if data["resourceType"] == "policy":
        delete_policy_manifest(ctx, data)
