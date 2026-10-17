
"""Tactical mission selection interface for YoruTerminal."""

from rich.panel import Panel
from rich.text import Text

from database.db import get_connection
from ui.terminal import console
from ui.phishing_menu import play_phishing_mission
from ui.log_investigator_menu import play_log_investigator
from ui.security_puzzle_room_menu import play_security_puzzle_room
from ui.incident_response_menu import play_incident_response


DIFFICULTY_STYLES = {
    "Beginner": "bright_green",
    "Intermediate": "bright_yellow",
    "Advanced": "bright_red",
}


def show_missions_menu(user_id: int) -> None:
    """Display registered missions stored in the database."""
    with get_connection() as connection:
        missions = connection.execute(
            """
            SELECT id, title, category, description, difficulty
            FROM missions
            ORDER BY
                CASE difficulty
                    WHEN 'Beginner' THEN 1
                    WHEN 'Intermediate' THEN 2
                    WHEN 'Advanced' THEN 3
                    ELSE 4
                END,
                title
            """
        ).fetchall()

    console.print()
    console.print(
        Panel(
            Text("MISSION SELECT", style="bold bright_cyan", justify="center"),
            subtitle="[dim]Choose your next operation[/]",
            border_style="bright_magenta",
            padding=(0, 2),
        )
    )

    if not missions:
        console.print("[yellow]No missions are currently available.[/]")
        return

    for number, mission in enumerate(missions, start=1):
        difficulty = mission["difficulty"]
        difficulty_style = DIFFICULTY_STYLES.get(
            difficulty, "white"
        )

        mission_details = Text()
        mission_details.append(
            f"{mission['id'].upper()}",
            style="bold bright_cyan",
        )
        mission_details.append("  //  ")
        mission_details.append(
            mission["category"],
            style="bright_magenta",
        )
        mission_details.append("\n")
        mission_details.append("DIFFICULTY  ", style="dim")
        mission_details.append(
            difficulty.upper(),
            style=f"bold {difficulty_style}",
        )
        mission_details.append("\n\n")
        mission_details.append(
            mission["description"],
            style="white",
        )

        console.print(
            Panel(
                mission_details,
                title=f"[bold bright_green][{number:02}][/]",
                border_style="bright_blue",
                padding=(0, 2),
            )
        )

    console.print(
        "\n[bold bright_green][0][/] [dim]Return to Player Menu[/]"
    )

    while True:
        choice = console.input(
            "\n[bold bright_cyan]yoru@missions[/] "
            "[bright_magenta]›[/] "
        ).strip()

        if choice == "0":
            console.print("[dim]Returning to player menu...[/]")
            return

        if choice.isdigit() and 1 <= int(choice) <= len(missions):
            selected_mission = missions[int(choice) - 1]
            mission_id = selected_mission["id"]

            if mission_id == "phishing-001":
                play_phishing_mission(user_id)

            elif mission_id == "logs-001":
                play_log_investigator(user_id)

            elif mission_id == "puzzle-001":
                play_security_puzzle_room(user_id)

            elif mission_id == "incident-001":
                play_incident_response(user_id)

            else:
                console.print(
                    "[yellow]This mission is not playable yet.[/]"
                )
        else:
            console.print(
                "[bold red]Invalid choice.[/] "
                "[dim]Select a listed mission or 0.[/]"
            )
