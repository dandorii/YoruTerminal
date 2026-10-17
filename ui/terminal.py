
"""Shared terminal presentation for YoruTerminal."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from database.db import get_connection


console = Console()

# Tactical Shinobi color palette
CYAN = "bright_cyan"
VIOLET = "bright_magenta"
GREEN = "bright_green"
RED = "bright_red"
MUTED = "dim"


def get_system_status() -> dict[str, str]:
    """Check database connectivity and count registered missions."""
    try:
        with get_connection() as connection:
            connection.execute("SELECT 1")
            result = connection.execute(
                "SELECT COUNT(*) FROM missions"
            ).fetchone()

            mission_count = result[0]

        return {
            "database": "ONLINE",
            "missions": str(mission_count),
        }

    except Exception:
        return {
            "database": "UNAVAILABLE",
            "missions": "UNKNOWN",
        }



def show_banner() -> None:
    """Display the YoruTerminal Hidden Clan startup screen."""
    status_info = get_system_status()

    logo = Text()
    logo.append(
        r"""
                 /\
                /  \
               / /\ \
              / /  \ \
             /_/____\_\

    Y   Y   OOO   RRRR   U   U
    Y   Y  O   O  R   R  U   U
     Y Y   O   O  RRRR   U   U
      Y    O   O  R  R   U   U
      Y     OOO   R   R   UUU
""".strip("\n"),
        style=f"bold {CYAN}",
    )
    logo.append(
        "\n\n    YORU CLAN // SHADOW DIVISION",
        style=f"bold {VIOLET}",
    )
    logo.append(
        "\n    CLASSIFIED CYBER OPERATIONS",
        style=f"bold {CYAN}",
    )
    logo.append(
        "\n    Infiltrate. Analyze. Adapt.",
        style=MUTED,
    )

    console.print()
    console.print(
        Panel(
            logo,
            title=f"[bold {CYAN}]YORU // HIDDEN CLAN[/]",
            subtitle=f"[italic {VIOLET}]AUTHORIZED OPERATORS ONLY[/]",
            border_style=VIOLET,
            padding=(1, 2),
        )
    )

    status = Table.grid(padding=(0, 2))
    status.add_column(style=MUTED, justify="right")
    status.add_column()

    status.add_row(
        "SYSTEM",
        f"[{GREEN}]* INTERFACE READY[/]",
    )
    status.add_row(
        "ENVIRONMENT",
        f"[{CYAN}]LOCAL TRAINING SIMULATOR[/]",
    )

    database_online = status_info["database"] == "ONLINE"
    database_style = GREEN if database_online else RED

    status.add_row(
        "DATABASE",
        f"[{database_style}]* {status_info['database']}[/]",
    )

    mission_count = status_info["missions"]

    if mission_count.isdigit():
        count = int(mission_count)
        mission_style = GREEN if count > 0 else RED
        mission_text = f"[{mission_style}]{count} REGISTERED[/]"
    else:
        mission_text = f"[{RED}]STATUS UNKNOWN[/]"

    status.add_row("MISSIONS", mission_text)

    console.print(
        Panel(
            status,
            title=f"[bold {VIOLET}]SYSTEM STATUS[/]",
            border_style=VIOLET,
            padding=(0, 2),
        )
    )
    console.print()



def show_main_menu() -> None:
    """Display the main menu."""
    console.print(f"\n[bold {CYAN}]MAIN MENU[/]")
    console.print(f"[{GREEN}]1.[/] Register")
    console.print(f"[{GREEN}]2.[/] Login")
    console.print(f"[{RED}]3.[/] Exit")


def get_menu_choice() -> str:
    """Read a menu selection from the user."""
    return console.input(
        f"\n[bold {CYAN}]yoru@terminal[/] "
        f"[{VIOLET}]>[/] "
    ).strip()
