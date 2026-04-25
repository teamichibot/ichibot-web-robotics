import os
import re

base_dir = "/Users/ichibot/web ichibot 2"

with open(f"{base_dir}/product-detail.html", "r") as f:
    template = f.read()

def create_page(filename, title, image_text, badge, price_html, desc, specs_list1, specs_list2, btn_text, is_event=False):
    content = template.replace("Ultimate 5 Max — Ichibot Robotics", f"{title} — Ichibot Robotics")
    content = content.replace("Ultimate 5 Max adalah robot line follower dengan spesifikasi tertinggi dari Ichibot.", f"{title} di Ichibot Robotics.")
    
    # Hero section
    # Replace Image
    content = re.sub(r'<img src="https://placehold.co/[^"]+" alt="[^"]+">', 
                     f'<img src="https://placehold.co/800x800/111111/444444?text={image_text}" alt="{title}">', content)
    
    # Replace Badges
    content = re.sub(r'<span class="badge badge-red"[^>]*>.*?</span>', badge, content)
    
    # Replace Title
    content = re.sub(r'<h1 class="detail-title">.*?</h1>', f'<h1 class="detail-title">{title}</h1>', content)
    
    # Replace Price
    if price_html:
        content = re.sub(r'<div class="detail-price-wrap">.*?</div>', f'<div class="detail-price-wrap">\n{price_html}\n            </div>', content, flags=re.DOTALL)
    else:
        content = re.sub(r'<div class="detail-price-wrap">.*?</div>', '', content, flags=re.DOTALL)
    
    # Replace Description
    content = re.sub(r'<p class="detail-desc-text">.*?</p>\s*<p class="detail-desc-text" style="margin-bottom: 0;">.*?</p>', f'<p class="detail-desc-text">\n                {desc}\n              </p>', content, flags=re.DOTALL)
    
    # Replace Specs
    if specs_list1 or specs_list2:
        specs1_html = "\n".join([f"              <li>{s}</li>" for s in specs_list1])
        specs2_html = "\n".join([f"              <li>{s}</li>" for s in specs_list2])
        content = re.sub(r'<ul class="spec-list">.*?</ul>\s*<ul class="spec-list">.*?</ul>', f'<ul class="spec-list">\n{specs1_html}\n            </ul>\n            <ul class="spec-list">\n{specs2_html}\n            </ul>', content, flags=re.DOTALL)
        # Change section title
        content = re.sub(r'<h2 class="section-title" style="font-size: 1.8rem;">Spesifikasi Lengkap</h2>', '<h2 class="section-title" style="font-size: 1.8rem;">Detail / Informasi</h2>', content)
    else:
        content = re.sub(r'<!-- Specifications -->.*?</section>', '', content, flags=re.DOTALL)

    # Replace WhatsApp Link
    whatsapp_text = title.replace(" ", "%20")
    content = re.sub(r'https://wa.me/6281234567890\?text=[^"]+', f'https://wa.me/6281234567890?text=Halo%20Ichibot%2C%20saya%20ingin%20info%20mengenai%20{whatsapp_text}', content)
    content = re.sub(r'<i class="fa-brands fa-whatsapp"></i> Pesan Sekarang', f'<i class="fa-brands fa-whatsapp"></i> {btn_text}', content)

    # Replace Back Link
    if "pelatihan" in filename:
        content = content.replace('href="products.html" class="text-secondary"', 'href="pelatihan.html" class="text-secondary"')
        content = content.replace('Kembali ke Produk', 'Kembali ke Pelatihan')
    elif "achievement" in filename:
        content = content.replace('href="products.html" class="text-secondary"', 'href="achievements.html" class="text-secondary"')
        content = content.replace('Kembali ke Produk', 'Kembali ke Pencapaian')
    elif "event" in filename:
        content = content.replace('href="products.html" class="text-secondary"', 'href="events.html" class="text-secondary"')
        content = content.replace('Kembali ke Produk', 'Kembali ke Kalender Events')
    
    # Hide Tokopedia/Shopee buttons
    content = re.sub(r'<a href="#" class="btn btn-ghost btn-lg" title="Beli di Tokopedia">.*?</a>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a href="#" class="btn btn-ghost btn-lg" title="Beli di Shopee">.*?</a>', '', content, flags=re.DOTALL)
    
    with open(f"{base_dir}/{filename}", "w") as f:
        f.write(content)

