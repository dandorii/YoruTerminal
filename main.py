
from getpass import getpass
from rich.panel import Panel
from rich.table import Table

from missions.seed import seed_missions
from ui.missions_menu import show_missions_menu
from ui.mission_history import show_mission_history

from auth.accounts import (
    RegistrationError,
    authenticate_user,
    register_user,
)
from core.session import Session
from database.db import get_connection, init_db
from ui.terminal import (
    console,
    get_menu_choice,
    show_banner,
    show_main_menu,
)


session = Session()


def register_menu() -> None:
    """Collect registration details and create an account."""
    console.print("\n[bold cyan]CREATE ACCOUNT[/]")

    username = console.input("Username: ").strip()
    password = getpass("Password (input hidden): ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        console.print("[red]Passwords do not match.[/]")
        return

    try:
        user_id = register_user(username, password)
        console.print(
            f"[green]Account created successfully![/] "
            f"Welcome, {username}."
        )
        session.login(user_id)
        console.print("[cyan]You are now logged in.[/]")

    except RegistrationError as exc:
        console.print(f"[red]{exc}[/]")


def login_menu() -> None:
    """Authenticate an existing account."""
    console.print("\n[bold cyan]LOGIN[/]")

    username = console.input("Username: ").strip()
    password = getpass("Password (input hidden): ")

    user_id = authenticate_user(username, password)

    if user_id is None:
        console.print("[red]Invalid username or password.[/]")
        return

    session.login(user_id)
    console.print(f"[green]Welcome back, {username}!")



def show_player_dashboard() -> None:
    """Display the authenticated player's tactical profile."""
    if not session.is_authenticated:
        console.print("[bold red]Access denied.[/] Please log in first.")
        return

    with get_connection() as connection:
        player = connection.execute(
            """
            SELECT u.username, p.xp, p.rank, p.missions_completed
            FROM users AS u
            JOIN player_progress AS p ON p.user_id = u.id
            WHERE u.id = ?
            """,
            (session.user_id,),
        ).fetchone()

    if player is None:
        session.logout()
        console.print("[bold red]Account not found.[/] Please log in again.")
        return

    profile = Table.grid(padding=(0, 2))
    profile.add_column(style="dim", justify="right")
    profile.add_column()

    profile.add_row(
        "OPERATOR",
        f"[bold bright_cyan]{player['username']}[/]",
    )
    profile.add_row(
        "RANK",
        f"[bold bright_magenta]{player['rank']}[/]",
    )
    profile.add_row(
        "EXPERIENCE",
        f"[bold bright_green]{player['xp']} XP[/]",
    )
    profile.add_row(
        "MISSIONS COMPLETED",
        f"[bold bright_cyan]{player['missions_completed']}[/]",
    )

    console.print()
    console.print(
        Panel(
            profile,
            title="[bold bright_cyan]OPERATOR PROFILE[/]",
            subtitle="[dim]YORU TERMINAL // PERSONNEL RECORD[/]",
            border_style="bright_magenta",
            padding=(1, 3),
        )
    )



def main() -> None:
    """Initialize YoruTerminal and run the account menu."""
    init_db()
    seed_missions()
    show_banner()

    while True:
        if session.is_authenticated:
            console.print("\n[bold cyan]PLAYER MENU[/]")
            console.print("[green]1.[/] View dashboard")
            console.print("[green]2.[/] Missions")
            console.print("[green]3.[/] Mission history")
            console.print("[green]4.[/] Logout")
            console.print("[green]5.[/] Exit")
        else:
            show_main_menu()

        choice = get_menu_choice()

        if not session.is_authenticated:
            if choice == "1":
                register_menu()
            elif choice == "2":
                login_menu()
            elif choice == "3":
                console.print(
                    "\n[cyan]Session terminated. Stay sharp.[/]"
                )
                break
            else:
                console.print(
                    "[red]Invalid choice. Select 1, 2, or 3.[/]"
                )
        else:
            if choice == "1":
                show_player_dashboard()
            elif choice == "2":
                show_missions_menu(session.user_id)
            elif choice == "3":
                show_mission_history(session.user_id)
            elif choice == "4":
                session.logout()
                console.print("[yellow]You have logged out.[/]")
            elif choice == "5":
                console.print(
                    "\n[cyan]Session terminated. Stay sharp.[/]"
                )
                break
            else:
                console.print("[red]Invalid choice. Try again.[/]")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]YoruTerminal closed.[/]")
