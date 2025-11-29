import json
import time
import random
import os
from pathlib import Path

# ===== KONFIGURASI =====
MASTER_PATH = r"D:\Master\pages\Tiktok\vidio"  # Raw string sudah benar
PRODUK_YANG_AKAN_DIUPLOAD = ["Baofeng UV-5R Dual Band,1731284724415825654"]  # Format: "Nama Barang,ID_Produk"
MODE_ACAK = 0  # 0=Produk lengkap dulu, 1=Round Robin per video, 2=Produk sebagian lalu lanjut
# =======================

def random_delay():
    min_delay = 50 * 60        # 3000 detik
    max_delay = 70 * 60        # 4200 detik
    delay = round(random.uniform(min_delay, max_delay), 3)

    print(f"Delay: {delay} detik ({delay/60:.2f} menit)")
    time.sleep(delay)

def load_progress():
    """Load progress terakhir"""
    try:
        with open("progress.json", "r") as f:
            return json.load(f)
    except:
        return {"last_index": 0, "putaran": 1}

def save_progress(last_index, putaran):
    """Simpan progress ke file"""
    with open("progress.json", "w") as f:
        json.dump({"last_index": last_index, "putaran": putaran}, f, indent=4)

def parse_folder_name(folder_name):
    """Parse nama folder untuk mendapatkan nama_barang dan id_produk"""
    # Split berdasarkan koma
    if ',' in folder_name:
        parts = folder_name.split(',', 1)  # Split hanya pada koma pertama
        nama_barang = parts[0].strip()
        id_produk = parts[1].strip()
        
        # Validasi ID produk harus angka
        if not id_produk.isdigit():
            print(f"[WARNING] ID produk bukan angka: {id_produk}")
            id_produk = "000000"
    else:
        # Jika tidak ada koma, gunakan seluruh string sebagai nama barang
        nama_barang = folder_name
        id_produk = "000000"
        print(f"[WARNING] Format folder tidak valid (tidak ada koma): {folder_name}")
    
    return nama_barang, id_produk

def scan_videos_from_folders():
    """Scan semua video dari folder produk yang dikonfigurasi"""
    produk_videos = {}
    
    for produk_folder in PRODUK_YANG_AKAN_DIUPLOAD:
        # Gunakan os.path.join untuk handle path dengan benar
        produk_path = os.path.join(MASTER_PATH, produk_folder)
        produk_path = Path(produk_path)
        
        if not produk_path.exists():
            print(f"[WARNING] Folder produk '{produk_folder}' tidak ditemukan di {produk_path}")
            continue
        
        # Parse nama folder untuk mendapatkan nama_barang dan id_produk
        nama_barang, id_produk = parse_folder_name(produk_folder)
        print(f"[INFO] Folder: '{produk_folder}' -> Nama: '{nama_barang}', ID: '{id_produk}'")
        print(f"[INFO] Mencari video di: {produk_path}")
            
        # Cari semua file video
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(produk_path.glob(f"*{ext}"))
            video_files.extend(produk_path.glob(f"*{ext.upper()}"))
        
        # Urutkan video secara alfanumerik
        video_files.sort()
        
        produk_videos[produk_folder] = {
            'nama_barang': nama_barang,
            'id_produk': id_produk,
            'videos': []
        }
        
        for video_file in video_files:
            produk_videos[produk_folder]['videos'].append({
                'judul_video': video_file.stem,
                'id_produk': id_produk,
                'nama_barang': nama_barang,
                'video_path': str(video_file)
            })
    
    total_videos = sum(len(data['videos']) for data in produk_videos.values())
    print(f"[INFO] Ditemukan {total_videos} video dari {len(produk_videos)} produk")
    return produk_videos

