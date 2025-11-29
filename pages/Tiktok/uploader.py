import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

video_folder = "D:\\Master\\pages\\Tiktok\\vidio"

# VARIABLE GLOBAL DRIVER
driver = None

def discard_memory_draft():
    xpaths = [
        "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[2]/button[1]/div[2]",
        "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[2]/button[1]",
        "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[2]",
    ]

    for path in xpaths:
        elements = driver.find_elements(By.XPATH, path)
        if elements:
            elements[0].click()
            print('[+] TERDETEKSI ADA VIDIO YANG BELUM SELESAI')
            xpaths = [
                "/html/body/div[5]/div/div/div[3]/button[2]/div/div",
                "/html/body/div[5]/div/div/div[3]/button[2]/div",
                "/html/body/div[5]/div/div/div[3]/button[2]",
            ]

            for path in xpaths:
                elements = driver.find_elements(By.XPATH, path)
                if elements:
                    elements[0].click()
                    print('[+] SUKSES DI HAPUS!!!')

    #print('[+] Tidak ada yang perlu di discard')

# Fungsi untuk generate delay acak
def random_delay():
    return round(random.uniform(5.0, 15.0), 1)

def random_delay_upload():
    #return round(random.uniform(1500, 2100), 1) # 30 menit sampai 35 menit
    #return round(random.uniform(30.0, 60.0), 1) # 30 detik sampai 60 detik
    return round(random.uniform(1800, 3600), 1) # 30 detik sampai 60 detik

def uploadvidio(video_id):
    print(video_id)

    driver.get("https://www.tiktok.com/tiktokstudio/upload?from=creator_center")
    time.sleep(2)

    print(f"🔄 Mengupload video: {video_id}")

    time.sleep(random_delay())

    # Ambil input file asli
    input_file = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@type="file" and @accept="video/*"]')
        )
    )

    # Upload menggunakan send_keys
    input_file.send_keys(video_id)

    # Trigger event onchange (WAJIB PADA UI TIKTOK TERBARU)
    driver.execute_script(
        "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
        input_file
    )

    print(f"📤 Menunggu proses upload TikTok...")

    # Tunggu sampai thumbnail muncul (berarti benar-benar keupload)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.XPATH, '//img[contains(@src,"tiktok")]')
        )
    )

    print(f"✅ Video benar-benar sudah terupload: {video_id}")

    time.sleep(random_delay())

