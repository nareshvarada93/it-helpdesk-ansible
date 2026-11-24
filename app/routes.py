
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)

from app.database import (
    get_all_tickets,
    create_ticket,
    get_ticket,
    update_status,
    save_report
)

from app.automation import run_health_check

main = Blueprint("main", __name__)


@main.route("/")
def index():

    tickets = get_all_tickets()

    total = len(tickets)
    open_count = sum(t["status"] == "Open" for t in tickets)
    in_progress = sum(
        t["status"] == "In Progress" for t in tickets
    )
    resolved = sum(t["status"] == "Resolved" for t in tickets)

    return render_template(
        "index.html",
        tickets=tickets,
        total=total,
        open_count=open_count,
        in_progress=in_progress,
        resolved=resolved
    )


@main.route("/new-ticket", methods=["GET", "POST"])
def new_ticket():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "")

        if not title or not description:
            flash("Title and description are required.", "error")
            return redirect(url_for("main.new_ticket"))

        if priority not in ["Low", "Medium", "High", "Critical"]:
            flash("Please select a valid priority.", "error")
            return redirect(url_for("main.new_ticket"))

        create_ticket(title, description, priority)

        flash("Support ticket created successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("new_ticket.html")


@main.route("/ticket/<int:ticket_id>")
def ticket_detail(ticket_id):

    ticket = get_ticket(ticket_id)

    if ticket is None:
        flash("Ticket not found.", "error")
        return redirect(url_for("main.index"))

    return render_template("ticket_detail.html", ticket=ticket)


@main.route("/update-status/<int:ticket_id>", methods=["POST"])
def change_status(ticket_id):

    ticket = get_ticket(ticket_id)

    if ticket is None:
        flash("Ticket not found.", "error")
        return redirect(url_for("main.index"))

    status = request.form.get("status")

    if status not in ["Open", "In Progress", "Resolved"]:
        flash("Invalid ticket status.", "error")
        return redirect(url_for("main.ticket_detail", ticket_id=ticket_id))

    update_status(ticket_id, status)

    flash("Ticket status updated.", "success")

    return redirect(url_for("main.ticket_detail", ticket_id=ticket_id))


@main.route("/run-check/<int:ticket_id>", methods=["POST"])
def execute_check(ticket_id):

    ticket = get_ticket(ticket_id)

    if ticket is None:
        flash("Ticket not found.", "error")
        return redirect(url_for("main.index"))

    report = run_health_check(ticket_id)

    save_report(ticket_id, report)

    flash("Server diagnostic check completed.", "success")

    return redirect(url_for("main.ticket_detail", ticket_id=ticket_id))