def generate_upload_sequence(produk_videos, mode_acak):
    """Generate urutan upload berdasarkan mode acak"""
    sequence = []
    
    if mode_acak == 0:
        # MODE 0: Upload semua video produk 1 dulu, lalu produk 2, lalu produk 3
        for produk_folder in PRODUK_YANG_AKAN_DIUPLOAD:
            if produk_folder in produk_videos:
                sequence.extend(produk_videos[produk_folder]['videos'])
    
    elif mode_acak == 1:
        # MODE 1: Round Robin - video 1 semua produk, lalu video 2 semua produk, dst
        # Cari jumlah maksimum video per produk
        max_videos = max(len(data['videos']) for data in produk_videos.values())
        
        for video_index in range(max_videos):
            for produk_folder in PRODUK_YANG_AKAN_DIUPLOAD:
                if (produk_folder in produk_videos and 
                    video_index < len(produk_videos[produk_folder]['videos'])):
                    sequence.append(produk_videos[produk_folder]['videos'][video_index])
    
    elif mode_acak == 2:
        # MODE 2: Upload video 1 & 2 semua produk dulu, lalu video 3 & 4 semua produk
        # Cari jumlah maksimum video per produk
        max_videos = max(len(data['videos']) for data in produk_videos.values())
        
        # Group video per 2 (bisa diubah sesuai kebutuhan)
        group_size = 2
        
        for group_start in range(0, max_videos, group_size):
            for produk_folder in PRODUK_YANG_AKAN_DIUPLOAD:
                if produk_folder in produk_videos:
                    videos = produk_videos[produk_folder]['videos']
                    # Ambil video dalam group saat ini
                    for video_index in range(group_start, min(group_start + group_size, len(videos))):
                        sequence.append(videos[video_index])
    
    else:
        print(f"[WARNING] Mode acak {mode_acak} tidak valid, menggunakan mode 0")
        for produk_folder in PRODUK_YANG_AKAN_DIUPLOAD:
            if produk_folder in produk_videos:
                sequence.extend(produk_videos[produk_folder]['videos'])
    
    return sequence

# Load progress
progress = load_progress()
last_index = progress["last_index"]
putaran = progress["putaran"]

print(f"🔄 Melanjutkan dari video index ke: {last_index}")
print(f"🔁 Putaran terakhir: {putaran}")
print(f"🎯 Mode Acak: {MODE_ACAK}")
print(f"📦 Produk yang akan diupload: {', '.join(PRODUK_YANG_AKAN_DIUPLOAD)}")
print(f"📁 Master Path: {MASTER_PATH}")

while True:
    # Scan video dari folder
    produk_videos = scan_videos_from_folders()
    
    if not produk_videos:
        print("[ERROR] Tidak ada video yang ditemukan!")
        time.sleep(5)
        continue

    # Generate urutan upload berdasarkan mode acak
    upload_sequence = generate_upload_sequence(produk_videos, MODE_ACAK)
    
    print(f"\n==========================")
    print(f"   PUTARAN KE : {putaran}")
    print(f"   MODE ACAK  : {MODE_ACAK}")
    print(f"   TOTAL VIDEO: {len(upload_sequence)}")
    print(f"==========================\n")

    # Tampilkan urutan upload
    print("📋 Urutan Upload:")
    for i, video in enumerate(upload_sequence, 1):
        print(f"  {i}. {video['nama_barang']} - {video['judul_video']} (ID: {video['id_produk']})")
    print()

    # Mulai dari index terakhir
    for index in range(last_index, len(upload_sequence)):
        try:
            video = upload_sequence[index]
            judul = video.get('judul_video', 'Tidak ada judul')
            id_produk = video.get('id_produk', 'Tidak ada ID produk')
            nama_barang = video.get('nama_barang', 'Tidak ada nama barang')
            video_path = video.get('video_path', 'Tidak ada path')

            print(f"[{index+1}/{len(upload_sequence)}] {judul}")
            print(f"   📦 Produk: {nama_barang}")
            print(f"   🆔 ID: {id_produk}")
            print(f"   📁 Path: {video_path}")

            # Import dan jalankan main function dengan FULL PATH video
            import main as au
            au.main(video_path, id_produk, nama_barang)  # Kirim full path video

            # Simpan progress setelah sukses
            save_progress(index + 1, putaran)

            random_delay()

        except Exception as e:
            print(f"[ERROR] Terjadi masalah saat memproses video -> {e}")
            time.sleep(3)

    # Reset progress setelah 1 putaran selesai
    print(f"\n✅ Selesai putaran {putaran}, mengulang lagi dari awal...\n")
    putaran += 1
    last_index = 0  # kembali ke video pertama
    save_progress(last_index, putaran)
    
    print("🕐 Menunggu 2 detik sebelum putaran berikutnya...")
    time.sleep(2)