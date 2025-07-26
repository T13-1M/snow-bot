# 🤖 Snow Bot - Bot Discord Multifungsi

Selamat datang di repository Snow Bot! Ini adalah bot Discord serbaguna yang dibuat dengan Python (`discord.py`), dirancang untuk memeriahkan server dengan berbagai fitur interaktif.

## ✨ Fitur-fitur Keren
- 📈 **Sistem Level & XP**: Pengguna akan mendapatkan XP dan naik level setiap kali mengirim pesan, membuat server jadi lebih aktif!
- 🏆 **Papan Peringkat (/lb)**: Tampilkan 10 pengguna dengan level tertinggi di server.
- 🧠 **AI Chat Cerdas**: Ngobrol langsung dengan AI Google Gemini di channel khusus. Bot akan mengingat riwayat percakapan per pengguna.
- 😂 **Meme Acak**: Kirim meme baru dan lucu dari internet dengan satu perintah.
- ℹ️ **Info Lengkap**: Dapatkan informasi detail tentang server atau pengguna tertentu.
- 👋 **Sambutan Otomatis**: Pesan selamat datang dan selamat tinggal yang personal dengan embed keren saat ada anggota yang bergabung atau keluar.
- 🎮 **Game Sederhana**: Mainkan game simpel seperti lempar koin (`!coinflip`).
- 🔒 **Perintah Khusus Admin**: Moderator dan pemilik server punya akses ke perintah khusus seperti kick anggota dan hapus pesan massal.

## ⚙️ Cara Setup dan Instalasi

Untuk menjalankan bot ini di servermu sendiri, ikuti langkah-langkah berikut:

#### 1. Prasyarat
- Python 3.8 atau yang lebih baru
- Akun Discord dan sudah membuat aplikasi bot untuk mendapatkan token.
- API Key dari Google AI Studio untuk fitur Gemini.

#### 2. Instalasi
1.  **Clone repository ini ke komputermu:**
    ```bash
    git clone [https://github.com/](https://github.com/)T13-1M/snow-botpy.git
    ```

2.  **Pindah ke direktori proyek:**
    ```bash
    cd snow-bot
    ```

3.  **Install semua library yang dibutuhkan:**
    (Buat file `requirements.txt` dengan isi di bawah, lalu jalankan perintah pip)
    ```txt
    # Isi untuk file requirements.txt
    discord.py
    python-dotenv
    google-generativeai
    aiohttp
    ```
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup Environment Variabel**
    Buat file baru bernama `.env` di dalam folder proyek. Salin konten di bawah ini dan isi dengan nilaimu sendiri. **JANGAN BAGIKAN ISI FILE INI KE SIAPAPUN!**
    ```env
    DISCORD_TOKEN="TOKEN_BOT_DISCORD_KAMU"
    GEMINI_API="API_KEY_GEMINI_KAMU"

    # ID Channel (klik kanan channel di Discord dan 'Copy Channel ID')
    ID_CHANNEL_LB="ID_CHANNEL_UNTUK_LEADERBOARD"
    ID_CHANNEL_WELLCOME="ID_CHANNEL_UNTUK_PESAN_SELAMAT_DATANG"
    ID_CHANNEL_EXIT="ID_CHANNEL_UNTUK_PESAN_SELAMAT_TINGGAL"
    ID_CHANNEL_AI="ID_CHANNEL_UNTUK_CHAT_DENGAN_AI"
    ```

5.  **Jalankan Bot**
    Buka terminal di folder proyek dan jalankan:
    ```bash
    python snow.py
    ```

## 📜 Daftar Perintah Utama
- `!menu`: Menampilkan daftar semua perintah yang tersedia.
- `!rank [mention]`: Menampilkan level dan XP. Bisa mention orang lain untuk melihat rank mereka.
- `!leaderboard` atau `!lb`: Menampilkan 10 pengguna teratas.
- `!halo`: Menyapa bot.
- `!meme`: Mengirim meme acak.
- `!coinflip <gambar/coin>`: Bermain tebak koin.
- `!userinfo [mention]`: Menampilkan info tentang seorang pengguna.
- `!serverinfo`: Menampilkan info tentang server saat ini.

## 📄 Lisensi
Proyek ini dilisensikan di bawah **GNU General Public License v3.0**. Lihat file `LICENSE` untuk detail lengkapnya.
