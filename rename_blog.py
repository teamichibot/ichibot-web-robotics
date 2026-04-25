import os
import re
import glob

base_dir = "/Users/ichibot/web ichibot 2"
html_files = glob.glob(f"{base_dir}/*.html")

for file_path in html_files:
    if file_path.endswith("achievements.html"):
        continue # We'll delete it later

    with open(file_path, "r") as f:
        content = f.read()

    # Nav and Footer links
    content = content.replace('href="achievements.html">Pencapaian</a>', 'href="blog.html">Blog</a>')
    content = content.replace('href="achievements.html" class="active">Pencapaian</a>', 'href="blog.html" class="active">Blog</a>')
    content = content.replace('href="achievements.html"', 'href="blog.html"')

    # Back links in detail pages
    content = content.replace('Kembali ke Pencapaian', 'Kembali ke Blog')
    content = content.replace('Kategori Pencapaian', 'Kategori Blog')

    # Index page specific
    if file_path.endswith("index.html"):
        content = content.replace('<h2>Pencapaian Terbaru</h2>', '<h2>Blog Terbaru</h2>')
        # Also fix the "Pencapaian Ichibot" in the hero if any
        content = content.replace('<h1>Pencapaian Ichibot</h1>', '<h1>Blog Ichibot</h1>')
        # Replace the badges on the index page from KemenanganLomba to Juara
        content = content.replace('<span class="badge badge-red">#KemenanganLomba</span>', '<span class="badge badge-red">#Juara</span>')

    # Detail pages specific
    if "achievement-" in file_path:
        content = content.replace('<span class="badge badge-red">Kemenangan Lomba', '<span class="badge badge-red">Juara')

    with open(file_path, "w") as f:
        f.write(content)

# Update blog.html specifically
with open(f"{base_dir}/blog.html", "r") as f:
    blog_content = f.read()

# Update Hero
blog_content = blog_content.replace('<h1>Pencapaian</h1>', '<h1>Blog</h1>')
blog_content = blog_content.replace('Index Postingan Blog: Kategori Pencapaian', 'Blog & Berita')
blog_content = blog_content.replace('Menampilkan semua postingan blog yang difilter dengan kata kunci "Pencapaian".', 'Kumpulan tutorial, berita, event, dan pencapaian juara dari Ichibot Robotics.')
blog_content = blog_content.replace('Pencapaian — Ichibot Robotics', 'Blog — Ichibot Robotics')

# Replace the filters
filters = """
      <div class="filter-tabs reveal reveal-d1">
        <button class="filter-tab active" data-filter="semua">Semua</button>
        <button class="filter-tab" data-filter="juara">Juara</button>
        <button class="filter-tab" data-filter="berita">Berita</button>
        <button class="filter-tab" data-filter="tutorial">Tutorial</button>
        <button class="filter-tab" data-filter="ekspor">Ekspor</button>
        <button class="filter-tab" data-filter="komunitas">Komunitas</button>
        <button class="filter-tab" data-filter="milestone">Milestone</button>
      </div>
"""
blog_content = re.sub(r'<div class="filter-tabs reveal reveal-d1">.*?</div>', filters, blog_content, flags=re.DOTALL)

# Re-categorize the cards
# Currently they might be "pencapaian", "berita", "tutorial", or "perlombaan", "ekspor" etc.
# We will just rewrite the data-category based on the card title or content.
# Let's map titles to categories
category_map = {
    "Juara 1 Tingkat Nasional Universitas Brawijaya": "juara",
    "Juara Umum Line Follower UTM Malaysia": "juara",
    "Ultimate 5 Max Tembus Pasar Jerman": "ekspor",
    "Robot Sumo 1 Kg Terjual ke Jepang": "ekspor",
    "Kopdar Nasional 500+ Pengguna di Yogyakarta": "komunitas",
    "Perayaan 10 Tahun Ichibot Robotics": "milestone",
    "Panduan Lengkap Tuning PID untuk Line Follower": "tutorial",
    "Rilis Update Firmware Chios v3.0": "berita"
}

for title, cat in category_map.items():
    # Find the wrapper div for this title and change its data-category
    # The structure is <div class="achievement-card-wrap" data-category="..."> ... <h3 class="achievement-card-title">TITLE</h3>
    # Regex to find the whole card start up to the title
    pattern = r'(<div class="achievement-card-wrap" data-category=")[^"]+(">[^<]*<div class="glass-card achievement-card">.*?<h3 class="achievement-card-title">[^<]*?' + re.escape(title) + r'[^<]*?</h3>)'
    blog_content = re.sub(pattern, r'\g<1>' + cat + r'\g<2>', blog_content, flags=re.DOTALL)

# Update badges in blog.html
blog_content = blog_content.replace('<span class="badge badge-red">#KemenanganLomba</span>', '<span class="badge badge-red">#Juara</span>')

with open(f"{base_dir}/blog.html", "w") as f:
    f.write(blog_content)

# Delete achievements.html as it's no longer used
try:
    os.remove(f"{base_dir}/achievements.html")
except:
    pass

print("Pencapaian changed to Blog, and Juara category added.")
