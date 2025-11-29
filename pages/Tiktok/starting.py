import json
import time
import random
import os
from pathlib import Path

# ===== KONFIGURASI =====
MASTER_PATH = r"D:\Master\pages\Tiktok\vidio"
PRODUK_YANG_AKAN_DIUPLOAD = ["Baofeng UV-5R Dual Band"]  # Sesuaikan dengan nama folder produk
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

def scan_videos_from_folders():
    """Scan semua video dari folder produk yang dikonfigurasi"""
    produk_videos = {}
    
    for produk in PRODUK_YANG_AKAN_DIUPLOAD:
        produk_path = Path(MASTER_PATH) / produk
        
        if not produk_path.exists():
            print(f"[WARNING] Folder produk '{produk}' tidak ditemukan di {produk_path}")
            continue
            
        # Cari semua file video
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(produk_path.glob(f"*{ext}"))
            video_files.extend(produk_path.glob(f"*{ext.upper()}"))
        
        # Urutkan video secara alfanumerik
        video_files.sort()
        
        produk_videos[produk] = []
        for video_file in video_files:
            produk_videos[produk].append({
                'judul_video': video_file.stem,
                'id_produk': produk,
                'video_path': str(video_file)
            })
    
    print(f"[INFO] Ditemukan {sum(len(videos) for videos in produk_videos.values())} video dari {len(produk_videos)} produk")
    return produk_videos

def generate_upload_sequence(produk_videos, mode_acak):
    """Generate urutan upload berdasarkan mode acak"""
    sequence = []
    
    if mode_acak == 0:
        # MODE 0: Upload semua video produk 1 dulu, lalu produk 2, lalu produk 3
        # Contoh: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4
        for produk in PRODUK_YANG_AKAN_DIUPLOAD:
            if produk in produk_videos:
                sequence.extend(produk_videos[produk])
    
    elif mode_acak == 1:
        # MODE 1: Round Robin - video 1 semua produk, lalu video 2 semua produk, dst
        # Contoh: 1.1, 2.1, 3.1, 1.2, 2.2, 3.2, 1.3, 2.3, 3.3, 1.4, 2.4, 3.4
        
        # Cari jumlah maksimum video per produk
        max_videos = max(len(videos) for videos in produk_videos.values())
        
        for video_index in range(max_videos):
            for produk in PRODUK_YANG_AKAN_DIUPLOAD:
                if produk in produk_videos and video_index < len(produk_videos[produk]):
                    sequence.append(produk_videos[produk][video_index])
    
    elif mode_acak == 2:
        # MODE 2: Upload video 1 & 2 semua produk dulu, lalu video 3 & 4 semua produk
        # Contoh: 1.1, 1.2, 2.1, 2.2, 3.1, 3.2, 1.3, 1.4, 2.3, 2.4, 3.3, 3.4
        
        # Cari jumlah maksimum video per produk
        max_videos = max(len(videos) for videos in produk_videos.values())
        
        # Group video per 2 (bisa diubah sesuai kebutuhan)
        group_size = 2
        
        for group_start in range(0, max_videos, group_size):
            for produk in PRODUK_YANG_AKAN_DIUPLOAD:
                if produk in produk_videos:
                    # Ambil video dalam group saat ini
                    for video_index in range(group_start, min(group_start + group_size, len(produk_videos[produk]))):
                        sequence.append(produk_videos[produk][video_index])
    
    else:
        print(f"[WARNING] Mode acak {mode_acak} tidak valid, menggunakan mode 0")
        for produk in PRODUK_YANG_AKAN_DIUPLOAD:
            if produk in produk_videos:
                sequence.extend(produk_videos[produk])
    
    return sequence

# Load progress
progress = load_progress()
last_index = progress["last_index"]
putaran = progress["putaran"]

print(f"🔄 Melanjutkan dari video index ke: {last_index}")
print(f"🔁 Putaran terakhir: {putaran}")
print(f"🎯 Mode Acak: {MODE_ACAK}")
print(f"📦 Produk yang akan diupload: {', '.join(PRODUK_YANG_AKAN_DIUPLOAD)}")

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
        print(f"  {i}. {video['id_produk']} - {video['judul_video']}")
    print()

    # Mulai dari index terakhir
    for index in range(last_index, len(upload_sequence)):
        try:
            video = upload_sequence[index]
            judul = video.get('judul_video', 'Tidak ada judul')
            id_produk = video.get('id_produk', 'Tidak ada ID produk')
            video_path = video.get('video_path', 'Tidak ada path')

            print(f"[{index+1}/{len(upload_sequence)}] {judul} : {id_produk}")
            print(f"   📁 Path: {video_path}")

            # Import dan jalankan main function
            import main as au
            au.main(judul, id_produk)

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