# Pelatihan
create_page(
    "pelatihan-basic.html", "Pelatihan Line Follower Dasar", "Pelatihan+LF+Dasar",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Pelatihan Dasar</span>',
    '<span class="detail-price">Rp 1.000.000</span> <span class="detail-price-coret" style="text-decoration:none;">(Di Ichibot)</span> / <span class="detail-price">Rp 1.500.000</span> <span class="detail-price-coret" style="text-decoration:none;">(In-House)</span>',
    "Program pelatihan dasar yang dirancang untuk pemula. Ini adalah workshop satu hari penuh dengan maksimal dua tim yang dipandu oleh tentor expert dari Ichibot.",
    ["Pengenalan robot line follower", "Interpretasi sensor optik", "Dasar pemrograman Arduino"],
    ["Kalibrasi parameter dasar", "Praktik langsung di track sederhana", "Robot disediakan selama sesi"]
    , "Daftar Pelatihan"
)

create_page(
    "pelatihan-competition.html", "Pelatihan Line Follower Perlombaan", "Pelatihan+LF+Perlombaan",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Pelatihan Intensif</span>',
    '<span class="detail-price">Rp 1.500.000</span> <span class="detail-price-coret" style="text-decoration:none;">(Di Ichibot)</span> / <span class="detail-price">Rp 2.000.000</span> <span class="detail-price-coret" style="text-decoration:none;">(In-House)</span>',
    "Pelatihan intensif yang lebih mendalam dengan fokus pada teknik-teknik advanced seperti tuning PID, analisis track perlombaan, strategi navigasi di persimpangan dan tikungan tajam.",
    ["Tuning PID Advanced", "Analisis track perlombaan", "Strategi navigasi persimpangan"],
    ["Tikungan tajam", "Simulasi kondisi lomba sesungguhnya", "Mempersiapkan tim meraih podium"]
    , "Daftar Pelatihan"
)

create_page(
    "pelatihan-myrio.html", "Pelatihan MyRIO 1900 Pengoperasian", "Pelatihan+MyRIO",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Pelatihan Premium</span>',
    '<span class="detail-price">Rp 4.000.000</span>',
    "Pelatihan premium selama 2 hari untuk mahasiswa, dosen, dan teknisi yang ingin menguasai platform NI myRIO 1900. Spesifik untuk kompetisi KS/KRCI dengan durasi 2 hari penuh, maksimal 3 peserta.",
    ["Pengenalan LabVIEW", "Konfigurasi hardware", "Pemrograman gerakan dasar"],
    ["Manajemen objek", "Path planning untuk navigasi otomatis", "Sertifikat dan Konsumsi"]
    , "Daftar Pelatihan"
)

# Achievements
create_page(
    "achievement-ub.html", "Juara 1 Tingkat Nasional Universitas Brawijaya", "Juara+1+UB",
    '<span class="badge badge-red" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Kemenangan Lomba &middot; Okt 2025</span>',
    '',
    "Tim komunitas Ichibot meraih Juara 1 tingkat nasional di Universitas Brawijaya pada Oktober 2025 dalam kompetisi Line Follower, mengalahkan lebih dari 120 tim dari seluruh Indonesia dengan menggunakan robot Ultimate 5 Max.",
    [], [], "Bagikan / Tanya"
)

create_page(
    "achievement-export-germany.html", "Ultimate 5 Max Tembus Pasar Jerman", "Ekspor+ke+Jerman",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Ekspor &middot; Sep 2025</span>',
    '',
    "Ekspor pertama ke Jerman pada September 2025 dengan pengiriman 20 unit Ultimate 5 Max ke universitas teknik. Universitas tersebut memilih Ichibot karena performa sensor dan ketahanan yang lebih baik dibanding brand Eropa dengan harga jauh lebih murah.",
    [], [], "Bagikan / Tanya"
)

