# 📸 Ephemere — Automated Photo Delivery Script

This script automatically sends personalized emails with:

* A fully formatted HTML email (with inline images such as the logo or icons)
* A ZIP file containing the recipient’s photos
* Gmail SMTP authentication
* Automatic JPEG renaming + ZIP creation
* Automatic archival of processed files

---

## ✅ 1. Requirements

### **Python**

You must have **Python 3.9+** installed.

Check your version:

```bash
python3 --version
```

If missing, install Python from:
[https://www.python.org/downloads/](https://www.python.org/downloads/)

---

## ✅ 2. Install Dependencies

From the project root, run:

```bash
python3 -m pip install beautifulsoup4
```

No other external packages are required (everything else is in the Python standard library).

---

## ✅ 3. Project Structure

Your repository should look like this:

```
/project-root
│
├── send_photos.py        # Your script
├── email.html            # HTML template for your email
├── Ephemere_Logo_Cropped_Black.png
├── icon_flickr.svg
├── icon_instagram.svg
├── icon_discord.svg
│
├── to_send/              # Input folder
│   ├── recipient1@email.com/
│   │   ├── photo1.jpg
│   │   ├── photo2.jpg
│   │   └── ...
│   ├── someone_else@gmail.com/
│   │   ├── ...
│   └── ...
│
└── sent/                 # Auto-generated archive output
```

### **Important**

* `to_send/` **must** exist.
* Inside `to_send/`, create a folder **named exactly as the recipient's email address**.
* Put their `.jpg/.jpeg` photos inside.
* The script will rename, zip, send, then move the ZIP file into `/sent`.

---

## ✅ 4. Configure Gmail

The script uses Gmail SMTP with an **App Password**.

Steps:

1. Enable 2-factor authentication on your Google account
2. Go to **Security → App Passwords**
3. Generate a new password
4. Paste it in the script:

```python
GMAIL_ADDRESS = "SENDER_EMAIL"
GMAIL_APP_PASSWORD = "APP_PASSWORD"
```

---

## ✅ 5. How the Script Works

### **1. Load email.html**

* Reads your HTML template
* Finds all `<img src="./...">`
* Embeds them as inline images using CID
* Rewrites the HTML so images display correctly in email clients

### **2. Process each recipient folder**

For each folder inside `to_send/`:

1. Rename photos → `image_01.jpeg`, `image_02.jpeg`, …
2. ZIP the folder into `recipient_email.zip`
3. Send the email:

   * HTML body
   * Inline logo/icons
   * ZIP attachment
4. Move the ZIP to `/sent`

---

## ✅ 6. Run the Script

From the repo root:

```bash
python3 send_photos.py
```

You will see logs like:

```
Processing example@gmail.com...
✅ Sent email to example@gmail.com
📦 Moved example@gmail.com and its zip to 'sent'
```

---

## ❗ Troubleshooting

| Issue                       | Solution                                                                                  |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| Email images not displaying | Check `<img src="./yourfile.ext">` paths and ensure the file exists next to `email.html`. |
| Gmail blocks the login      | Make sure you're using an **App Password**, not your normal one.                          |
| Script finds no folders     | Ensure `to_send/` contains subfolders named after actual email addresses.                 |

---

