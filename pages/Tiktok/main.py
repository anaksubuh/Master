import undetected_chromedriver as uc
import os
import time
from selenium.webdriver.common.by import By

class TikTokChrome:
    def __init__(self):
        self.driver = None
        self.profile_path = r"D:\\Master Profile\\tiktok\\jojo2801"
    
    def create_driver(self):
        """Buat Chrome driver dengan profile"""
        try:
            options = uc.ChromeOptions()
            options.add_argument(f"--user-data-dir={self.profile_path}")
            options.add_argument("--profile-directory=Default")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            self.driver = uc.Chrome(options=options, driver_executable_path=None)
            #self.driver.set_window_size(1920, 1080)
            #self.driver.set_window_position(0, 1080)
            #self.driver.set_window_position(0, 0)
            print("✅ Chrome driver berhasil dibuat")
            return True
            
        except Exception as e:
            print(f"❌ Error membuat driver: {str(e)}")
            return False
    
    def open_tiktok(self):
        """Buka TikTok"""
        if not self.driver:
            print("❌ Driver belum dibuat")
            return False
        
        self.driver.get("https://www.tiktok.com/tiktokstudio/upload?from=creator_center")
        self.driver.maximize_window()
        print("✅ TikTok Studio dibuka")
        return True
    
    def check_login(self):
        """Cek status login berdasarkan avatar profile"""
        try:
            self.driver.get("https://www.tiktok.com/tiktokstudio/upload?from=creator_center")
            time.sleep(5)
            
            # Cek apakah ada avatar/profile image yang loaded
            avatar_indicators = [
                "img[src*='tiktokcdn.com']",
                "img[alt*='avatar']",
                "img[class*='avatar']",
                "div[class*='avatar']",
                "//img[contains(@src, 'tiktokcdn.com')]",
                "//div[contains(@class, 'avatar')]"
            ]
            
            # Cek semua kemungkinan elemen avatar
            for indicator in avatar_indicators:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, indicator) if "//" not in indicator else self.driver.find_elements(By.XPATH, indicator)
                    for element in elements:
                        # Cek jika element visible dan ada src attribute
                        if element.is_displayed():
                            src = element.get_attribute('src') or ''
                            if 'tiktokcdn.com' in src:
                                print(f"✅ Avatar ditemukan: {src[:50]}...")
                                return True
                except:
                    continue
            
            # Cek alternative: apakah ada tombol upload video (indikator sudah login di studio)
            upload_indicators = [
                "//div[contains(text(), 'Upload video')]",
                "//button[contains(text(), 'Upload')]",
                "//div[contains(@class, 'upload')]"
            ]
            
            for indicator in upload_indicators:
                try:
                    if self.driver.find_elements(By.XPATH, indicator):
                        print("✅ Elemen upload ditemukan - sudah login")
                        return True
                except:
                    continue
            
            # Jika tidak ada avatar dan tidak ada elemen upload, berarti belum login
            print("❌ Tidak ditemukan avatar/profile image")
            return False
            
        except Exception as e:
            print(f"Error cek login: {str(e)}")
            return False
    
    def wait_for_manual_login(self):
        """Tunggu user login manual"""
        print("⏳ Menunggu login manual...")
        input("🔑 Silakan login manual di browser, lalu tekan Enter di sini...")
        
        # Verifikasi login setelah manual login
        time.sleep(3)
        if self.check_login():
            print("✅ Login berhasil!")
            return True
        else:
            print("❌ Masih belum login, coba lagi")
            return False
    
    def close(self):
        """Tutup driver"""
        if self.driver:
            time.sleep(25)
            self.driver.quit()
            print("✅ Driver ditutup")

def main(video_id, namaproduk):
    # Buat instance
    tiktok = TikTokChrome()
    
    try:
        # Buat driver
        if tiktok.create_driver():
            # Buka TikTok Studio
            tiktok.open_tiktok()
            
            # Cek login status
            status = tiktok.check_login()
            print(f"🔐 Status Login: {'✅ SUDAH LOGIN' if status else '❌ BELUM LOGIN'}")
            
            # Jika belum login, tunggu manual login
            if not status:
                print("⚠️ Browser dibuka, silakan login manual...")
                if tiktok.wait_for_manual_login():
                    print("🎉 Login berhasil! Browser siap digunakan.")
                else:
                    print("❌ Gagal login, aplikasi ditutup.")
                    return
            
            print("\n" + "="*50)
            print("🎬 TIKTOK STUDIO READY!")
            print("="*50)
            print("✅ Browser sudah login")
            print("✅ TikTok Studio terbuka") 
            print("✅ Siap untuk upload video")
            print("\n🔄 Biarkan browser terbuka untuk proses upload...")

            # PERBAIKAN: Panggil function dengan parameter yang benar
            import uploader as up
            up.autoupload(video_id, namaproduk, tiktok.driver)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        # Tutup
        tiktok.close()

#if __name__ == "__main__":
#    main()