create_page(
    "achievement-meetup.html", "Kopdar Nasional 500+ Pengguna di Yogyakarta", "Kopdar+Nasional",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Komunitas &middot; Agu 2025</span>',
    '',
    "Di Yogyakarta pada Agustus 2025, lebih dari 500 pengguna Ichibot dari seluruh Indonesia berkumpul untuk berbagi pengalaman tentang setting PID dan tuning, sekaligus melihat preview produk terbaru yang akan diluncurkan akhir tahun.",
    [], [], "Bagikan / Tanya"
)

create_page(
    "achievement-japan.html", "Robot Sumo 1 Kg Terjual ke Jepang", "Ekspor+Jepang",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Ekspor &middot; Jul 2025</span>',
    '',
    "Pada Juli 2025, robot Sumo 1 Kg berhasil masuk pasar Jepang dengan pengiriman batch pertama 15 unit ke klub-klub sumo robotik di Tokyo dan Osaka — pencapaian bersejarah karena komunitas sumo robot Jepang yang sangat selektif akhirnya mengakui kualitas robot buatan Indonesia.",
    [], [], "Bagikan / Tanya"
)

create_page(
    "achievement-10years.html", "Perayaan 10 Tahun Ichibot Robotics", "10+Tahun+Ichibot",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Milestone &middot; Jun 2025</span>',
    '',
    "Ichibot merayakan 10 tahun perjalanannya pada Juni 2025, berkembang dari lab kecil di Yogyakarta menjadi perusahaan dengan ribuan pengguna di berbagai negara, menampilkan evolusi produk dan mengumumkan roadmap hingga 2027.",
    [], [], "Bagikan / Tanya"
)

create_page(
    "achievement-utm.html", "Juara Umum Line Follower UTM Malaysia", "Juara+Malaysia",
    '<span class="badge badge-red" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Kemenangan Lomba &middot; Mei 2025</span>',
    '',
    "Di Mei 2025, tim meraih juara umum di kompetisi Line Follower UTM Malaysia. Membawa pulang piala Juara Umum Internasional. Kombinasi Ultimate 5 Max dan strategi tuning PID yang sangat presisi menjadi kuncinya.",
    [], [], "Bagikan / Tanya"
)

# Events
create_page(
    "event-its.html", "Line Follower Contest — ITS Surabaya", "Event+ITS",
    '<span class="badge badge-red" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Kompetisi &middot; 14 Jun 2026</span>',
    '',
    "Kompetisi line follower tingkat nasional di Institut Teknologi Sepuluh Nopember (ITS) Surabaya. Siapkan tim dan robot terbaik Anda untuk bertanding di lintasan ekstrem.",
    ["Tanggal: 14 Juni 2026", "Lokasi: Institut Teknologi Sepuluh Nopember, Surabaya"],
    ["Kategori: Line Follower", "Pendaftaran: Dibuka segera"], "Daftar Kompetisi"
)

create_page(
    "event-workshop-pid.html", "Workshop Tuning PID — Ichibot Yogyakarta", "Workshop+PID",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Workshop &middot; 22 Jun 2026</span>',
    '',
    "Workshop eksklusif mempelajari cara tuning PID untuk line follower dan robot sumo secara langsung dari expert Ichibot.",
    ["Tanggal: 22 Juni 2026", "Lokasi: Workshop Ichibot, Sleman, Yogyakarta"],
    ["Kategori: Pelatihan", "Peserta Terbatas: Maks 20 orang"], "Daftar Workshop"
)

create_page(
    "event-ub.html", "Robot Contest Nasional — Universitas Brawijaya", "Event+UB",
    '<span class="badge badge-red" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Kompetisi &middot; 05 Jul 2026</span>',
    '',
    "Ajang kompetisi robot nasional bergengsi di Universitas Brawijaya dengan berbagai kategori perlombaan termasuk Line Follower dan Sumo.",
    ["Tanggal: 05 Juli 2026", "Lokasi: Universitas Brawijaya, Malang"],
    ["Kategori: Berbagai Kategori", "Pendaftaran: Hubungi panitia lokal"], "Daftar Kompetisi"
)

print("Rest generated")
