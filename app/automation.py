
import subprocess
from pathlib import Path
from flask import current_app


def run_health_check(ticket_id):

    inventory = current_app.config["ANSIBLE_INVENTORY"]
    playbook = current_app.config["ANSIBLE_PLAYBOOK"]
    report_dir = Path(current_app.config["REPORT_DIR"])

    report_dir.mkdir(parents=True, exist_ok=True)

    command = [
        "ansible-playbook",
        "-i", inventory,
        playbook
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
            cwd=current_app.root_path + "/.."
        )

        output = result.stdout
        error = result.stderr

        if result.returncode == 0:
            status = "SUCCESS"
        else:
            status = "FAILED"

        report = (
            f"Automation Status: {status}\n\n"
            f"Exit Code: {result.returncode}\n\n"
            f"OUTPUT:\n{output}\n\n"
            f"ERROR:\n{error}"
        )

    except subprocess.TimeoutExpired:
        report = "Automation FAILED: Playbook execution timed out."

    except FileNotFoundError:
        report = (
            "Automation FAILED: Ansible executable not found. "
            "Check Ansible installation."
        )

    except OSError as error:
        report = f"Automation FAILED: {error}"

    report_file = report_dir / f"ticket_{ticket_id}.txt"
    report_file.write_text(report, encoding="utf-8")

    return report
