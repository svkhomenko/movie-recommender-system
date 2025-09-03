from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
from consts.email import Template

env = Environment(
    loader=FileSystemLoader(Path(__file__).parent.parent / "emails_templates")
)


def send_mail(email: str, template: Template, data={}):
    from_email = "Movie RS"
    to_email = email

    message = MIMEMultipart()
    message["Subject"] = template["subject"]
    message["From"] = from_email
    message["To"] = to_email

    html = env.get_template(template["file"]).render(
        data | {"client_url": os.getenv("CLIENT_URL")}
    )
    message.attach(MIMEText(html, "html"))

    with SMTP(
        os.getenv("EMAIL_HOST") or "live.smtp.mailtrap.io",
        int(os.getenv("EMAIL_PORT") or 587),
    ) as server:
        server.starttls()
        server.login(
            os.getenv("EMAIL_USERNAME") or "", os.getenv("EMAIL_PASSWORD") or ""
        )
        server.sendmail(from_email, to_email, message.as_string())
