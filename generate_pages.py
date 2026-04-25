import os
import re

base_dir = "/Users/ichibot/web ichibot 2"

with open(f"{base_dir}/product-detail.html", "r") as f:
    template = f.read()

def create_product_page(filename, title, image_text, badge, price_html, desc, specs_list1, specs_list2):
    content = template.replace("Ultimate 5 Max — Ichibot Robotics", f"{title} — Ichibot Robotics")
    content = content.replace("Ultimate 5 Max adalah robot line follower dengan spesifikasi tertinggi dari Ichibot.", f"{title} adalah produk unggulan dari Ichibot Robotics.")
    
    # Hero section
    # Replace Image
    content = re.sub(r'<img src="https://placehold.co/[^"]+" alt="[^"]+">', 
                     f'<img src="https://placehold.co/800x800/111111/444444?text={image_text}" alt="{title}">', content)
    
    # Replace Badges
    content = re.sub(r'<span class="badge badge-red"[^>]*>.*?</span>', badge, content)
    
    # Replace Title
    content = re.sub(r'<h1 class="detail-title">.*?</h1>', f'<h1 class="detail-title">{title}</h1>', content)
    
    # Replace Price
    content = re.sub(r'<div class="detail-price-wrap">.*?</div>', f'<div class="detail-price-wrap">\n{price_html}\n            </div>', content, flags=re.DOTALL)
    
    # Replace Description
    content = re.sub(r'<p class="detail-desc-text">.*?</p>\s*<p class="detail-desc-text" style="margin-bottom: 0;">.*?</p>', f'<p class="detail-desc-text">\n                {desc}\n              </p>', content, flags=re.DOTALL)
    
    # Replace Specs
    specs1_html = "\n".join([f"              <li>{s}</li>" for s in specs_list1])
    specs2_html = "\n".join([f"              <li>{s}</li>" for s in specs_list2])
    content = re.sub(r'<ul class="spec-list">.*?</ul>\s*<ul class="spec-list">.*?</ul>', f'<ul class="spec-list">\n{specs1_html}\n            </ul>\n            <ul class="spec-list">\n{specs2_html}\n            </ul>', content, flags=re.DOTALL)
    
    # Replace WhatsApp Link
    whatsapp_text = title.replace(" ", "%20")
    content = re.sub(r'https://wa.me/6281234567890\?text=[^"]+', f'https://wa.me/6281234567890?text=Halo%20Ichibot%2C%20saya%20ingin%20memesan%20{whatsapp_text}', content)
    
    with open(f"{base_dir}/{filename}", "w") as f:
        f.write(content)

# 1. Ichiduino Basic+
create_product_page(
    "product-ichiduino-basic-plus.html",
    "Ichiduino Basic+",
    "Ichiduino+Basic+",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Line Follower</span>',
    '<span class="detail-price">Rp 585.000</span> <span class="detail-price-coret" style="text-decoration:none;">(Belum Dirakit)</span> / <span class="detail-price">Rp 780.000</span> <span class="detail-price-coret" style="text-decoration:none;">(Dirakit)</span>',
    "Ichiduino Basic+ adalah robot line follower edukasi yang sangat cocok untuk pemula yang ingin belajar robotika dasar. Menggunakan Arduino Nano Atmega328P, robot ini sangat mudah diprogram menggunakan Arduino IDE.",
    ["Arduino Nano Atmega328P", "8 Optic Line Sensor", "OLED 0.96\"", "2x 18650 Battery"],
    ["Tersedia dalam bentuk DIY Kit", "Atau pilih opsi sudah dirakit", "Cocok untuk belajar dasar robotika", "Mudah diprogram"]
)

