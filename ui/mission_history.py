
"""Mission history interface for YoruTerminal."""

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from database.db import get_connection
from ui.terminal import console


def show_mission_history(user_id: int) -> None:
    """Display the player's 20 most recent mission attempts."""
    with get_connection() as connection:
        attempts = connection.execute(
            """
            SELECT
                r.id,
                r.mission_id,
                m.title,
                r.score,
                r.completed,
                r.xp_awarded,
                r.attempted_at
            FROM mission_results AS r
            JOIN missions AS m ON m.id = r.mission_id
            WHERE r.user_id = ?
            ORDER BY r.id DESC
            LIMIT 20
            """,
            (user_id,),
        ).fetchall()

    console.print()
    console.print(
        Panel(
            Text(
                "MISSION HISTORY",
                style="bold bright_cyan",
                justify="center",
            ),
            subtitle="[dim]YORU TERMINAL // OPERATION RECORDS[/]",
            border_style="bright_magenta",
            padding=(0, 2),
        )
    )

    if not attempts:
        console.print(
            Panel(
                "No mission attempts recorded yet.\n"
                "Complete a mission to create your first record.",
                title="[bold bright_yellow]NO RECORDS FOUND[/]",
                border_style="bright_blue",
                padding=(1, 2),
            )
        )
        return

    history = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="bright_blue",
        expand=True,
    )

    history.add_column("ID", style="dim", justify="right", width=4)
    history.add_column("MISSION", min_width=18)
    history.add_column("SCORE", justify="center", width=9)
    history.add_column("STATUS", justify="center", width=12)
    history.add_column("XP", justify="right", width=6)
    history.add_column("ATTEMPTED AT", min_width=19)

    for attempt in attempts:
        completed = bool(attempt["completed"])

        status = (
            Text("COMPLETE", style="bold bright_green")
            if completed
            else Text("INCOMPLETE", style="bold bright_yellow")
        )

        history.add_row(
            str(attempt["id"]),
            f"{attempt['title']}\n[dim]{attempt['mission_id'].upper()}[/]",
            f"{attempt['score']}/100",
            status,
            f"+{attempt['xp_awarded']}",
            attempt["attempted_at"],
        )

    console.print(history)
    console.print(
        f"\n[dim]Showing {len(attempts)} most recent attempt(s), "
        "up to 20 records.[/]"
    )
