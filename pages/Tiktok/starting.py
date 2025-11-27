import json
import time
import random

def random_delay():
    min_delay = 50 * 60        # 3000 detik
    max_delay = 70 * 60        # 4200 detik
    delay = round(random.uniform(min_delay, max_delay), 3)

    print(f"Delay: {delay} detik ({delay/60:.2f} menit)")
    time.sleep(delay)

def load_database():
    try:
        with open('database.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"[ERROR] Gagal membuka database.json -> {e}")
        time.sleep(5)
        return None

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

# Load progress
progress = load_progress()
last_index = progress["last_index"]
putaran = progress["putaran"]

print(f"🔄 Melanjutkan dari video index ke: {last_index}")
print(f"🔁 Putaran terakhir: {putaran}")

while True:
    data = load_database()

    if data is None:
        continue

    if "videos" not in data:
        print("[ERROR] Key 'videos' tidak ditemukan di database.json")
        time.sleep(5)
        continue

    videos = data["videos"]
    total_video = len(videos)

    print(f"\n==========================")
    print(f"   PUTARAN KE : {putaran}")
    print(f"==========================\n")

    # Mulai dari index terakhir, bukan dari 0
    for index in range(last_index, total_video):
        try:
            video = videos[index]

            judul = video.get('judul_video', 'Tidak ada judul')
            id_produk = video.get('id_produk', 'Tidak ada ID produk')

            print(f"[{index+1}/{total_video}] {judul} : {id_produk}")

            import main as au
            au.main(judul, id_produk)

            # Simpan progress setelah sukses
            save_progress(index + 1, putaran)

            random_delay()

        except Exception as e:
            print(f"[ERROR] Terjadi masalah saat memproses video -> {e}")
            time.sleep(3)

    # Reset index setelah 1 putaran selesai
    print(f"\nSelesai putaran {putaran}, mengulang lagi dari awal...\n")
    putaran += 1
    last_index = 0  # kembali ke video pertama
    save_progress(last_index, putaran)
    time.sleep(2)
