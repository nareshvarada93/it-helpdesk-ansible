
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "local-development-key-change-before-production"
    )

    DATABASE = os.path.join(BASE_DIR, "helpdesk.db")

    ANSIBLE_INVENTORY = os.path.join(
        BASE_DIR, "ansible", "inventory", "hosts.ini"
    )

    ANSIBLE_PLAYBOOK = os.path.join(
        BASE_DIR, "ansible", "playbooks", "health_check.yml"
    )

    REPORT_DIR = os.path.join(BASE_DIR, "reports")
