import os
import re

base_dir = "/Users/ichibot/web ichibot 2"

# 1. Update products.html
with open(f"{base_dir}/products.html", "r") as f:
    products_content = f.read()

product_links = {
    "Ichiduino Basic+": "product-ichiduino-basic-plus.html",
    "Ichiduino Pro": "product-ichiduino-pro.html",
    "Sumo 500g": "product-sumo-500g.html",
    "Sumo 1 Kg": "product-sumo-1kg.html",
    "Transporter Mecanum Pro": "product-transporter-mecanum-pro.html", # Put Pro before normal to avoid matching wrong one
    "Transporter Mecanum": "product-transporter-mecanum.html",
    "Transporter Ultimate Omni": "product-transporter-omni.html",
    "Sumo 2 Kg": "product-sumo-2kg.html",
    "Mobile Robot Omnidirectional myRIO 1900": "product-myrio-1900.html",
    "Mobile Robot Mecanum myRIO 1950": "product-myrio-1950.html"
}

for name, link in product_links.items():
    # Regex to find the Detail button specifically for this product.
    # We find the name, and then the first href="#" after it.
    pattern = r'(<h3 class="product-card-name"[^>]*>' + re.escape(name) + r'</h3>.*?<a href=") #(")'
    products_content = re.sub(pattern, r'\g<1>' + link + r'\g<2>', products_content, flags=re.DOTALL)

with open(f"{base_dir}/products.html", "w") as f:
    f.write(products_content)


# 2. Update pelatihan.html
with open(f"{base_dir}/pelatihan.html", "r") as f:
    pelatihan_content = f.read()

pelatihan_links = {
    "Pelatihan Line Follower Dasar": "pelatihan-basic.html",
    "Pelatihan Line Follower Perlombaan": "pelatihan-competition.html",
    "Pelatihan MyRIO 1900 Pengoperasian": "pelatihan-myrio.html"
}

for name, link in pelatihan_links.items():
    pattern = r'(<h3 class="product-card-name"[^>]*>' + re.escape(name) + r'</h3>.*?<a href=") #(")'
    pelatihan_content = re.sub(pattern, r'\g<1>' + link + r'\g<2>', pelatihan_content, flags=re.DOTALL)

with open(f"{base_dir}/pelatihan.html", "w") as f:
    f.write(pelatihan_content)


# 3. Update achievements.html
with open(f"{base_dir}/achievements.html", "r") as f:
    achievements_content = f.read()

achievement_links = {
    "🏆 Juara 1 Tingkat Nasional Universitas Brawijaya": "achievement-ub.html",
    "🇩🇪 Ultimate 5 Max Tembus Pasar Jerman": "achievement-export-germany.html",
    "Kopdar Nasional 500+ Pengguna di Yogyakarta": "achievement-meetup.html",
    "🇯🇵 Robot Sumo 1 Kg Terjual ke Jepang": "achievement-japan.html",
    "Perayaan 10 Tahun Ichibot Robotics": "achievement-10years.html",
    "🇲🇾 Juara Umum Line Follower UTM Malaysia": "achievement-utm.html"
}

for name, link in achievement_links.items():
    pattern = r'(<h3 class="achievement-card-title">' + re.escape(name) + r'</h3>\s*<p class="achievement-card-desc">.*?</p>)'
    replacement = r'\g<1>\n              <a href="' + link + r'" class="btn btn-ghost btn-sm" style="margin-top: 12px; width: 100%;">Baca Selengkapnya</a>'
    achievements_content = re.sub(pattern, replacement, achievements_content)

with open(f"{base_dir}/achievements.html", "w") as f:
    f.write(achievements_content)


# 4. Update index.html
with open(f"{base_dir}/index.html", "r") as f:
    index_content = f.read()

# Replace product links in index
for name, link in product_links.items():
    pattern = r'(<h3 class="product-card-name"[^>]*>' + re.escape(name) + r'</h3>.*?<a href=") (products\.html")'
    index_content = re.sub(pattern, r'\g<1>' + link + r'"', index_content, flags=re.DOTALL)

# Add read more to achievements in index
index_achievement_links = {
    "Juara 1 Tingkat Nasional Universitas Brawijaya": "achievement-ub.html",
    "Ultimate 5 Max Tembus Pasar Jerman": "achievement-export-germany.html",
    "Kopdar Nasional 500+ Pengguna": "achievement-meetup.html"
}
for name, link in index_achievement_links.items():
    pattern = r'(<h3 class="achievement-card-title">' + re.escape(name) + r'</h3>\s*<p class="achievement-card-desc">.*?</p>)'
    replacement = r'\g<1>\n              <a href="' + link + r'" class="btn btn-ghost btn-sm" style="margin-top: 12px; width: 100%;">Baca Selengkapnya</a>'
    index_content = re.sub(pattern, replacement, index_content)

# Update events links in index to detail pages
# Slide event
index_content = index_content.replace('href="achievements.html" class="btn btn-red btn-lg">Semua Events', 'href="events.html" class="btn btn-red btn-lg">Semua Events')
index_content = index_content.replace('href="achievements.html" class="section-header-action">Lihat Semua &rarr;</a>\n        </div>\n\n        <div class="events-grid">', 'href="events.html" class="section-header-action">Lihat Semua &rarr;</a>\n        </div>\n\n        <div class="events-grid">')

index_content = index_content.replace('<h3 class="event-card-title">Line Follower Contest — ITS Surabaya</h3>', '<h3 class="event-card-title">Line Follower Contest — ITS Surabaya</h3>\n              <a href="event-its.html" class="btn btn-ghost btn-sm" style="margin-top: 12px;">Detail Event</a>')
index_content = index_content.replace('<h3 class="event-card-title">Workshop Tuning PID — Ichibot Yogyakarta</h3>', '<h3 class="event-card-title">Workshop Tuning PID — Ichibot Yogyakarta</h3>\n              <a href="event-workshop-pid.html" class="btn btn-ghost btn-sm" style="margin-top: 12px;">Detail Event</a>')
index_content = index_content.replace('<h3 class="event-card-title">Robot Contest Nasional — Universitas Brawijaya</h3>', '<h3 class="event-card-title">Robot Contest Nasional — Universitas Brawijaya</h3>\n              <a href="event-ub.html" class="btn btn-ghost btn-sm" style="margin-top: 12px;">Detail Event</a>')

with open(f"{base_dir}/index.html", "w") as f:
    f.write(index_content)


# 5. Add events.html to Footer in ALL html files
import glob
files = glob.glob(f"{base_dir}/*.html")

for file in files:
    with open(file, "r") as f:
        content = f.read()
    
    # Replace the footer links
    footer_nav = """<h4 class="footer-heading">Navigasi</h4>
          <div class="footer-links">
            <a href="index.html">Beranda</a>
            <a href="products.html">Produk</a>
            <a href="pelatihan.html">Pelatihan</a>
            <a href="achievements.html">Pencapaian</a>
            <a href="events.html">Events</a>
            <a href="community.html">Komunitas</a>
            <a href="about.html">Tentang Kami</a>
          </div>"""
    content = re.sub(r'<h4 class="footer-heading">Navigasi</h4>\s*<div class="footer-links">.*?</div>', footer_nav, content, flags=re.DOTALL)
    
    with open(file, "w") as f:
        f.write(content)

print("Links replaced.")
