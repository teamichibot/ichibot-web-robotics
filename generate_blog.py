import os
import re

base_dir = "/Users/ichibot/web ichibot 2"

with open(f"{base_dir}/achievements.html", "r") as f:
    content = f.read()

# Generate blog.html from achievements.html
blog_content = content.replace("<title>Pencapaian — Ichibot Robotics</title>", "<title>Blog & Berita — Ichibot Robotics</title>")

# Update Navigation to show Blog (Wait, the nav doesn't have Blog. I won't change the main nav).
blog_content = blog_content.replace('href="achievements.html" class="active"', 'href="achievements.html"')

# Update Hero
blog_content = blog_content.replace('<div class="section-label">Jejak Sang Juara</div>', '<div class="section-label">Berita & Insight</div>')
blog_content = blog_content.replace('<h1>Pencapaian Ichibot</h1>', '<h1>Blog Ichibot</h1>')
blog_content = blog_content.replace('<p class="text-secondary">Dari kejuaraan nasional hingga ekspor internasional ke 17+ negara.</p>', '<p class="text-secondary">Kumpulan postingan, tutorial, berita, dan pencapaian terbaru dari Ichibot Robotics.</p>')

# Update Filters in blog.html
blog_filters = """
      <div class="filter-tabs reveal reveal-d1">
        <button class="filter-tab active" data-filter="semua">Semua</button>
        <button class="filter-tab" data-filter="pencapaian">Pencapaian</button>
        <button class="filter-tab" data-filter="berita">Berita</button>
        <button class="filter-tab" data-filter="tutorial">Tutorial</button>
      </div>
"""
blog_content = re.sub(r'<div class="filter-tabs reveal reveal-d1">.*?</div>', blog_filters, blog_content, flags=re.DOTALL)

# In blog.html, all the existing achievements need their data-category set to "pencapaian" so they filter correctly.
blog_content = re.sub(r'data-category="(perlombaan|ekspor|komunitas|milestone)"', r'data-category="pencapaian"', blog_content)

# Add some dummy Berita and Tutorial posts to blog.html
dummy_posts = """
        <!-- Tutorial 1 -->
        <div class="achievement-card-wrap" data-category="tutorial">
          <div class="glass-card achievement-card">
            <div class="achievement-card-image">
              <img src="https://placehold.co/800x600/111111/444444?text=Tutorial+PID" alt="Tutorial PID">
            </div>
            <div class="achievement-card-body">
              <div class="achievement-card-meta">
                <span class="badge badge-gray">#Tutorial</span>
                <span class="achievement-card-date">10 Mei 2026</span>
              </div>
              <h3 class="achievement-card-title">Panduan Lengkap Tuning PID untuk Line Follower</h3>
              <p class="achievement-card-desc">Pelajari dasar-dasar tuning Proporsional, Integral, dan Derivatif untuk membuat pergerakan robot lebih smooth.</p>
              <a href="#" class="btn btn-ghost btn-sm" style="margin-top: 12px; width: 100%;">Baca Selengkapnya</a>
            </div>
          </div>
        </div>

        <!-- Berita 1 -->
        <div class="achievement-card-wrap" data-category="berita">
          <div class="glass-card achievement-card">
            <div class="achievement-card-image">
              <img src="https://placehold.co/800x450/111111/444444?text=Rilis+Chios+3" alt="Rilis Chios 3">
            </div>
            <div class="achievement-card-body">
              <div class="achievement-card-meta">
                <span class="badge badge-white">#Berita</span>
                <span class="achievement-card-date">02 Apr 2026</span>
              </div>
              <h3 class="achievement-card-title">Rilis Update Firmware Chios v3.0</h3>
              <p class="achievement-card-desc">Update terbaru untuk sistem operasi Chios membawa fitur kalibrasi otomatis dan antarmuka web yang diperbarui.</p>
              <a href="#" class="btn btn-ghost btn-sm" style="margin-top: 12px; width: 100%;">Baca Selengkapnya</a>
            </div>
          </div>
        </div>
"""
# Insert dummy posts inside masonry grid
grid_insert_pos = blog_content.find('<div class="masonry-grid">') + len('<div class="masonry-grid">\n')
blog_content = blog_content[:grid_insert_pos] + dummy_posts + blog_content[grid_insert_pos:]

with open(f"{base_dir}/blog.html", "w") as f:
    f.write(blog_content)


# Update achievements.html to reflect it's a filtered blog index
# Keep the current layout, but change the title/subtitle to match the user's intent.
achievements_content = content
achievements_content = achievements_content.replace('<div class="section-label">Jejak Sang Juara</div>', '<div class="section-label">Index Postingan Blog: Kategori Pencapaian</div>')
achievements_content = achievements_content.replace('<h1>Pencapaian Ichibot</h1>', '<h1>Pencapaian</h1>')
achievements_content = achievements_content.replace('<p class="text-secondary">Dari kejuaraan nasional hingga ekspor internasional ke 17+ negara.</p>', '<p class="text-secondary">Menampilkan semua postingan blog yang difilter dengan kata kunci "Pencapaian".</p>')

# Keep the sub-filters in achievements.html (Perlombaan, Ekspor, Komunitas, Milestone) since it makes sense for sub-filtering the achievements category.
# Or we can remove the filter tabs to make it simple. Let's keep them as sub-filters.

with open(f"{base_dir}/achievements.html", "w") as f:
    f.write(achievements_content)

print("Blog index created and achievements updated.")
