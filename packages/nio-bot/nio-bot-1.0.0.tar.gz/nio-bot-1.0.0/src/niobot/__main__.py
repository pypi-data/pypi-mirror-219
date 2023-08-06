import asyncio
import datetime
import os
import pathlib
import re
import sys
import logging

import niobot
import importlib.metadata

try:
    import click
    import httpx
except ImportError:
    print("Missing CLI dependencies. Did you install CLI extras?", file=sys.stderr)
    sys.exit(1)
import subprocess

logger = logging.getLogger("cli")

DEFAULT_BOT_TEMPLATE = """#!/usr/bin/env python3
\"\"\"
Generated by NioBot's setup script at {timestamp} on build {version_info}. Feel free to edit this file!
\"\"\"
import niobot
import time


bot = niobot.NioBot(
    "{homeserver}",
    "{user_id}",
    "{device_id}",
    store_path="{store_path}",
    command_prefix="{prefix}",
    owner_id="{owner_id}",
)


@bot.command()
async def ping(ctx: niobot.Context):
    \"\"\"Shows the latency between the bot and the homeserver, in milliseconds.\"\"\"
    server_timestamp_seconds = ctx.message.server_timestamp / 1000
    latency = time.time() - server_timestamp_seconds
    await ctx.reply(f"Pong! {{latency * 1000:.2f}}ms")


@bot.command()
async def info(ctx: niobot.Context):
    \"\"\"Shows information about the currently running instance.\"\"\"
    await ctx.reply(f"Bot owner: {{ctx.client.owner_id}}\\n"
                    f"Bot user ID: {{ctx.client.user_id}}\\n"
                    f"Bot homeserver: {{ctx.client.homeserver}}\\n"
                    f"Bot command prefix: {{ctx.client.command_prefix}}\\n"
                    f"Bot command count: {{len(ctx.client.commands)}}\\n"
                    f"Bot module count: {{len(ctx.client.modules)}}\\n"
                    f"Bot uptime: {{time.time() - ctx.client.start_time:,.0f}} seconds")

bot.run(password="{password}")
"""


@click.group()
@click.option(
    "--log-level", "-L",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="WARNING"
)
@click.pass_context
def cli_root(ctx, log_level: str):
    """CLI utilities for nio-bot."""
    logging.basicConfig(
        level=getattr(logging, log_level),
    )

    try:
        from .__version__ import __version__, __version_tuple__
    except ImportError:
        logger.warning("Failed to import version metadata.")
        __version__ = "unknown"
        __version_tuple__ = (0, 0, "unknown", "gunknown.d19991231")
    else:
        logger.debug("Version: %s", __version__)

    ctx.obj = {
        "timestamp": datetime.datetime.now(),
        "version_info": __version__,
        "version_tuple": __version_tuple__
    }


