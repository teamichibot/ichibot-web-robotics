import os

base_dir = "/Users/ichibot/web ichibot 2"

with open(f"{base_dir}/achievements.html", "r") as f:
    content = f.read()

# Modify Title, Meta, Hero
content = content.replace("<title>Pencapaian — Ichibot Robotics</title>", "<title>Events — Ichibot Robotics</title>")
content = content.replace('href="achievements.html" class="active"', 'href="achievements.html"')
# We don't have events in nav but let's keep it as is.
content = content.replace("Jejak Sang Juara", "Kalender Kegiatan")
content = content.replace("Pencapaian Ichibot", "Events & Updates")
content = content.replace("Dari kejuaraan nasional hingga ekspor internasional ke 17+ negara.", "Daftar kompetisi, workshop, dan update terbaru seputar dunia robotika.")

# Replace Filter tabs
filters = """
      <div class="filter-tabs reveal reveal-d1">
        <button class="filter-tab active" data-filter="semua">Semua</button>
        <button class="filter-tab" data-filter="kompetisi">Kompetisi</button>
        <button class="filter-tab" data-filter="workshop">Workshop</button>
      </div>
"""
content = content.replace("""      <div class="filter-tabs reveal reveal-d1">
        <button class="filter-tab active" data-filter="semua">Semua</button>
        <button class="filter-tab" data-filter="perlombaan">Perlombaan</button>
        <button class="filter-tab" data-filter="ekspor">Ekspor</button>
        <button class="filter-tab" data-filter="komunitas">Komunitas</button>
        <button class="filter-tab" data-filter="milestone">Milestone</button>
      </div>""", filters)

# Replace Grid Content
events_grid = """
      <div class="masonry-grid">
        <div class="achievement-card-wrap" data-category="kompetisi">
          <div class="glass-card achievement-card">
            <div class="achievement-card-image">
              <img src="https://placehold.co/800x600/111111/444444?text=Event+ITS" alt="ITS Surabaya">
            </div>
            <div class="achievement-card-body">
              <div class="achievement-card-meta">
                <span class="badge badge-red">#Kompetisi</span>
                <span class="achievement-card-date">14 Jun 2026</span>
              </div>
              <h3 class="achievement-card-title">Line Follower Contest — ITS Surabaya</h3>
              <p class="achievement-card-desc">Kompetisi line follower tingkat nasional di Institut Teknologi Sepuluh Nopember (ITS) Surabaya.</p>
              <a href="event-its.html" class="btn btn-ghost btn-sm" style="margin-top: 12px; width: 100%;">Baca Selengkapnya</a>
            </div>
          </div>
        </div>

        <div class="achievement-card-wrap" data-category="workshop">
          <div class="glass-card achievement-card">
            <div class="achievement-card-image">
              <img src="https://placehold.co/800x450/111111/444444?text=Workshop+PID" alt="Workshop PID">
            </div>
            <div class="achievement-card-body">
              <div class="achievement-card-meta">
                <span class="badge badge-white">#Workshop</span>
                <span class="achievement-card-date">22 Jun 2026</span>
              </div>
              <h3 class="achievement-card-title">Workshop Tuning PID — Ichibot Yogyakarta</h3>
              <p class="achievement-card-desc">Workshop eksklusif mempelajari cara tuning PID untuk line follower dan robot sumo.</p>
              <a href="event-workshop-pid.html" class="btn btn-ghost btn-sm" style="margin-top: 12px; width: 100%;">Baca Selengkapnya</a>
            </div>
          </div>
        </div>

        <div class="achievement-card-wrap" data-category="kompetisi">
          <div class="glass-card achievement-card">
            <div class="achievement-card-image">
              <img src="https://placehold.co/800x533/111111/444444?text=Event+UB" alt="Robot Contest UB">
            </div>
            <div class="achievement-card-body">
              <div class="achievement-card-meta">
                <span class="badge badge-red">#Kompetisi</span>
                <span class="achievement-card-date">05 Jul 2026</span>
              </div>
              <h3 class="achievement-card-title">Robot Contest Nasional — Universitas Brawijaya</h3>
              <p class="achievement-card-desc">Ajang kompetisi robot nasional bergengsi di Universitas Brawijaya dengan berbagai kategori perlombaan.</p>
              <a href="event-ub.html" class="btn btn-ghost btn-sm" style="margin-top: 12px; width: 100%;">Baca Selengkapnya</a>
            </div>
          </div>
        </div>
      </div>
"""

start_grid = content.find('<div class="masonry-grid">')
end_grid = content.find('</div>\n    </div>\n  </section>')
content = content[:start_grid] + events_grid + content[end_grid:]

with open(f"{base_dir}/events.html", "w") as f:
    f.write(content)

print("Events page generated.")
