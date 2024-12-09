import csv
import hashlib
from datetime import datetime, timedelta
from fpdf import FPDF
import re
import pandas as pd

# MUTTAQIN =============================
def id_berikutnya(filename):
    try:
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                return int(rows[-1][0]) + 1
    except FileNotFoundError:
        pass
    return 1

# Menu utama
def main_menu():
    print("=== Selamat Datang di Lahanku ===")
    print("[1] Login")
    print("[2] Register")
    pilihan = input("Pilih menu: ")
    
    if pilihan == '1':
        login()
    elif pilihan == '2':
        register()
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
        main_menu()

def register():
    print("=== Registrasi ===")
    
    try:
        users_df = pd.read_csv("users.csv", header=None)
        users_df.columns = ["user_id", "nama", "email", "password", "ktp", "nomor_hp", "alamat", "level"]
    except FileNotFoundError:
        users_df = pd.DataFrame(columns=["user_id", "nama", "email", "password", "ktp", "nomor_hp", "alamat", "level"])
    
    user_id = 1 if users_df.empty else users_df["user_id"].max() + 1

    nama = input("Masukkan Nama: ")
    email = input("Masukkan Email: ")
    password = input("Masukkan Password: ")
    ktp = input("Masukkan No KTP: ")
    nomor_hp = input("Masukkan Nomor HP: ")
    alamat = input("Masukkan Alamat: ")
    
    print("Pilih jenis akun:")
    print("[1] Pengguna")
    print("[2] Pemilik Lahan")
    pilihan_level = input("Pilih (1/2): ")
    
    if pilihan_level == '1':
        level = "pengguna"
    elif pilihan_level == '2':
        level = "pemilik_lahan"
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
        register()
        return
    
    password = hashlib.sha256(password.encode()).hexdigest()
    
    new_user = pd.DataFrame({
        "user_id": [user_id],
        "nama": [nama],
        "email": [email],
        "password": [password],
        "ktp": [ktp],
        "nomor_hp": [nomor_hp],
        "alamat": [alamat],
        "level": [level]
    })
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    
    users_df.to_csv("users.csv", index=False, header=False)
    
    print("Registrasi berhasil! Silakan login.")
    main_menu()

