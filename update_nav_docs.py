import os
import re
import glob

base_dir = "/Users/ichibot/web ichibot 2"
html_files = glob.glob(f"{base_dir}/*.html")

for file_path in html_files:
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Add Docs to navbar
    # Find Event Update and append Docs
    content = content.replace(
        '<a href="events.html">Event Update</a>\n      </div>',
        '<a href="events.html">Event Update</a>\n        <a href="https://docs.ichibot.id" target="_blank">Docs</a>\n      </div>'
    )
    
    # Alternatively, if spacing differs, use regex:
    content = re.sub(
        r'(<a href="events\.html">Event Update</a>)\s*(</div>)',
        r'\1\n        <a href="https://docs.ichibot.id" target="_blank">Docs</a>\n      \2',
        content
    )

    # 2. Replace the nav-cta WhatsApp button with Login
    pattern_cta = r'<div class="nav-cta">\s*<a href="https://wa\.me/[^"]*"[^>]*>\s*<i class="fa-brands fa-whatsapp"></i> Hubungi Kami\s*</a>\s*</div>'
    
    # Some files might have different formatting, let's just match the whole div
    pattern_cta_general = r'<div class="nav-cta">.*?</div>'
    
    new_cta = """<div class="nav-cta">
        <a href="https://user.ichibot.id" class="btn btn-red btn-sm">
          <i class="fa-solid fa-user"></i> Login
        </a>
      </div>"""
      
    content = re.sub(pattern_cta_general, new_cta, content, flags=re.DOTALL)

    with open(file_path, "w") as f:
        f.write(content)

print("Navbar updated with Docs and Login button.")
