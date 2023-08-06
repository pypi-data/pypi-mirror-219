import os
import sys
from datetime import datetime
from itertools import chain
from os import path

import typer

from hyprshade.constants import (
    EMPTY_STR,
    SHADER_DIRS,
)
from hyprshade.helpers import resolve_shader_path
from hyprshade.utils import systemd_user_config_home

app = typer.Typer(no_args_is_help=True)


@app.command()
def ls() -> int:
    """List available screen shaders"""

    for shader in chain(
        *map(
            os.listdir,
            SHADER_DIRS,
        )
    ):
        shader, _ = path.splitext(shader)
        print(shader)

    return 0


@app.command()
def on(shader_name_or_path: str) -> int:
    """Turn on screen shader"""

    shader_path = resolve_shader_path(shader_name_or_path)
    code = os.system(f"hyprctl keyword decoration:screen_shader '{shader_path}'")
    return code


@app.command()
def off() -> int:
    """Turn off screen shader"""

    code = os.system(f"hyprctl keyword decoration:screen_shader '{EMPTY_STR}'")
    return code


@app.command()
def toggle(shader_name_or_path: str) -> int:
    """Toggle screen shader"""

    import json
    from json import JSONDecodeError

    current_shader: str | None = None
    try:
        o = json.load(os.popen("hyprctl -j getoption decoration:screen_shader"))
        current_shader = str(o["str"]).strip()
    except JSONDecodeError:
        print("Failed to get current screen shader", file=sys.stderr)
        return 1

    if path.isfile(current_shader) and path.samefile(
        resolve_shader_path(shader_name_or_path), current_shader
    ):
        off()
        return 0

    return on(shader_name_or_path)


@app.command()
def auto() -> int:
    """Turn on/off screen shader based on schedule"""

    from hyprshade.config import Config

    t = datetime.now().time()
    schedule = Config().to_schedule()
    shade = schedule.find_shade(t)

    if shade is not None:
        return on(shade)
    return off()


@app.command()
def install() -> int:
    """Instal systemd user units"""

    from hyprshade.config import Config

    schedule = Config().to_schedule()

    with open(path.join(systemd_user_config_home(), "hyprshade.service"), "w") as f:
        f.write(
            """[Unit]
Description=Apply screen filter

[Service]
Type=oneshot
ExecStart="/usr/bin/hyprshade" auto
"""
        )

    with open(path.join(systemd_user_config_home(), "hyprshade.timer"), "w") as f:
        on_calendar = "\n".join(
            sorted([f"OnCalendar=*-*-* {x}" for x in schedule.on_calendar_entries()])
        )
        f.write(
            f"""[Unit]
Description=Apply screen filter on schedule

[Timer]
{on_calendar}
Persistent=true

[Install]
WantedBy=timers.target"""
        )

    return 0


def main():
    app()