# Fungsi login
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def login():
    print("=== Login ===")
    email = input("Masukkan Email: ").strip()
    password = input("Masukkan Password: ").strip()

    if not is_valid_email(email):
        print("Format email tidak valid. Silakan coba lagi.")
        login()
        return

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        with open("users.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == email and row[3] == password_hash:
                    print(f"Login berhasil! Selamat datang, {row[1]}")
                    show_menu(row[7], row[0])
                    return

    except FileNotFoundError:
        print("Database pengguna belum tersedia. Silakan registrasi terlebih dahulu.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    print("Email atau password salah. Coba lagi.")
    main_menu()

# Menu sesuai level
def show_menu(level, user_id):
    print("\n=== Menu Utama ===")
    print("[0] Profil")
    if level == "pengguna":
        print("[1] Sewa Lahan")
        print("[2] Data Perjanjian")
        print("[3] Lihat History")
        pilihan = input("Pilih menu: ")
        if pilihan == '0':
            show_profile(level, user_id)
        elif pilihan == '1':
            sewa_lahan(user_id)
        elif pilihan == '2':
            data_perjanjian(user_id)
        elif pilihan == '3':
            lihat_history(user_id)
        else:
            print("Pilihan tidak valid. Silahkan coba lagi")
            show_menu(level, user_id)

    elif level == "pemilik_lahan":
        print("[1] Data Lahan")
        print("[2] List Penyewa")
        pilihan = input("Pilih menu: ")
        if pilihan == '0':
            show_profile(level, user_id)
        elif pilihan == '1':
            data_lahan(user_id)
        elif pilihan == '2':
            list_penyewa(user_id)
        else:
            print("Pilihan tidak valid. Silahkan coba lagi")
            show_menu(level, user_id)

    elif level == "admin":
        print("[1] Rekap Penyewaan")
        print("[2] Rekap Jumlah Pengguna")

        while True:
            pilihan = input("Pilih menu: ")
            if pilihan == '1':
                rekap_penyewaan(user_id)
                break
            elif pilihan == '2':
                rekap_jumlah_pengguna(user_id)
                break
            elif pilihan == '0':
                show_profile(level, user_id)
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
    else:
        print("Level akses tidak dikenali.")
        return

# SEMUA HAK AKSES
def show_profile(level, user_id):
    try:
        with open('users.csv', 'r') as file:
            users = list(csv.reader(file))

        user_index = next((i for i, u in enumerate(users) if u[0] == user_id), None)

        if user_index is None:
            print("Pengguna tidak ditemukan.")
            return

        user = users[user_index]

        print("\n=== Profil Pengguna ===")
        print(f"ID Pengguna: {user[0]}")
        print(f"Nama: {user[1]}")
        print(f"Email: {user[2]}")
        print(f"Nomor KTP: {user[4]}")
        print(f"Nomor HP: {user[5]}")
        print(f"Alamat: {user[6]}")
        print("=" * 30)

        print("Pilih data yang ingin diubah:")
        print("[1] Nama")
        print("[2] Email")
        print("[3] Nomor KTP")
        print("[4] Nomor HP")
        print("[5] Alamat")
        print("[0] Kembali ke Menu Utama")
        print(" ")
        print("=====Logout=====")
        print("[9] Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            new_name = input("Masukkan nama baru: ")
            users[user_index][1] = new_name
            print(f"Nama berhasil diubah menjadi {new_name}")
        elif pilihan == '2':
            new_email = input("Masukkan email baru: ")
            users[user_index][2] = new_email
            print(f"Email berhasil diubah menjadi {new_email}")
        elif pilihan == '3':
            new_ktp = input("Masukkan nomor KTP baru: ")
            users[user_index][4] = new_ktp
            print(f"Nomor KTP berhasil diubah menjadi {new_ktp}")
        elif pilihan == '4':
            new_phone = input("Masukkan nomor HP baru: ")
            users[user_index][5] = new_phone
            print(f"Nomor HP berhasil diubah menjadi {new_phone}")
        elif pilihan == '5':
            new_address = input("Masukkan alamat baru: ")
            users[user_index][6] = new_address
            print(f"Alamat berhasil diubah menjadi {new_address}")
        elif pilihan == '0':
            show_menu(level, user_id)
            return
        elif pilihan == '9':
            print("Terima kasih telah menggunakan layanan kami. Sampai jumpa kembali!")
            return
        else:
            print("Pilihan tidak valid. Kembali ke menu utama.")
            show_menu(level, user_id)
            return

        with open('users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(users)

        show_menu(level, user_id)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# MUTTAQIN ===========================

# PENGGUNA

# SHINTA ==========================
def sewa_lahan(user_id):
    print("\n=== Sewa Lahan ===")
    tanaman_cari = input("Masukkan tanaman yang ingin Anda tanam: ").lower()
    lahan_ditemukan = []

    print(f"\nLahan yang cocok untuk '{tanaman_cari}':")
    print(f"{'No':<5} {'Lokasi':<30} {'Tanaman':<40} {'Luas':<10} {'Harga/hektar':<15}")
    print("=" * 100)

    try:
        with open("lahan.csv", mode="r") as file:   
            reader = csv.reader(file)
            lahan_data = list(reader)
            nomor = 1
            for row in lahan_data:
                tanaman_list = [tanaman.strip().lower() for tanaman in row[3].split(",")]
                if tanaman_cari in tanaman_list:
                    lahan_ditemukan.append(row)
                    print(f"{nomor:<5} {row[2]:<30} {row[3]:<40} {row[5]:<10} {row[6]:<15}")
                    nomor += 1
                    
    except FileNotFoundError:
        print("Belum ada data lahan.")

    if not lahan_ditemukan:
        print("Tidak ada lahan yang cocok untuk tanaman tersebut.")
        input("\nTekan Enter untuk kembali.")
        show_menu("pengguna", user_id)
        return

    nomor_pilih = int(input("\nPilih nomor lahan yang ingin Anda sewa (0 untuk batal): "))
    if nomor_pilih == 0:
        show_menu("pengguna", user_id)
        return

    if 1 <= nomor_pilih <= len(lahan_ditemukan):
        detail_lahan(user_id, lahan_ditemukan[nomor_pilih - 1])
    else:
        print("Nomor tidak valid.")
        sewa_lahan(user_id)

def detail_lahan(user_id, lahan):
    print("\n=== Detail Lahan ===")
    print(f"Lokasi: {lahan[2]}")
    print(f"Tanaman yang bisa ditanam: {lahan[3]}")
    print(f"Deskripsi: {lahan[4]}")
    print(f"Luas: {lahan[5]} hektar")
    print(f"Harga per hektar (per bulan): {lahan[6]}")

    tanggal_sewa = input("\nMasukkan tanggal sewa (YYYY-MM-DD): ")
    durasi_bulan = int(input("Masukkan durasi sewa (dalam bulan): "))
    luas_sewa = float(input("Masukkan luas lahan yang ingin Anda sewa (hektar): "))

    try:
        tanggal_sewa_date = datetime.strptime(tanggal_sewa, "%Y-%m-%d")
        tanggal_berakhir = tanggal_sewa_date + timedelta(days=30 * durasi_bulan)
        total_harga = luas_sewa * float(lahan[6]) * durasi_bulan

        print(f"\nTanggal Berakhir: {tanggal_berakhir.strftime('%Y-%m-%d')}")
        print(f"Konfirmasi Harga: Rp {total_harga:,.2f}")
        konfirmasi = input("Apakah Anda ingin melanjutkan? (y/n): ").lower()

        if konfirmasi == 'y':
            tambah_sewa(user_id, lahan, tanggal_sewa, tanggal_berakhir.strftime('%Y-%m-%d'), luas_sewa, total_harga)
        else:
            print("Sewa dibatalkan.")
    except ValueError:
        print("Format tanggal tidak valid.")
    
    input("\nTekan Enter untuk kembali.")
    show_menu("pengguna", user_id)

def tambah_sewa(user_id, lahan, tanggal_sewa, tanggal_berakhir, luas_sewa, total_harga):
    try:
        with open("lahan.csv", mode="r") as file:
            reader = csv.reader(file)
            lahan_data = list(reader)
        
        max_luas = None
        for row in lahan_data:
            if len(row) > 1 and row[0] == lahan[0]:
                max_luas = float(row[5])
                break
        
        if max_luas is None:
            print("ID lahan tidak ditemukan. Pastikan data 'lahan.csv' benar.")
            return

        with open("sewa.csv", mode="r") as file:
            reader = csv.reader(file)
            sewa_data = list(reader)
        
        total_luas_disewa = 0
        for row in sewa_data:
            if len(row) > 5 and row[2] == lahan[0]:
                sewa_start = datetime.strptime(row[3], "%Y-%m-%d")
                sewa_end = datetime.strptime(row[4], "%Y-%m-%d")
                input_start = datetime.strptime(tanggal_sewa, "%Y-%m-%d")
                input_end = datetime.strptime(tanggal_berakhir, "%Y-%m-%d")
                
                if not (input_end < sewa_start or input_start > sewa_end):
                    total_luas_disewa += float(row[5])

        if total_luas_disewa + luas_sewa > max_luas:
            print(f"Lahan sudah tersewa penuh untuk tanggal tersebut. Total luas tersedia: {max_luas - total_luas_disewa} hektar.")
            return

        with open("users.csv", mode="r") as file:
            reader = csv.reader(file)
            users_data = list(reader)
        
        id_pemilik = None
        nomor_telepon_pemilik = None
        for row in lahan_data:
            if row[0] == lahan[0]:
                id_pemilik = row[1]
                break
        
        for row in users_data:
            if row[0] == id_pemilik and row[7] == "pemilik_lahan":
                nomor_telepon_pemilik = row[5]
                break

        with open("sewa.csv", mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            last_id = 0
            for row in rows:
                if len(row) > 0 and row[0].isdigit():
                    last_id = max(last_id, int(row[0]))

        new_id = last_id + 1

        with open("sewa.csv", mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                new_id,                
                user_id,               
                lahan[0],              
                tanggal_sewa,          
                tanggal_berakhir,      
                luas_sewa,             
                total_harga,           
                "Belum Perjanjian"     
            ])
        print(f"Data penyewaan dengan ID {new_id} berhasil ditambahkan.")
        print(f"Untuk perjanjian, dapat menghubungi nomor telepon pemilik lahan: {nomor_telepon_pemilik}")
        print("Sewa berhasil ditambahkan. Menunggu perjanjian.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def data_perjanjian(user_id):
    print("\n=== Data Perjanjian ===")
    print(f"{'No':<5} {'Lokasi':<30} {'Tanggal Sewa':<15} {'Tanggal Berakhir':<15} {'Status':<20}  {'ID Lahan':<10}")
    print("="*100)

    data_sewa = []
    lokasi_dict = {}

    try:
        with open("lahan.csv", mode="r") as lahan_file:
            lahan_reader = csv.reader(lahan_file)
            for row in lahan_reader:
                lokasi_dict[row[0]] = row[2]
    except FileNotFoundError:
        print("File 'lahan.csv' tidak ditemukan.")
        return

    try:
        with open("sewa.csv", mode="r") as sewa_file:
            reader = csv.reader(sewa_file)
            for row in reader:
                if row[1] == str(user_id):
                    data_sewa.append(row)
                    
    except FileNotFoundError:
        print("Belum ada data persewaan.")
        show_menu("pengguna", user_id)
        return

    if not data_sewa:
        print("Tidak ada perjanjian yang perlu dibuat.")
        input("\nTekan Enter untuk kembali.")
        show_menu("pengguna", user_id)
        return

    for i, row in enumerate(data_sewa, start=1):
        lokasi_id = row[2]
        lokasi_name = lokasi_dict.get(lokasi_id, "Tidak Dikenal")
        tanggal_sewa = row[3]
        tanggal_berakhir = row[4]
        status = row[7]
        id_lahan = row[2]

        print(f"{i:<5} {lokasi_name:<30} {tanggal_sewa:<15} {tanggal_berakhir:<15} {status:<20} {id_lahan:<10}")

    pilihan = input("\nMasukkan nomor perjanjian untuk dibuat (atau 0 untuk batal): ")
    if pilihan.isdigit() and 1 <= int(pilihan) <= len(data_sewa):
        nomor = int(pilihan) - 1
        buat_surat_perjanjian(data_sewa[nomor], user_id)
        print("Surat perjanjian berhasil dibuat dan disimpan sebagai PDF.")
    elif pilihan == '0':
        print("Pembuatan surat perjanjian dibatalkan.")
        show_menu("pengguna", user_id)
    else:
        print("Pilihan tidak valid.")
    
    input("\nTekan Enter untuk kembali.")
    show_menu("pengguna", user_id)

def get_username(user_id):
    with open("users.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0 and row[0] == str(user_id):
                return row[1]
    return "Unknown"

def buat_surat_perjanjian(data, user_id):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Surat Perjanjian Sewa Lahan", ln=True, align='C')
    pdf.ln(10)

    tanggal_sewa = data[3]
    tanggal_berakhir = data[4]
    luas_sewa = float(data[5])
    total_harga = float(data[6])
    
    total_harga_format = f"Rp {total_harga:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    
    pdf.cell(200, 10, txt=f"Tanggal Sewa: {tanggal_sewa}", ln=True)
    pdf.cell(200, 10, txt=f"Tanggal Berakhir: {tanggal_berakhir}", ln=True)
    pdf.cell(200, 10, txt=f"Luas Lahan: {luas_sewa} hektar", ln=True)
    pdf.cell(200, 10, txt=f"Total Harga: {total_harga_format}", ln=True)
    pdf.cell(200, 10, txt=f"Status: {data[7]}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Dengan ini kedua belah pihak sepakat untuk melaksanakan perjanjian ini.", ln=True)
    pdf.cell(200, 10, txt="Pihak 1: Pemilik Lahan", ln=True)
    pdf.cell(200, 10, txt="Pihak 2: Penyewa", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Tanda Tangan:", ln=True)
    pdf.cell(200, 10, txt="Pihak 1: ___________________", ln=True)
    pdf.cell(200, 10, txt="Pihak 2: ___________________", ln=True)

    nama_penyewa = get_username(user_id).replace(" ", "_")

    id_sewa = data[0]  # ID sewa
    file_name = f"{id_sewa}_{nama_penyewa}.pdf"
    pdf.output(file_name)
    print(f"Surat perjanjian disimpan sebagai {file_name}.")

# SHINTA ============================

# NEVA ================================

def lihat_history(user_id):
    try:
        with open("sewa.csv", mode="r") as file:
            reader = csv.reader(file)
            data_sewa = [row for row in reader if len(row) > 7 and row[1] == str(user_id)]

        if not data_sewa:
            print("\nTidak ada data history penyewaan untuk user ini.")
            input("\nTekan Enter untuk kembali.")
            show_menu("pengguna", user_id)
            return

        print("\n=== History Penyewaan ===")
        print(f"{'No.':<5}{'ID Sewa':<10}{'Status':<15}{'Tgl Sewa':<15}{'Tgl Selesai':<15}{'Harga':<10}")
        for i, row in enumerate(data_sewa, start=1):
            print(f"{i:<5}{row[0]:<10}{row[7]:<20}{row[3]:<15}{row[4]:<15}Rp {float(row[6]):,.2f}")

        pilihan = input("\nMasukkan nomor untuk melihat detail (atau 0 untuk kembali): ")
        if pilihan == '0':
            show_menu("pengguna", user_id)
            return
        
        if not pilihan.isdigit() or not (1 <= int(pilihan) <= len(data_sewa)):
            print("Nomor tidak valid.")
            input("\nTekan Enter untuk kembali.")
            show_menu("pengguna", user_id)
            return

        detail = data_sewa[int(pilihan) - 1]
        print("\n=== Detail Penyewaan ===")
        print(f"ID Sewa: {detail[0]}")
        print(f"Status: {detail[7]}")
        print(f"Tanggal Sewa: {detail[3]}")
        print(f"Tanggal Selesai: {detail[4]}")
        print(f"Luas yang Disewa: {detail[5]} hektar")
        print(f"Total Harga: Rp {float(detail[6]):,.2f}")

        if detail[7] == "Belum Perjanjian":
            print("\nStatus masih 'Belum Perjanjian'. Tidak bisa mengubah status menjadi 'Berjalan' atau 'Selesai'.")
            input("\nTekan Enter untuk kembali.")
            show_menu("pengguna", user_id)
            return

        print("\nUbah status:")
        print("[1] Berjalan")
        print("[2] Selesai")
        status_input = input("Pilih status baru: ")
        if status_input == '1':
            status_baru = "Berjalan"
        elif status_input == '2':
            status_baru = "Selesai"
        else:
            print("Pilihan tidak valid.")
            input("\nTekan Enter untuk kembali.")
            show_menu("pengguna", user_id)
            return

        with open("sewa.csv", mode="r") as file:
            rows = list(csv.reader(file))

        selected_row = data_sewa[int(pilihan) - 1]
        for row in rows:
            if len(row) > 7 and row[0] == selected_row[0] and row[2] == str(user_id):  
                row[7] = status_baru
                break

        with open("sewa.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print(f"\nStatus berhasil diubah menjadi '{status_baru}'.")
        input("\nTekan Enter untuk kembali.")
        show_menu("pengguna", user_id)

    except FileNotFoundError as e:
        print(f"File tidak ditemukan: {e.filename}")
        input("\nTekan Enter untuk kembali.")
        show_menu("pengguna", user_id)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        input("\nTekan Enter untuk kembali.")
        show_menu("pengguna", user_id)

# PEMILIK LAHAN =========
def data_lahan(user_id):
    print("\n=== Data Lahan ===")
    print("[1] Tambah Lahan")
    print("[2] Lihat Semua Lahan")
    print("[0] Kembali")
    pilihan = input("Pilih menu: ")
    
    if pilihan == '1':
        tambah_lahan(user_id)
    elif pilihan == '2':
        lihat_lahan(user_id)
    elif pilihan == '0':
        show_menu("pemilik_lahan", user_id)
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
        data_lahan(user_id)

def tambah_lahan(user_id):
    print("\n=== Tambah Lahan ===")
    lahan_id = id_berikutnya("lahan.csv")
    lokasi = input("Masukkan lokasi lahan: ")
    tanaman = input("Masukkan jenis tanaman (pisahkan dengan koma, contoh: padi,jagung): ").lower()
    deskripsi = input("Masukkan deskripsi lahan: ")
    luas = input("Masukkan luas tanah (dalam hektar): ")
    harga_per_hektar = input("Masukkan harga per hektar: ")
    
    if lokasi == "" or tanaman == "" or deskripsi == "" or luas == "" or harga_per_hektar == "":
        print("Semua field harus diisi.")
        input("\nTekan Enter untuk kembali.")
        data_lahan(user_id)
        return

    with open("lahan.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([lahan_id, user_id, lokasi, tanaman, deskripsi, luas, harga_per_hektar])
    
    print("Lahan berhasil ditambahkan!")
    data_lahan(user_id)

def lihat_lahan(user_id):
    print("\n=== Daftar Lahan ===")
    print(f"{'ID':<5} {'Lokasi':<40} {'Tanaman':<20} {'Luas':<10} {'Harga':<10}")
    print("="*85)
    lahan_ada = False
    
    try:
        with open("lahan.csv", mode="r") as file:
            reader = csv.reader(file)
            lahan_data = list(reader)
            for row in lahan_data:
                if row[1] == user_id:
                    lahan_ada = True
                    print(f"{row[0]:<5} {row[2]:<40} {row[3]:<20} {row[5]:<10} {row[6]:<10}")
    except FileNotFoundError:
        print("Belum ada data lahan.")
    
    if not lahan_ada:
        print("Tidak ada data lahan milik Anda.")
        input("\nTekan Enter untuk kembali.")
        data_lahan(user_id)
        return

    print("\n[1] Hapus Lahan")
    print("[0] Kembali")
    pilihan = input("Pilih menu: ")
    if pilihan == '1':
        hapus_lahan(user_id, lahan_data)
    elif pilihan == '0':
        data_lahan(user_id)
    else:
        print("Pilihan tidak valid.")
        lihat_lahan(user_id)

def hapus_lahan(user_id, lahan_data):
    print("\n=== Hapus Lahan ===")
    id_lahan = input("Masukkan ID Lahan yang ingin dihapus: ")
    lahan_dihapus = False

    with open("lahan.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        for row in lahan_data:
            if row[0] == id_lahan and row[1] == user_id:
                lahan_dihapus = True
            else:
                writer.writerow(row)
    
    if lahan_dihapus:
        print(f"Lahan dengan ID {id_lahan} berhasil dihapus.")
    else:
        print(f"Lahan dengan ID {id_lahan} tidak ditemukan atau bukan milik Anda.")
    
    input("\nTekan Enter untuk kembali.")
    lihat_lahan(user_id)


def list_penyewa(user_id):
    print("\n=== List Penyewa ===")
    try:
        with open("lahan.csv", mode="r") as lahan_file, open("sewa.csv", mode="r") as sewa_file, open("users.csv", mode="r") as users_file:
            lahan_reader = csv.reader(lahan_file)
            sewa_reader = csv.reader(sewa_file)
            users_reader = list(csv.reader(users_file))

            lahan_pemilik = [lahan for lahan in lahan_reader if lahan[1] == user_id]
            if not lahan_pemilik:
                print("Anda belum memiliki lahan terdaftar.")
                return
            
            sewa_terkait = []
            for sewa in sewa_reader:
                for lahan in lahan_pemilik:
                    if sewa[2] == lahan[0]:
                        sewa_terkait.append(sewa)
                        break

            if not sewa_terkait:
                print("Belum ada penyewa untuk lahan Anda.")
                input("\nTekan Enter untuk kembali.")
                show_menu("pemilik_lahan", user_id)
                return
            
            print(f"{'No':<5} {'ID Lahan':<10} {'Lokasi':<40} {'Nama Penyewa':<20} {'Status':<15}")
            print("=" * 90)
            penyewa_dict = {}
            
            for i, sewa in enumerate(sewa_terkait, start=1):
                lahan = next((l for l in lahan_pemilik if l[0] == sewa[2]), None)
                
                penyewa = next((u for u in users_reader if u[0] == sewa[1]), None)
                
                penyewa_dict[str(i)] = (sewa, lahan, penyewa)
                print(f"{i:<5} {lahan[0]:<10} {lahan[2]:<40} {penyewa[1]:<20} {sewa[7]:<15}")
            
            pilihan = input("\nPilih nomor untuk melihat detail (0 untuk kembali): ")
            if pilihan == "0":
                show_menu("pemilik_lahan", user_id)
            if pilihan in penyewa_dict:
                detail_penyewa(penyewa_dict[pilihan], user_id)
            else:
                print("Nomor tidak valid.")
                
    except FileNotFoundError as e:
        print(f"File tidak ditemukan: {e}")

# NEVA ==================================


# FABYAN =================================

def detail_penyewa(data, user_id):
    sewa, lahan, penyewa = data
    print("\n=== Detail Penyewa ===")
    print(f"Nama Penyewa: {penyewa[1]}")
    print(f"Email Penyewa: {penyewa[2]}")
    print(f"No KTP: {penyewa[4]}")
    print(f"Lokasi Lahan: {lahan[2]}")
    print(f"Deskripsi: {lahan[4]}")
    print(f"Luas yang Disewa: {sewa[2]} hektar")
    print(f"Tanggal Sewa: {sewa[4]}")
    print(f"Tanggal Berakhir: {sewa[3]}")
    print(f"Total Harga: Rp {float(sewa[6]):,.2f}") 
    print(f"Status: {sewa[7]}")

    if sewa[7] == "Belum Perjanjian":
        konfirmasi = input("\nApakah Anda ingin menyetujui perjanjian ini? (y/n): ").lower()
        if konfirmasi == 'y':
            update_status_sewa(sewa)
            print("Perjanjian berhasil disetujui. Status diperbarui menjadi 'Belum Berjalan'.")
        else:
            print("Perjanjian tidak disetujui.")
    else:
        input(f"\nStatus sudah {sewa[7]} dan tidak dapat diubah. Tekan Enter untuk kembali ke List Penyewa.")

    list_penyewa(user_id)

def update_status_sewa(sewa):
    # Baca semua data sewa
    with open("sewa.csv", mode="r") as file:
        rows = list(csv.reader(file))
    
    for row in rows:
        if row[:7] == sewa[:7]:
            row[7] = "Belum Berjalan"
    
    with open("sewa.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# ADMIN =================
def rekap_penyewaan(user_id):
    try:
        with open("sewa.csv", "r") as sewa_file, open("users.csv", "r") as user_file, open("lahan.csv", "r") as lahan_file:
            sewa_reader = csv.reader(sewa_file)
            user_reader = csv.reader(user_file)
            lahan_reader = csv.reader(lahan_file)

            user_map = {row[0]: row[1] for row in user_reader if len(row) >= 2}
            lahan_map = {row[0]: {"lokasi": row[2], "id_pemilik": row[1]} for row in lahan_reader if len(row) >= 2}

            print("\n=== List Penyewa ===")
            print(f"{'No':<5} {'ID Lahan':<10} {'Lokasi':<20} {'Nama Penyewa':<20} {'Nama Pemilik':<20} {'Status':<15}")
            print("=" * 100)

            sewa_list = [row for row in sewa_reader if len(row) >= 8]
            if not sewa_list:
                print("Tidak ada data penyewaan.")
                input("\nTekan Enter untuk kembali.")
                show_menu("admin", user_id)
                return

            for i, sewa in enumerate(sewa_list, start=1):
                id_lahan = sewa[2]
                id_penyewa = sewa[1]
                lokasi_lahan = lahan_map.get(id_lahan, {}).get("lokasi", "Unknown")
                id_pemilik = lahan_map.get(id_lahan, {}).get("id_pemilik", "Unknown")
                nama_penyewa = user_map.get(id_penyewa, "Unknown")
                nama_pemilik = user_map.get(id_pemilik, "Unknown")
                status = sewa[7]

                print(
                    f"{i:<5} {id_lahan:<10} {lokasi_lahan:<20} {nama_penyewa:<20} {nama_pemilik:<20} {status:<15}"
                )

            while True:
                pilihan = input("\nMasukkan nomor untuk melihat detail (atau 0 untuk kembali): ")
                if pilihan == "0":
                    show_menu("admin", user_id)
                    return
                if not pilihan.isdigit() or int(pilihan) < 1 or int(pilihan) > len(sewa_list):
                    print("Pilihan tidak valid. Silakan coba lagi.")
                    continue

                index = int(pilihan) - 1
                detail = sewa_list[index]
                tampilkan_detail(detail, user_map, lahan_map)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        input("\nTekan Enter untuk kembali.")
        show_menu("admin", user_id)

def tampilkan_detail(sewa, user_map, lahan_map):
    try:
        id_sewa = sewa[0]
        id_penyewa = sewa[1]
        id_lahan = sewa[2]
        tanggal_mulai = sewa[3]
        tanggal_selesai = sewa[4]
        durasi_bulan = int(float(sewa[5]))
        total_biaya = sewa[6]
        status = sewa[7]
        
        if durasi_bulan < 12:
            durasi = f"{durasi_bulan} bulan"
        else:
            tahun = durasi_bulan // 12
            bulan = durasi_bulan % 12
            if bulan == 0:
                durasi = f"{tahun} tahun"
            else:
                durasi = f"{tahun} tahun {bulan} bulan"

        lokasi_lahan = lahan_map.get(id_lahan, {}).get("lokasi", "Unknown")
        id_pemilik = lahan_map.get(id_lahan, {}).get("id_pemilik", "Unknown")

        nama_penyewa = user_map.get(id_penyewa, "Unknown")
        nama_pemilik = user_map.get(id_pemilik, "Unknown")

        print("\n=== Detail Penyewaan ===")
        print(f"ID Penyewa     : {id_penyewa}")
        print(f"Nama Penyewa   : {nama_penyewa}")
        print(f"ID Sewa        : {id_sewa}")
        print(f"ID Lahan       : {id_lahan}")
        print(f"Lokasi Lahan   : {lokasi_lahan}")
        print(f"Nama Pemilik   : {nama_pemilik}")
        print(f"Tanggal Mulai  : {tanggal_mulai}")
        print(f"Tanggal Selesai: {tanggal_selesai}")
        print(f"Durasi         : {durasi}")
        print(f"Total Biaya    : Rp {float(total_biaya):,.2f}")
        print(f"Status         : {status}")
        print("=" * 30)


    except Exception as e:
        print(f"Terjadi kesalahan saat menampilkan detail: {e}")

def rekap_jumlah_pengguna(user_id):
    try:
        # Membaca file CSV
        with open("users.csv", "r") as user_file, open("sewa.csv", "r") as sewa_file:
            user_reader = csv.reader(user_file)
            sewa_reader = csv.reader(sewa_file)

            users = [row for row in user_reader if len(row) >= 2 and row[7] == 'pengguna']
            if not users:
                print("Tidak ada data pengguna dengan level 'pengguna'.")
                return  

            sewa_list = [row for row in sewa_reader if len(row) >= 2]
            
            pengguna_menyewa = {sewa[1] for sewa in sewa_list}

            print("\n=== Rekap Jumlah Pengguna ===")
            print(f"Total Pengguna dengan level 'pengguna': {len(users)}")
            print(f"Total Pengguna yang Melakukan Penyewaan: {len(pengguna_menyewa)}\n")
            print(f"{'No':<5} {'ID Pengguna':<15} {'Nama Pengguna':<20} {'Status':<20}")
            print("=" * 60)

            for i, user in enumerate(users, start=1):
                id_user = user[0]
                nama_user = user[1]
                status = "Menyewa" if id_user in pengguna_menyewa else "Belum Menyewa"
                print(f"{i:<5} {id_user:<15} {nama_user:<20} {status:<20}")

            input("\nTekan Enter untuk kembali.")
            show_menu("admin", user_id)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# FABYAN ===============================

main_menu()