def deskripsiedit(nama_produk):

    nama_produk = 'HT Baofeng UV-82'
    def generate_descriptions(nama_produk, jumlah_hashtag=4):
        semua_hashtag = [
            '#baofeng', '#baofengoriginal', '#htbaofeng', '#htmurah',
            '#radiokomunikasi', '#handytransceiver', '#htuv5r', '#radioht', '#htoutdoor',
            '#komunikasidarat', '#komunikasisecurity', '#radiokomunitas', '#frep', '#orari',
            '#hamradio', '#radiosurvival', '#radioscurity', '#komunitasradio', '#radiopemula',
            '#radiocamping', '#survivalgear', '#preppergear', '#alatoutdoor', '#alatsecurity',
            '#htbagus', '#htrecommended', '#jualht', '#httermurah', '#radiowalkietalkie'
        ]
        
        tagtrending = ' ' + ' '.join(random.sample(semua_hashtag, min(jumlah_hashtag, len(semua_hashtag))))

        templates = [
            f"🔥 Temukan keunggulan {nama_produk.strip()} yang bikin komunikasi makin lancar & profesional! Jangan sampai kehabisan!#baofengUV-82 {tagtrending}",
            f"💡 Butuh HT powerful? {nama_produk.strip()} jawabannya! Dual band, suara jernih, baterai tahan lama!#baofengUV-82 {tagtrending}",
            f"✨ Ingin komunikasi lebih stabil? {nama_produk.strip()} siap bantu kamu tetap terhubung di segala situasi! Grab it now!#baofengUV-82 {tagtrending}",
            f"😱 Wajib punya! {nama_produk.strip()} bikin komunikasi jarak jauh makin mudah dan aman! Yuk buruan beli!#baofengUV-82 {tagtrending}",
            f"💖 Simpel, kuat, dan tahan lama! {nama_produk.strip()} memang juara di kelasnya! Klik beli sekarang!#baofengUV-82 {tagtrending}",
            f"🔥 Sudah coba {nama_produk.strip()}? Kalau belum, kamu ketinggalan banget! Daya 5W, baterai 2800mAh!#baofengUV-82 {tagtrending}",
            f"💡 Solusi cerdas untuk kerja lapangan! {nama_produk.strip()} bikin komunikasi tim lebih efektif. Dapatkan segera!#baofengUV-82 {tagtrending}",
            f"✨ Rahasia komunikasi stabil ada di {nama_produk.strip()}! Dual band VHF/UHF yang super fleksibel!#baofengUV-82 {tagtrending}",
            f"🔥 Banyak yang sudah pakai {nama_produk.strip()}! Sekarang giliran kamu. Yuk, beli sekarang!#baofengUV-82 {tagtrending}",
            f"💡 Inovasi terbaik buat komunikasi lapangan! {nama_produk.strip()} bikin kerja makin gampang!#baofengUV-82 {tagtrending}",
            f"🔥 Sudah banyak yang order {nama_produk.strip()}! Kamu kapan? Jangan sampai kehabisan!#baofengUV-82 {tagtrending}",
            f"✨ HT andalan yang wajib kamu punya! {nama_produk.strip()} bikin komunikasi makin stabil dan jelas!#baofengUV-82 {tagtrending}",
            f"🔥 Gunakan {nama_produk.strip()} dan rasakan sinyal kuatnya! Beli sekarang juga sebelum habis!#baofengUV-82 {tagtrending}",
            f"🚀 Upgrade komunikasi tim kamu dengan {nama_produk.strip()}! Dual PTT, jangkauan lebih jauh!#baofengUV-82 {tagtrending}",
            f"💎 Barang berkualitas dengan harga terbaik! {nama_produk.strip()} bikin komunikasi makin mudah & aman!#baofengUV-82 {tagtrending}",
            f"🔥 Jangan lewatkan kesempatan punya {nama_produk.strip()}! Stok terbatas, buruan beli!#baofengUV-82 {tagtrending}",
            f"✨ Dengan {nama_produk.strip()}, komunikasi jadi lebih praktis, stabil, dan profesional!#baofengUV-82 {tagtrending}",
            f"💡 Cari HT berkualitas? {nama_produk.strip()} solusinya! Cek sekarang juga.#baofengUV-82 {tagtrending}",
            f"🔥 Dapatkan performa maksimal dengan {nama_produk.strip()}! Hanya di sini harga termurah!#baofengUV-82 {tagtrending}",
            f"💎 Produk eksklusif yang bikin komunikasi lebih simpel! {nama_produk.strip()} siap menemani kegiatanmu!#baofengUV-82 {tagtrending}",
            f"✨ Nggak perlu bingung lagi! {nama_produk.strip()} bikin komunikasi makin mudah & nyaman!#baofengUV-82 {tagtrending}",
            f"🔥 Udah banyak yang order {nama_produk.strip()}! Yuk jadi yang selanjutnya!#baofengUV-82 {tagtrending}",
            f"💖 Kamu pasti suka dengan {nama_produk.strip()}! Beli sekarang sebelum kehabisan!#baofengUV-82 {tagtrending}",
            f"🚀 Saatnya upgrade ke {nama_produk.strip()}! Kualitas terbaik, jangkauan lebih jauh!#baofengUV-82 {tagtrending}",
            f"✨ Tampil profesional dengan {nama_produk.strip()}! Buruan checkout sebelum kehabisan!#baofengUV-82 {tagtrending}"
        ]

        return random.choice(templates)

    # Contoh penggunaan
    deskripsi = generate_descriptions(nama_produk)

    # HAPUS global driver dari sini

    # Fungsi untuk memfilter hanya karakter dalam BMP (Basic Multilingual Plane)
    def filter_bmp(text):
        return ''.join(c for c in text if ord(c) <= 0xFFFF)

    # Filter deskripsi untuk menghilangkan karakter non-BMP
    deskirpsi_bersih = filter_bmp(deskripsi)

    # Temukan elemen deskripsi
    desc_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='combobox']"))
    )

    # Klik untuk fokus
    desc_box.click()
    time.sleep(1)

    # Hapus isi lama (tekan Ctrl+A lalu Delete)
    desc_box.send_keys(Keys.CONTROL, 'a')
    time.sleep(0.1)
    desc_box.send_keys(Keys.DELETE)
    time.sleep(1)

    # Ketik manual huruf demi huruf
    for char in deskirpsi_bersih:
        desc_box.send_keys(char)
        time.sleep(0.05)  # jeda antar huruf biar natural

    # ENTER untuk trigger perubahan
    desc_box.send_keys(Keys.ENTER)
    time.sleep(1)

    # Klik di luar untuk "simulasi" kehilangan fokus
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(3)

