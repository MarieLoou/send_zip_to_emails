import os
import re
import shutil
import smtplib
import zipfile
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
from bs4 import BeautifulSoup  # pip install beautifulsoup4
# -------------------------
# CONFIG
# -------------------------
GMAIL_ADDRESS = "" # sender's email
GMAIL_APP_PASSWORD = "" # app password

BASE_DIR = Path(__file__).parent / "to_send"
SENT_DIR = Path(__file__).parent / "sent"
SENT_DIR.mkdir(exist_ok=True)

EMAIL_HTML_PATH = Path(__file__).parent / "email.html"

# -------------------------
# FUNCTIONS
# -------------------------
def load_html_with_inline_images():
    """Load email.html and embed local images with CID references"""
    html = EMAIL_HTML_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    msg = EmailMessage()
    msg["From"] = GMAIL_ADDRESS
    msg["Subject"] = "De belles photos pour ton CV 📸"

    # Find local <img src="./...">
    for img in soup.find_all("img", src=True):
        src = img["src"]
        if src.startswith("./"):
            img_path = EMAIL_HTML_PATH.parent / src[2:]
            if img_path.exists():
                cid = make_msgid(domain="ephemere.local")[1:-1]  # remove <>
                img["src"] = f"cid:{cid}"

                # Determine maintype/subtype
                ext = img_path.suffix.lower()
                if ext in [".png", ".jpg", ".jpeg"]:
                    maintype, subtype = "image", ext[1:]
                elif ext == ".svg":
                    maintype, subtype = "image", "svg+xml"
                else:
                    print(f"⚠️ Unsupported image type: {img_path}")
                    continue

                with open(img_path, "rb") as f:
                    msg.add_related(
                        f.read(),
                        maintype=maintype,
                        subtype=subtype,
                        cid=f"<{cid}>",
                        filename=img_path.name,
                    )
            else:
                print(f"⚠️ Image not found: {img_path}")

    msg.add_alternative(str(soup), subtype="html")
    return msg


def rename_jpegs(folder: Path):
    jpegs = sorted([f for f in folder.iterdir() if f.suffix.lower() in [".jpg", ".jpeg"]])
    for idx, f in enumerate(jpegs, start=1):
        new_name = folder / f"image_{idx:02d}.jpeg"
        f.rename(new_name)
    return folder


def zip_folder(folder: Path):
    zip_path = folder.parent / f"{folder.name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in folder.iterdir():
            if file.is_file() and file.suffix.lower() in [".jpg", ".jpeg"]:
                zipf.write(file, arcname=file.name)
    return zip_path


def send_email_with_attachment(to_email: str, attachment_path: Path):
    msg = load_html_with_inline_images()
    msg["To"] = to_email

    # Attach zip
    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="zip",
            filename=attachment_path.name
        )

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)

    print(f"✅ Sent email to {to_email}")


def process_folder(subfolder: Path):
    recipient = subfolder.name
    print(f"Processing {recipient}...")

    rename_jpegs(subfolder)
    zip_path = zip_folder(subfolder)
    send_email_with_attachment(recipient, zip_path)

    shutil.move(str(zip_path), SENT_DIR / zip_path.name)
    print(f"📦 Moved {recipient} and its zip to 'sent'\n")


# -------------------------
# MAIN LOOP
# -------------------------
def main():
    for subfolder in BASE_DIR.iterdir():
        if subfolder.is_dir() and subfolder.name != "sent":
            process_folder(subfolder)

if __name__ == "__main__":
    main()