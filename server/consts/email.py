from typing import TypedDict


class Template(TypedDict):
    subject: str
    file: str


EMAIL_CONFIRM: Template = {
    "subject": "Please confirm your email",
    "file": "email-confirm.html.jinja",
}

PASSWORD_CONFIRM: Template = {
    "subject": "Please confirm your password reset",
    "file": "password-confirm.html.jinja",
}