def inputproduk(namaproduk):

    if namaproduk == 'ss':
        try:
            with open('upload_propat.txt', 'r') as file:
                nomor = 1
                lines = file.readlines()  # Membaca seluruh isi file sekaligus

                for line in lines:  # Iterasi melalui setiap baris
                    try:
                        xpath = line.strip()
                        print(f'Line {nomor}: {xpath}')

                        while True:
                            try:
                                eksekusi = xpath.split(',')
                                xpath = eksekusi[0]
                                perintah = str(eksekusi[1])

                                if perintah == 'click':
                                    tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                                    tombol.click()
                                    print(f'Berhasil klik pada line {nomor}')
                                    time.sleep(2)
                                elif perintah == 'sendkeys':
                                    konten = eksekusi[2]
                                    tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                                    print(f'Berhasil mengirim teks pada line {nomor}')
                                    tombol.click()
                                    tombol.send_keys(konten)
                                    time.sleep(2)
                            except Exception as e:
                                print(f'Gagal pada line {nomor}: {e}, mencoba lagi...')
                                time.sleep(1)
                                continue
                            else:
                                break
                        nomor += 1
                    except Exception as e:
                        print(f'Terjadi kesalahan saat membaca line {nomor}: {e}')
                        time.sleep(1)
                        continue

            print("Finis: Semua data telah diproses")

        except FileNotFoundError:
            print(f'File tidak ditemukan: upload_propat.txt')
        except Exception as e:
            print(f'Terjadi kesalahan: {e}')

    else:
        randomdelay = 3

        tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[2]/div[6]/div[2]/button')))
        tombol.click()
        time.sleep(randomdelay)

        p = 1  # nilai awal

        while True:
            try:
                print('[+] next')
                try:
                    tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[{p}]/div/div/div[2]/div/div[2]/button[2]/div/div')))
                except:
                    tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[{p}]/div/div/div[2]/div/div[2]/button[2]/div')))
                tombol.click()
                time.sleep(randomdelay)

                print('[+] showcase product')
                tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[{p}]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/button/div')))
                tombol.click()
                time.sleep(randomdelay)

                # input nama produk
                tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[{p}]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/input')))
                tombol.click()
                tombol.send_keys(namaproduk)
                time.sleep(randomdelay)

                print('[+] click cari')
                tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[{p}]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div')))
                tombol.click()
                time.sleep(randomdelay)

                print('[+] pilih produk pertama')
                tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[{p}]/div[2]/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[1]/div/div[1]/div[1]/input')))
                tombol.click()
                time.sleep(randomdelay)

                print('[+] next')
                tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[{p}]/div[2]/div/div/div[3]/button[2]')))
                tombol.click()
                time.sleep(randomdelay)

                print('[+] add')
                tombol = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[{p}]/div[2]/div/div/div[3]/button[2]/div')))
                tombol.click()
                time.sleep(randomdelay)

                print(f"Sukses di p={p-1}, coba p={p}")
                break  # keluar dari loop jika berhasil
            except:
                p += 1  # tambah 1 jika gagal

def aturwaktu(jam, menit):
    jam = str(int(jam) + 1)  # Pastikan jam bertipe string setelah diubah
    time.sleep(10)  # Tunggu halaman siap

    # Klik dropdown waktu dulu (jika perlu)
    try:
        dropdown = driver.find_element(By.XPATH, "//div[@class='schedule-time-dropdown']")
        dropdown.click()
        time.sleep(1)  # Tunggu dropdown muncul
    except:
        print("Dropdown tidak ditemukan atau tidak perlu diklik")

    # Pilih opsi waktu
    try:
        time_option = driver.find_element(By.XPATH, f"//div[contains(@class, 'calendar-time-option') and text()='{jam}']")
        time_option.click()
    except:
        print(f"Tidak bisa menemukan opsi waktu untuk {jam}")

def chekcopyrigth():
    xpaths = [
        "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[7]/div/div[1]/div/div[2]/div/span",
        "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[7]/div/div[1]/div/div[2]/div",
        "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[7]/div/div[1]/div/div[2]",
        "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[7]/div/div[1]/div",
        "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[7]/div/div[1]",
    ]

    for path in xpaths:
        elements = driver.find_elements(By.XPATH, path)
        if elements:
            elements[0].click()
            print('[+] sukses chek copy right')
            return

    print('[+] Gagal membuat cherk copy right , hehehe')

def draft():

    ############### Menjadikan Video Draft ###############
    xpath_tombol = '/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[5]/div/button[2]'

    try:
        tombol = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath_tombol))
        )
        tombol.click()
        print("✅ Video berhasil disimpan sebagai draft!")
    except Exception as e:
        print(f"❌ Gagal menyimpan sebagai draft: {e}")

def posting():
    while True:
        berhasil = False

        for p in range(1, 11):  # dari 1 sampai 10
            xpath_tombol = f'/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[{p}]/div/button[1]'

            try:
                tombol = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_tombol))
                )
                tombol.click()
                print(f"✅ Video berhasil di posting pada index ke-{p}!!!")
                berhasil = True
                break  # keluar dari for-loop
            except Exception as e:
                pass
                #print(f"⚠️ Gagal klik pada index {p}: {e}")

        if berhasil:
            driver.quit()
            break  # keluar dari while-loop jika berhasil
        else:
            print("❌ Tidak ada tombol yang bisa diklik dari index 1 sampai 10. Ulangi...")

    pass

def autoupload(judul, id_produk, nama_barang,external_driver):
    # MODIFIKASI: Assign external driver ke global driver
    global driver
    driver = external_driver

    delay_eksekusi = 2

    discard_memory_draft()

    time.sleep(delay_eksekusi)

    uploadvidio(judul) ##################

    time.sleep(delay_eksekusi)

    #chekcopyrigth() ##################

    time.sleep(delay_eksekusi)

    deskripsiedit(nama_barang) ##################

    time.sleep(delay_eksekusi)

    inputproduk(id_produk) ##################

    time.sleep(delay_eksekusi)

    #draft()
    posting()