
"""Interactive terminal interface for Phishing Detective."""

from core.session import Session
from core.progression import record_mission_attempt
from rich.panel import Panel
from rich.text import Text

from missions.phishing_detective import get_questions
from missions.mission_engine import (
    calculate_mission_score,
    validate_answer,
)

from ui.terminal import console


def play_phishing_mission(user_id: int) -> dict:
    """Run the Phishing Detective mission and return its results."""
    questions = get_questions()
    correct_answers = 0
    hints_used = 0

    console.print(
        Panel(
            "[bold cyan]PHISHING DETECTIVE[/]\n"
            "Mission 01: Suspicious Message\n\n"
            "Analyze each message and identify the safest response.",
            border_style="cyan",
        )
    )

    for index, question in enumerate(questions, start=1):
        console.print(
            f"\n[bold cyan]Question {index}/{len(questions)}[/]"
        )
        console.print(
            Panel(
                question["message"],
                title="Message Evidence",
                border_style="blue",
            )
        )
        console.print(f"\n[bold]{question['prompt']}[/]")

        for option, description in question["options"].items():
            console.print(f"[green]{option}.[/] {description}")

        while True:
            choice = console.input(
                "\n[bold cyan]Answer (A-D), H for hint, or Q to quit: [/]"
            ).strip().upper()

            if choice == "Q":
                console.print(
                    "[yellow]Mission exited. Your results were not saved.[/]"
                )
                return {
                    "score": 0,
                    "completed": False,
                    "correct_answers": correct_answers,
                    "total_questions": len(questions),
                    "hints_used": hints_used,
                    "xp_awarded": 0,
                }

            if choice == "H":
                hints_used += 1

                hints = {
                    "phish-q1": (
                        "Look for pressure to act quickly and requests "
                        "for sensitive information through an unfamiliar link."
                    ),
                    "phish-q2": (
                        "Check whether the sender is trustworthy and "
                        "whether the link destination matches its description."
                    ),
                    "phish-q3": (
                        "A familiar-looking message is not automatically safe. "
                        "Think about how to verify the announcement independently."
                    ),
                }

                hint_text = hints.get(
                    question["id"],
                    "Review the message evidence and consider the safest action.",
                )

                console.print(
                    Panel(
                        hint_text,
                        title="Hint",
                        border_style="yellow",
                    )
                )
                continue

            if choice in question["options"]:
                break

            console.print(
                "[red]Invalid choice. Enter A, B, C, D, H, or Q.[/]"
            )

        is_correct = validate_answer(question, choice)

        if is_correct:
            correct_answers += 1
            console.print("[bold green]Correct![/]")
        else:
            console.print(
                f"[bold red]Incorrect. The correct answer is "
                f"{question['answer']}.[/]"
            )

        console.print(
            Panel(
                question["explanation"],
                title="Explanation",
                border_style="cyan",
            )
        )



    score = calculate_mission_score(
        correct_answers,
        len(questions),
        hints_used,
    )

    result = record_mission_attempt(
    user_id=user_id,
    mission_id="phishing-001",
    base_score=score,
    completed=True,
    hints_used=0,
    )


    debrief = Text()
    debrief.append("MISSION STATUS   ", style="dim")
    debrief.append("COMPLETE\n", style="bold bright_green")

    debrief.append("CORRECT ANSWERS  ", style="dim")
    debrief.append(
        f"{correct_answers}/{len(questions)}\n",
        style="bold bright_cyan",
    )

    debrief.append("HINTS USED       ", style="dim")
    debrief.append(f"{hints_used}\n", style="bold bright_yellow")

    debrief.append("FINAL SCORE      ", style="dim")
    debrief.append(f"{score}/100\n", style="bold bright_cyan")

    debrief.append("XP AWARDED       ", style="dim")
    debrief.append(
        f"+{result['xp_awarded']} XP",
        style="bold bright_green",
    )

    console.print(
        Panel(
            debrief,
            title="[bold bright_cyan]MISSION DEBRIEF // PHISHING-001[/]",
            subtitle="[dim]YORU TERMINAL // OPERATION REPORT[/]",
            border_style="bright_magenta",
            padding=(1, 3),
        )
    )


    return {
        "score": score,
        "completed": True,
        "correct_answers": correct_answers,
        "total_questions": len(questions),
        "hints_used": hints_used,
        "xp_awarded": result["xp_awarded"],
    }
