
import sqlite3
from flask import current_app


def get_db():
    connection = sqlite3.connect(
        current_app.config["DATABASE"],
        timeout=10
    )
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            diagnostic_report TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def get_all_tickets():
    connection = get_db()
    tickets = connection.execute(
        "SELECT * FROM tickets ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return tickets


def create_ticket(title, description, priority):
    connection = get_db()

    connection.execute("""
        INSERT INTO tickets (title, description, priority)
        VALUES (?, ?, ?)
    """, (title, description, priority))

    connection.commit()
    connection.close()


def get_ticket(ticket_id):
    connection = get_db()

    ticket = connection.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    ).fetchone()

    connection.close()
    return ticket


def update_status(ticket_id, status):
    connection = get_db()

    connection.execute(
        "UPDATE tickets SET status = ? WHERE id = ?",
        (status, ticket_id)
    )

    connection.commit()
    connection.close()


def save_report(ticket_id, report):
    connection = get_db()

    connection.execute(
        "UPDATE tickets SET diagnostic_report = ? WHERE id = ?",
        (report, ticket_id)
    )

    connection.commit()
    connection.close()
