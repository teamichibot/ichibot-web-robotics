import os
import re

base_dir = "/Users/ichibot/web ichibot 2"

files = [
    "achievement-ub.html",
    "achievement-export-germany.html",
    "achievement-meetup.html",
    "achievement-japan.html",
    "achievement-10years.html",
    "achievement-utm.html"
]

for file in files:
    with open(f"{base_dir}/{file}", "r") as f:
        content = f.read()

    # Extract info
    title_match = re.search(r'<h1 class="detail-title">(.*?)</h1>', content)
    title = title_match.group(1) if title_match else ""

    badge_match = re.search(r'<span class="badge[^>]*>(.*?)</span>', content)
    badge_html = badge_match.group(0) if badge_match else '<span class="badge badge-red">Pencapaian</span>'
    
    # Extract date from badge if possible
    date = "2025"
    if "Okt 2025" in badge_html: date = "12 Oktober 2025"
    elif "Sep 2025" in badge_html: date = "05 September 2025"
    elif "Agu 2025" in badge_html: date = "20 Agustus 2025"
    elif "Jul 2025" in badge_html: date = "15 Juli 2025"
    elif "Jun 2025" in badge_html: date = "10 Juni 2025"
    elif "Mei 2025" in badge_html: date = "28 Mei 2025"

    image_match = re.search(r'<img src="(https://placehold.co/[^"]+)" alt="([^"]+)">', content)
    image_src = image_match.group(1) if image_match else ""

    desc_match = re.search(r'<p class="detail-desc-text">\s*(.*?)\s*</p>', content, flags=re.DOTALL)
    desc = desc_match.group(1) if desc_match else ""

    # Build new main content
    blog_main = f"""
  <main>
    <article class="blog-post">
      <!-- Hero Header -->
      <header class="blog-header container" style="padding-top: 140px; padding-bottom: 40px; text-align: center; max-width: 800px;">
        <a href="achievements.html" class="text-secondary" style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 24px; text-decoration: none; font-size: 0.9rem;">
          <i class="fa-solid fa-arrow-left"></i> Kembali ke Pencapaian
        </a>
        <div style="margin-bottom: 16px;">
          {badge_html.replace('position: absolute; top: 16px; left: 16px; z-index: 2;', '')}
        </div>
        <h1 class="detail-title" style="margin-bottom: 16px; font-size: clamp(2rem, 5vw, 3.5rem); line-height: 1.2;">{title}</h1>
        <div class="text-secondary" style="font-size: 0.95rem;">
          Oleh <strong style="color: var(--text-primary);">Tim Ichibot</strong> &middot; {date}
        </div>
      </header>

      <!-- Featured Image -->
      <div class="container" style="max-width: 1000px; margin-bottom: 64px;">
        <div class="detail-image-wrap" style="border-radius: var(--radius-card-lg); overflow: hidden; box-shadow: var(--shadow-card); border: 1px solid var(--glass-border);">
          <img src="{image_src}" alt="{title}" style="width: 100%; height: auto; display: block; aspect-ratio: 21/9; object-fit: cover;">
        </div>
      </div>

      <!-- Content -->
      <div class="container" style="max-width: 760px; margin-bottom: 80px;">
        <div class="blog-content text-secondary" style="line-height: 1.8; font-size: 1.1rem; color: var(--text-secondary);">
          <p style="margin-bottom: 24px; font-size: 1.2rem; color: var(--text-primary); font-weight: 500;">{desc}</p>
          <p style="margin-bottom: 24px;">Dalam perjalanan kami mencapai titik ini, berbagai tantangan telah kami hadapi. Mulai dari meriset desain yang paling efisien, memilih komponen yang paling tangguh, hingga menguji coba algoritma di lintasan yang paling rumit sekalipun. Keberhasilan ini tidak diraih dalam semalam, melainkan melalui proses panjang dedikasi dan kolaborasi seluruh tim.</p>
          <p style="margin-bottom: 24px;">Kami ingin mengucapkan terima kasih yang sebesar-besarnya kepada seluruh anggota komunitas Ichibot. Tanpa dukungan, feedback, dan antusiasme Anda semua, pencapaian ini tidak akan pernah terwujud. Setiap diskusi di grup, setiap pertanyaan, dan setiap masukan sangat berarti bagi pengembangan produk-produk kami.</p>
          <h2 style="color: var(--text-primary); margin-top: 48px; margin-bottom: 20px; font-family: var(--font-display); font-size: 1.8rem;">Langkah Kami Selanjutnya</h2>
          <p style="margin-bottom: 24px;">Pencapaian ini bukanlah akhir dari perjalanan, melainkan awal dari tantangan baru. Ke depannya, kami berkomitmen untuk terus berinovasi dan menghadirkan solusi robotika yang tidak hanya relevan dengan kebutuhan kompetisi, tetapi juga dapat diterapkan di dunia industri.</p>
          <p style="margin-bottom: 24px;">Tetap ikuti update terbaru dari kami dan mari bersama-sama membangun ekosistem robotika yang lebih kuat di Indonesia dan di kancah internasional!</p>
        </div>

        <div style="margin-top: 64px; padding-top: 32px; border-top: 1px solid var(--glass-border); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 24px;">
          <div class="tags" style="display: flex; gap: 8px; flex-wrap: wrap;">
            <span class="badge badge-gray">Robotika</span>
            <span class="badge badge-gray">Inovasi</span>
            <span class="badge badge-gray">Pencapaian</span>
          </div>
          <div class="share" style="display: flex; gap: 12px; align-items: center;">
            <span class="text-secondary" style="font-size: 0.9rem;">Bagikan:</span>
            <a href="#" class="btn btn-ghost btn-sm" style="padding: 8px 12px; border-radius: 50%;"><i class="fa-brands fa-twitter"></i></a>
            <a href="#" class="btn btn-ghost btn-sm" style="padding: 8px 12px; border-radius: 50%;"><i class="fa-brands fa-facebook"></i></a>
            <a href="#" class="btn btn-ghost btn-sm" style="padding: 8px 12px; border-radius: 50%;"><i class="fa-brands fa-whatsapp"></i></a>
          </div>
        </div>
      </div>
    </article>
  </main>
"""

    # Replace <main>...</main> with blog_main
    content = re.sub(r'<main>.*?</main>', blog_main, content, flags=re.DOTALL)

    # Make sure link back goes to blog or achievements. Let's make it back to achievements since that's the filtered view.
    
    with open(f"{base_dir}/{file}", "w") as f:
        f.write(content)

print("Achievement details converted to blog post layouts.")
