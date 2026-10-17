
"""Interactive gameplay for the Incident Response Simulator."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from missions.incident_response_simulator import MISSION_ID, get_questions
from missions.mission_engine import validate_answer, calculate_mission_score
from core.progression import record_mission_attempt

console = Console()


def play_incident_response(user_id: int) -> dict:
    """Run the incident response mission and record its result."""
    questions = get_questions()
    correct_answers = 0
    hints_used = 0

    console.print(
        Panel(
            "Assess the evidence, prioritize containment, preserve "
            "relevant records, and choose responsible recovery actions.",
            title="Incident Response Simulator",
            border_style="cyan",
        )
    )

    for question in questions:
        console.print(
            Panel(
                f"{question['title']}\n\n{question['evidence']}",
                title="Incident Briefing",
                border_style="blue",
            )
        )
        console.print(f"\n[bold]{question['prompt']}[/]\n")

        for letter, option in question["options"].items():
            console.print(f"[cyan]{letter}.[/] {option}")

        while True:
            choice = console.input(
                "\n[bold cyan]Your decision (A-D, H for hint): [/]"
            ).strip().upper()

            if choice == "H":
                hints_used += 1
                console.print(
                    Panel(
                        question["hint"],
                        title="Hint",
                        border_style="yellow",
                    )
                )
                continue

            if choice in question["options"]:
                break

            console.print("[red]Enter A, B, C, D, or H.[/]")

        if validate_answer(question, choice):
            correct_answers += 1
            console.print("[green]Good decision![/]")
        else:
            console.print(
                f"[red]Not the best response.[/] "
                f"Suggested answer: {question['answer']}"
            )

        console.print(f"[dim]{question['explanation']}[/]\n")

    score = calculate_mission_score(
        correct_answers,
        len(questions),
        hints_used=hints_used,
    )

    result = record_mission_attempt(
        user_id=user_id,
        mission_id=MISSION_ID,
        base_score=score,
        completed=True,
        hints_used=0,
    )

    xp_awarded = result.get("xp_awarded", 0)


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
    debrief.append(f"+{xp_awarded} XP", style="bold bright_green")

    console.print(
        Panel(
            debrief,
            title=f"[bold bright_cyan]MISSION DEBRIEF // {MISSION_ID.upper()}[/]",
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
        "xp_awarded": xp_awarded,
    }
