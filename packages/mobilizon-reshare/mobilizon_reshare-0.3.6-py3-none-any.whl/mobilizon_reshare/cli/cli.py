import functools

import click
import uvicorn
from click import pass_context

from mobilizon_reshare.cli import safe_execution
from mobilizon_reshare.cli.commands.format.format import format_event
from mobilizon_reshare.cli.commands.list.list_event import list_events
from mobilizon_reshare.cli.commands.list.list_publication import list_publications
from mobilizon_reshare.cli.commands.publish.main import publish_command as publish_main
from mobilizon_reshare.cli.commands.pull.main import pull_command as pull_main
from mobilizon_reshare.cli.commands.recap.main import recap_command as recap_main
from mobilizon_reshare.cli.commands.retry.main import (
    retry_event_command,
    retry_publication_command,
)
from mobilizon_reshare.cli.commands.start.main import start_command as start_main
from mobilizon_reshare.config.command import CommandConfig
from mobilizon_reshare.config.config import current_version, get_settings, init_logging
from mobilizon_reshare.config.publishers import publisher_names
from mobilizon_reshare.dataclasses.event import _EventPublicationStatus
from mobilizon_reshare.models.publication import PublicationStatus
from mobilizon_reshare.publishers import get_active_publishers


def test_settings(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    settings = get_settings()
    init_logging(settings)
    click.echo("OK!")
    ctx.exit()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(current_version())
    ctx.exit()


def print_platforms(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    for platform in get_active_publishers():
        click.echo(platform)
    ctx.exit()


status_name_to_enum = {
    "event": {
        "waiting": _EventPublicationStatus.WAITING,
        "completed": _EventPublicationStatus.COMPLETED,
        "failed": _EventPublicationStatus.FAILED,
        "partial": _EventPublicationStatus.PARTIAL,
        "all": None,
    },
    "publication": {
        "completed": PublicationStatus.COMPLETED,
        "failed": PublicationStatus.FAILED,
        "all": None,
    },
}
from_date_option = click.option(
    "-b",
    "--begin",
    type=click.DateTime(),
    expose_value=True,
    help="Include only events that begin after this datetime.",
)
to_date_option = click.option(
    "-e",
    "--end",
    type=click.DateTime(),
    expose_value=True,
    help="Include only events that end before this datetime.",
)
event_status_argument = click.argument(
    "status",
    type=click.Choice(list(status_name_to_enum["event"].keys())),
    default="all",
    expose_value=True,
)
publication_status_argument = click.argument(
    "status",
    type=click.Choice(list(status_name_to_enum["publication"].keys())),
    default="all",
    expose_value=True,
)
force_publish_option = click.option(
    "-F",
    "--force",
    type=click.UUID,
    expose_value=True,
    help="Publish the given event, bypassing all selection logic. This command WILL publish"
    "regardless of the configured strategy, so use it with care.",
)
platform_name_option = click.option(
    "-p",
    "--platform",
    type=str,
    expose_value=True,
    help="Restrict the platforms where the event will be published. This makes sense only in"
    " case of force-publishing.",
)
list_supported_option = click.option(
    "--list-platforms",
    is_flag=True,
    callback=print_platforms,
    expose_value=False,
    is_eager=True,
    help="Show all active platforms.",
)
test_configuration = click.option(
    "-t",
    "--test-configuration",
    is_flag=True,
    callback=test_settings,
    expose_value=False,
    is_eager=True,
    help="Validate the current configuration.",
)


@click.group()
@test_configuration
@list_supported_option
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show the current version.",
)
@pass_context
def mobilizon_reshare(obj):
    pass


@mobilizon_reshare.command(
    help="Synchronize and publish events. It is equivalent to running consecutively pull and then publish."
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Prevents data to be published to platforms. WARNING: it will download and write new events to the database",
    default=False,
)
def start(dry_run):

    safe_execution(start_main, CommandConfig(dry_run=dry_run))


@mobilizon_reshare.command(help="Publish a recap of already published events.")
@click.option(
    "--dry-run",
    "dry_run",
    is_flag=True,
    help="Prevents data to be published to platforms. WARNING: it will download and write new events to the database",
    default=False,
)
def recap(dry_run):
    safe_execution(recap_main, CommandConfig(dry_run=dry_run))


@mobilizon_reshare.command(
    help="Fetch the latest events from Mobilizon, store them if they are unknown, "
    "update them if they are known and changed."
)
def pull():
    safe_execution(pull_main,)


@mobilizon_reshare.command(
    help="Select an event with the current configured strategy"
    " and publish it to all active platforms."
)
@force_publish_option
@platform_name_option
@click.option(
    "--dry-run",
    "dry_run",
    is_flag=True,
    help="Prevents data to be published to platforms.",
    default=False,
)
def publish(event, platform, dry_run):
    safe_execution(functools.partial(
            publish_main, event, platform
        ), CommandConfig(dry_run=dry_run))


@mobilizon_reshare.group(help="Operations that pertain to events")
def event():
    pass


@mobilizon_reshare.group(help="Operations that pertain to publications")
def publication():
    pass


@event.command(help="Query for events in the database.", name="list")
@event_status_argument
@from_date_option
@to_date_option
def event_list(status, begin, end):

    safe_execution(
        functools.partial(
            list_events, status_name_to_enum["event"][status], frm=begin, to=end,
        ),
    )


@publication.command(help="Query for publications in the database.", name="list")
@publication_status_argument
@from_date_option
@to_date_option
def publication_list(status, begin, end):
    safe_execution(
        functools.partial(
            list_publications,
            status_name_to_enum["publication"][status],
            frm=begin,
            to=end,
        ),
    )


@event.command(
    help="Format and print event with EVENT-ID using the publisher's format named "
    "PUBLISHER."
)
@click.argument("event-id", type=click.UUID)
@click.argument("publisher", type=click.Choice(publisher_names))
def format(
    event_id, publisher,
):
    safe_execution(functools.partial(format_event, event_id, publisher),)


@event.command(name="retry", help="Retries all the failed publications")
@click.argument("event-id", type=click.UUID)
def event_retry(event_id):
    safe_execution(functools.partial(retry_event_command, event_id),)


@publication.command(name="retry", help="Retries a specific publication")
@click.argument("publication-id", type=click.UUID)
def publication_retry(publication_id):
    safe_execution(functools.partial(retry_publication_command, publication_id),)


@mobilizon_reshare.command("web")
def web():
    uvicorn.run(
        "mobilizon_reshare.web.backend.main:app", host="0.0.0.0", port=8000, reload=True
    )


if __name__ == "__main__":
    mobilizon_reshare(obj={})