# 2. Ichiduino Pro
create_product_page(
    "product-ichiduino-pro.html",
    "Ichiduino Pro",
    "Ichiduino+Pro",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Line Follower</span>',
    '<span class="detail-price">Rp 1.949.025</span> <span class="detail-price-coret">Rp 1.999.000</span>',
    "Ichiduino Pro adalah upgrade dari versi Basic dengan mikrokontroler yang jauh lebih kuat, Atmega 2560. Dengan tambahan 12 sensor garis optik dan baterai Lipo 2s 400mAh, robot ini siap untuk lintasan yang lebih rumit.",
    ["Atmega 2560", "12 Optic Line Sensor", "OLED 0.96\"", "Lipo 2s 400mAh berkapasitas tinggi"],
    ["Magnetic charger", "Kompatibilitas dengan mBlock", "Kompatibilitas dengan Arduino IDE", "Sangat presisi di persimpangan"]
)

# 3. Sumo 500g
create_product_page(
    "product-sumo-500g.html",
    "Sumo 500g",
    "Sumo+500g",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Sumo</span>',
    '<span class="detail-price">Rp 1.755.000</span> <span class="detail-price-coret">Rp 1.800.000</span>',
    "Sumo 500g adalah robot sumo kelas ringan yang ditenagai oleh ESP32. Dilengkapi dengan WiFi dan Bluetooth, motor 16mm dengan kecepatan 500RPM, serta roda silikon yang memberikan cengkeraman maksimal di arena dohyo.",
    ["ESP32", "WiFi dan Bluetooth", "Baterai 3s 1000mAh Lipo", "Motor DC 16mm 500RPM"],
    ["Pisau tajam / Sharp Blade", "Silicone Wheel yang lengket di arena", "Respon sensor sangat cepat", "Desain yang aerodinamis"]
)

# 4. Sumo 1 Kg
create_product_page(
    "product-sumo-1kg.html",
    "Sumo 1 Kg",
    "Sumo+1+Kg",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Sumo</span>',
    '<span class="detail-price">Rp 2.340.000</span> <span class="detail-price-coret">Rp 2.400.000</span>',
    "Sumo 1 Kg adalah robot kelas menengah dengan kekuatan dorong yang luar biasa. Menggunakan motor 25mm yang lebih besar dan baterai 3s 1200mAh, robot ini dapat menghasilkan stall torque hingga 30kg.cm.",
    ["ESP32", "WiFi dan Bluetooth", "Baterai 3s 1200mAh Lipo", "Motor DC 25mm 500RPM"],
    ["Torsi stall mencapai 30kg.cm", "Pisau tajam untuk masuk ke bawah lawan", "Konstruksi sangat kokoh", "Siap kompetisi"]
)

# 5. Transporter Mecanum
create_product_page(
    "product-transporter-mecanum.html",
    "Transporter Mecanum",
    "Transporter+Mecanum",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Transporter</span>',
    '<span class="detail-price">Rp 3.022.500</span> <span class="detail-price-coret">Rp 3.100.000</span>',
    "Transporter Mecanum dilengkapi dengan roda mecanum 60mm untuk manuver omnidirectional. Memiliki sistem manipulator berupa gripper, elbow, dan lifter yang dapat dikendalikan menggunakan PS3 Remote.",
    ["ESP32 dengan konektivitas WiFi + BT", "Roda Mecanum 60mm", "Kendali PS3 Remote", "Manipulator Gripper"],
    ["Sistem Lifter axis", "Sistem Elbow", "Manuver omnidirectional yang lincah", "Ideal untuk kompetisi transporter"]
)

# 6. Transporter Ultimate Omni
create_product_page(
    "product-transporter-omni.html",
    "Transporter Ultimate Omni",
    "Transporter+Ultimate+Omni",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Transporter</span>',
    '<span class="detail-price">Rp 3.510.000</span> <span class="detail-price-coret">Rp 3.600.000</span>',
    "Versi Ultimate dari robot Transporter ini menggunakan roda omni 58mm untuk pergerakan ke segala arah tanpa perlu memutar badan. Memiliki baterai Lipo 1200mAh yang lebih besar dan sistem manipulator tiga sumbu.",
    ["ESP32", "WiFi dan Bluetooth", "Roda Omni 58mm", "Baterai 3s 1200mAh Lipo"],
    ["Kendali PS3 Remote", "Gripper", "Elbow", "Lifter axis"]
)

