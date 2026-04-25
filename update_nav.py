import os
import re
import glob

base_dir = "/Users/ichibot/web ichibot 2"
html_files = glob.glob(f"{base_dir}/*.html")

new_nav = """      <div class="nav-links">
        <div class="nav-item">
          <a href="#" style="cursor: pointer;">Produk & Layanan <i class="fa-solid fa-chevron-down" style="font-size: 0.8em; margin-left: 4px;"></i></a>
          <div class="nav-dropdown">
            <a href="products.html">Robot Edukasi</a>
            <a href="pelatihan.html">Pelatihan Robot</a>
            <a href="https://wa.me/6281234567890?text=Halo%20Ichibot%2C%20saya%20ingin%20info%20tentang%20Servis%20Robot" target="_blank">Servis Robot</a>
          </div>
        </div>
        <div class="nav-item">
          <a href="#" style="cursor: pointer;">Komunitas <i class="fa-solid fa-chevron-down" style="font-size: 0.8em; margin-left: 4px;"></i></a>
          <div class="nav-dropdown">
            <a href="blog.html">Blog & Berita</a>
            <a href="blog.html">Juara / Hall of Champions</a>
            <a href="community.html">Komunitas Ichibot</a>
            <a href="about.html">Tentang Kami</a>
          </div>
        </div>
        <a href="events.html">Event Update</a>
      </div>"""

for file_path in html_files:
    with open(file_path, "r") as f:
        content = f.read()

    # The nav-links block can vary slightly (some have active classes).
    # We will just replace everything from <div class="nav-links"> to its closing </div>
    pattern = r'<div class="nav-links">.*?</div>\s*(?=\s*<div class="nav-cta">)'
    content = re.sub(pattern, new_nav + '\n', content, flags=re.DOTALL)
    
    with open(file_path, "w") as f:
        f.write(content)

# Append CSS to components.css
css_addition = """

/* Dropdown Styles */
.nav-item {
  position: relative;
  display: flex;
  align-items: center;
}

.nav-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 220px;
  background: rgba(15, 15, 15, 0.85);
  backdrop-filter: blur(var(--blur-md));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-card);
  padding: 8px 0;
  display: flex;
  flex-direction: column;
  opacity: 0;
  visibility: hidden;
  transform: translateY(10px);
  transition: all var(--transition-base);
  box-shadow: var(--shadow-card);
  z-index: 100;
}

.nav-item:hover .nav-dropdown {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.nav-dropdown a {
  padding: 10px 20px;
  font-size: 0.95rem;
  width: 100%;
  border-radius: 0;
  color: var(--text-secondary);
}

.nav-dropdown a:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

/* Mobile adjustments */
@media (max-width: 960px) {
  .nav-item {
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
  }
  .nav-dropdown {
    position: static;
    opacity: 1;
    visibility: visible;
    transform: none;
    box-shadow: none;
    border: none;
    background: rgba(255, 255, 255, 0.02);
    border-left: 1px solid var(--glass-border);
    border-radius: 0;
    padding: 4px 0;
    margin-left: 16px;
    margin-top: 8px;
    min-width: 100%;
  }
}
"""

with open(f"{base_dir}/css/components.css", "a") as f:
    f.write(css_addition)

print("Navigation updated across all files and CSS injected.")