@cli_root.command()
@click.option("--no-colour", "--no-color", "-C", is_flag=True, default=False)
@click.pass_context
def version(ctx, no_colour: bool):
    """Shows version information."""
    logger.info("Gathering version info...")
    import platform
    from nio.crypto import ENCRYPTION_ENABLED

    logger.debug("Attempting to resolve matrix-nio via importlib...")
    nio_version = None
    try:
        nio_version = importlib.metadata.version("matrix-nio")
    except importlib.metadata.PackageNotFoundError:
        logger.critical("Failed to resolve nio version information via importlib.")

    if not nio_version:
        logger.debug("Attempting to resolve matrix-nio version information via pip...")
        command = [
            "pip",
            "show",
            "matrix-nio"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            logger.critical("Failed to resolve nio version information via pip.")
            nio_version = "0.0.0"
        else:
            logger.debug("Successfully resolved nio version information via pip.")
            nio_version = result.stdout.splitlines()[1].split(": ")[1]

    t = ctx.obj["version_tuple"]
    if len(t) > 3:
        t3 = t[3] or 'gN/A.d%s' % (datetime.datetime.now().strftime("%Y%m%d"))
        try:
            t3_commit, t3_date_raw = t3.split(".", 1)
        except ValueError:
            t3_commit = t3
            logger.warning("Failed to parse commit date from %r, using current date instead.", t3)
            t3_date = datetime.datetime.now()
            t3_date_raw = t3_date.strftime("%Y%m%d")
        t3_date = datetime.datetime.strptime(t3_date_raw[1:], "%Y%m%d")
    else:
        t3_commit = "<release>"
        mtime = pathlib.Path(__file__).stat().st_mtime
        t3_date = datetime.datetime.fromtimestamp(mtime)

    bot_version_deep = {
        "version": "%d.%d" % (t[0], t[1]),
        "build": t[2],
        "commit": t3_commit,
        "date": t3_date
    }

    bot_version = "%s (Version %s, build %s, commit %r, built %r)" % (
        ctx.obj["version_info"],
        bot_version_deep["version"],
        bot_version_deep["build"],
        bot_version_deep["commit"][1:],
        bot_version_deep["date"].strftime("%d/%m/%Y")
    )

    lines = [
        ["NioBot version", bot_version, lambda x: True],
        ["matrix-nio version", nio_version, lambda x: x.startswith("0.20")],
        ["Python version", platform.python_version(), lambda x: x.split(".")[0] == "3" and int(x.split(".")[1]) >= 9],
        ["Python implementation", platform.python_implementation(), lambda x: x == "CPython"],
        ["Operating System", platform.platform(), lambda val: val.startswith(("Windows", "Linux"))],
        ["Architecture", platform.machine(), lambda x: x == "x86_64"],
        ["OLM Installed", "Yes" if ENCRYPTION_ENABLED else "No", lambda x: x != "No"],
    ]

    click.echo()
    for line in lines:
        if no_colour:
            click.echo("%s: %s" % tuple(line)[:2])
        else:
            click.echo(
                click.style(line[0], fg="cyan") + ": " +
                click.style(line[1], fg="green" if line[2](line[1]) else "red")
            )
    click.echo()


@cli_root.command(name="test-homeserver")
@click.argument("homeserver")
def test_homeserver(homeserver: str):
    """Walks through resolving and testing a given homeserver."""
    import httpx
    import urllib.parse

    if homeserver.startswith("@"):
        _, homeserver = homeserver.split(":", 1)

    logger.debug("Parsing given input %r as a URL...", homeserver)
    parsed = urllib.parse.urlparse(homeserver)
    if not parsed.scheme:
        logger.info("No scheme found, assuming HTTPS.")
        parsed = urllib.parse.urlparse("https://" + homeserver)

    if not parsed.netloc:
        logger.critical("No netloc found, cannot continue.")
        logger.critical("URI parsed to: %r", parsed)
        return

    logger.debug("Attempting to resolve %r...", parsed.netloc)
    logger.info("Trying well-known of %r...", parsed.netloc)
    base_url = None
    try:
        response = httpx.get(
            "https://%s/.well-known/matrix/client" % parsed.netloc,
            timeout=30
        )
    except httpx.HTTPError as e:
        logger.critical("Failed to get well-known: %r", e)
        return
    else:
        logger.debug("Got response: %r", response)
        cors = response.headers.get("Access-Control-Allow-Origin", None)
        if not cors:
            logger.warning("No CORS header found. This homeserver will be unusable in web-based clients!")
        elif cors != "*":
            logger.warning(
                "CORS header found, but not set to wildcard. "
                "This homeserver will be unusable in most web-based clients!"
            )

        if response.status_code != 404:
            if response.status_code != 200 or len(response.content or b'') == 0:
                logger.critical("Well-known returned non-404, but no content. Failing.")
                return
            else:
                data = response.json()
                logger.debug("Well-known data: %r", data)
                if "m.homeserver" not in data:
                    logger.critical("Well-known data does not contain m.homeserver. Failing.")
                    return
                base_url = urllib.parse.urlparse(data["m.homeserver"]["base_url"])
                logger.debug("Parsed base URL: %r", base_url)
                if not base_url.scheme or not base_url.netloc:
                    logger.critical("Base URL does not contain a scheme. Invalid URL? Failing.")
                    return

    if not base_url:
        logger.info("No well-known found. Assuming %r as homeserver.", parsed.netloc)
        base_url = urllib.parse.urlparse("https://" + parsed.netloc)

    base_url = base_url.geturl()
    logger.info("Using %r as homeserver.", base_url)
    logger.info("Validating homeserver...")
    try:
        response = httpx.get(
            base_url + "/_matrix/client/versions",
            timeout=30
        )
    except httpx.HTTPError as e:
        logger.critical("Failed to get versions: %r", e)
        return
    else:
        data = response.json()
        logger.debug("Got response: %r", data)
        if "versions" not in data:
            logger.critical("Versions response does not contain versions. Failing.")
            return
        if "unstable_features" not in data:
            logger.warning("Versions response does not contain unstable_features. This may be bad.")

        logger.info("Homeserver validated.")
        click.secho("Homeserver validated.", fg="green")
        click.secho("%s -> %s" % (click.style(parsed.netloc, dim=True), click.style(base_url, fg="green")))


@cli_root.command(name="get-access-token")
@click.option("--username", "-U", default=None, help="The username part (without @)")
@click.option("--password", "-P", default=None, help="The password to use (will be prompted if not given)")
@click.option("--homeserver", "-H", default=None, help="The homeserver to use (will be prompted if not given)")
@click.option(
    "--device-id", "-D", "--session", "--session-id",
    default=None,
    help="The device ID to use (will be prompted if not given)"
)
@click.pass_context
def get_access_token(ctx, username: str, password: str, homeserver: str, device_id: str):
    """Fetches your access token from your homeserver."""
    if not username:
        username = ""

    while not re.match(r"@[\w\-.]{1,235}:[0-9A-Za-z\-_.]{3,253}", username):
        username = click.prompt("User ID (@username:homeserver.tld)")
        _, homeserver = username.split(":", 1)

    if not homeserver:
        _, homeserver = username.split(":", 1)

    if not password:
        password = click.prompt("Password (will not echo)", hide_input=True)

    if not homeserver:
        homeserver = click.prompt("Homeserver URL")

    if not device_id:
        device_id = click.prompt(
            "Device ID (a memorable display name for this login, such as 'bot-production')",
            default=os.uname().nodename
        )

    click.secho("Resolving homeserver... ", fg="cyan", nl=False)
    try:
        homeserver = asyncio.run(niobot.resolve_homeserver(homeserver))
    except ConnectionError:
        click.secho("Failed!", fg="red")
    else:
        click.secho("OK", fg="green")

    click.secho("Getting access token... ", fg="cyan", nl=False)
    status_code = None
    try:
        response = httpx.post(
            homeserver + "/_matrix/client/r0/login",
            json={
                "type": "m.login.password",
                "identifier": {
                    "type": "m.id.user",
                    "user": username
                },
                "password": password,
                "device_id": device_id,
                "initial_device_display_name": device_id
            }
        )
        status_code = response.status_code
        if status_code == 429:
            click.secho("Failed!", fg="red", nl=False)
            click.secho(" (Rate limited for {:.0f} seconds)".format(response.json()["retry_after_ms"] / 1000), bg="red")
            return
        response.raise_for_status()
    except httpx.HTTPError as e:
        click.secho("Failed!", fg="red", nl=False)
        click.secho(" (%s)" % status_code or str(e), bg="red")
    else:
        click.secho("OK", fg="green")
        click.secho("Access token: %s" % response.json()["access_token"], fg="green")


@cli_root.group()
def new():
    """Create a new file from a template."""


@new.command()
@click.argument("path", type=click.Path())
@click.option("--password", "-P", prompt=True, hide_input=True)
@click.option("--user-id", "-U", prompt=True)
@click.option("--homeserver", "-H", prompt=True)
@click.option("--device-id", "-D", prompt=True)
@click.option("--store-path", "-S", prompt=True)
@click.option("--prefix", "-P", prompt=True)
@click.option("--owner-id", "-O", prompt=True)
@click.pass_context
def bot(
        ctx,
        path: str,
        password: str,
        homeserver: str,
        user_id: str,
        device_id: str,
        store_path: str,
        prefix: str,
        owner_id: str
):
    """Creates a new bot with two basic commands from the template. Easy quickstart."""
    with open(path, "w") as f:
        f.write(DEFAULT_BOT_TEMPLATE.format(
            password=password,
            homeserver=homeserver,
            user_id=user_id,
            device_id=device_id,
            store_path=store_path,
            prefix=prefix,
            owner_id=owner_id,
            timestamp=datetime.datetime.utcnow().isoformat(),
            version_info=ctx.obj["version_info"]
        ))
    click.echo("Created bot file at %r" % path)


if __name__ == "__main__":
    cli_root()