# 7. Sumo 2 Kg
create_product_page(
    "product-sumo-2kg.html",
    "Sumo 2 Kg",
    "Sumo+2+Kg",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Sumo</span>',
    '<span class="detail-price">Rp 3.315.000</span> <span class="detail-price-coret">Rp 3.400.000</span>',
    "Sumo 2 Kg adalah mesin pendorong yang tak terhentikan di arena. Dengan torsi stall mencapai 65kg.cm berkat motor 37mm 300RPM, robot ini siap menyingkirkan lawan apa pun di kelas 2 kilogram.",
    ["ESP32", "WiFi dan Bluetooth", "Baterai 3s 2000mAh Lipo yang besar", "Motor DC 37mm 300RPM"],
    ["Torsi stall luar biasa 65kg.cm", "Bilah baja tajam yang kokoh", "Roda silikon dengan grip maksimal", "Bobot optimal mendekati 2kg"]
)

# 8. Transporter Mecanum Pro
create_product_page(
    "product-transporter-mecanum-pro.html",
    "Transporter Mecanum Pro",
    "Transporter+Mecanum+Pro",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">Transporter</span>',
    '<span class="detail-price">Rp 4.095.000</span> <span class="detail-price-coret">Rp 4.200.000</span>',
    "Transporter Mecanum Pro adalah kelas flagship dari lini transporter kami. Menggunakan roda mecanum besar 80mm dan memiliki sumbu manipulator ekstra berupa rotator untuk fleksibilitas manipulasi objek.",
    ["ESP32", "WiFi dan Bluetooth", "Roda Mecanum 80mm", "Kendali PS3 Remote"],
    ["Baterai 3s 1500mAh Lipo", "Sistem Gripper + Elbow", "Sistem Lifter", "Sistem Rotator tambahan"]
)

# 9. myRIO 1900
create_product_page(
    "product-myrio-1900.html",
    "Mobile Robot Omnidirectional myRIO 1900",
    "myRIO+1900+Mobile+Robot",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">MyRIO</span>',
    '<span class="detail-price">Rp 75.000.000</span>',
    "Platform robot edukasi level institusional yang menggunakan NI myRIO 1900. Dilengkapi 7 sensor jarak ultrasonik, kamera HD Logitech, dan pergerakan omnidirectional. Sempurna untuk riset dan kompetisi robot cerdas.",
    ["National Instruments myRIO 1900", "7 Sensor Jarak (Ultrasonik/Inframerah)", "2 Sensor Line", "Kamera HD Logitech"],
    ["Roda Omnidirectional", "Akses Gripper dan Lifter Axis", "Termasuk lisensi software LabVIEW", "Dukungan purna jual 1 tahun"]
)

# 10. myRIO 1950
create_product_page(
    "product-myrio-1950.html",
    "Mobile Robot Mecanum myRIO 1950",
    "myRIO+1950+Mecanum",
    '<span class="badge badge-white" style="position: absolute; top: 16px; left: 16px; z-index: 2;">MyRIO</span>',
    '<span class="detail-price">Rp 82.000.000</span>',
    "Versi upgrade dari platform myRIO dengan modul NI myRIO 1950 berkinerja tinggi. Roda mecanum 80mm memberikan mobilitas tingkat tinggi. Dilengkapi juga dengan gyroscope untuk navigasi yang lebih presisi.",
    ["National Instruments myRIO 1950 dengan FPGA ditingkatkan", "Roda Mecanum 80mm", "7 Sensor Jarak", "Sensor Gyroscope presisi"],
    ["Kamera HD Logitech", "Lifter dan Gripper", "Termasuk lisensi software LabVIEW", "Cocok untuk kompetisi level tinggi"]
)

print("Product pages generated.")
