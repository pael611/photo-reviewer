# Rafael Gallery - Photo Media Web App

Rafael Gallery adalah aplikasi web berbasis Flask yang memungkinkan pengguna untuk mengunggah, mengedit, dan menghapus foto beserta deskripsi dan foto profil. Aplikasi ini juga menyediakan fitur untuk membuat postingan secara acak menggunakan API eksternal.

## Fitur

- **Upload Foto**: Pengguna dapat mengunggah foto beserta foto profil, judul, dan deskripsi.
- **Edit Post**: Pengguna dapat mengedit postingan yang sudah ada, termasuk mengganti foto dan deskripsi.
- **Delete Post**: Pengguna dapat menghapus postingan beserta file gambar dari server.
- **Random Post**: Pengguna dapat membuat postingan acak dengan mengambil data dari [randomuser.me](https://randomuser.me), [dog.ceo](https://dog.ceo), dan [dogapi.dog](https://dogapi.dog).
- **Responsive UI**: Menggunakan Bootstrap untuk tampilan yang menarik dan responsif.
- **Footer Profil**: Menampilkan informasi pribadi, hobi, dan kontak developer.

## Struktur Direktori

```
.
├── app.py
├── requirements.txt
├── start.sh
├── .env
├── static/
│   ├── bootstrap.min.css
│   ├── bootstrap.min.js
│   ├── postYYYY-MM-DD-HH-MM-SS.jpg
│   └── profile/
│       └── profileYYYY-MM-DD-HH-MM-SS.jpg
└── templates/
    ├── index.html
    ├── editPost.html
    └── footer.html
```

## Instalasi & Menjalankan Aplikasi

1. **Clone repository ini**

   ```sh
   git clone <repo-url>
   cd project1
   ```
2. **Siapkan file `.env`**Isi file `.env` dengan variabel berikut:

   ```
   MONGODB_URI=<mongodb-uri-anda>
   DB_NAME=<nama-database-anda>
   ```
3. **Jalankan aplikasi**Gunakan script berikut untuk menginstall dependensi dan menjalankan server:

   ```sh
   bash start.sh
   ```

   Atau secara manual:

   ```sh
   python3 -m venv .data/venv
   source .data/venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```
4. **Akses aplikasi**
   Buka browser dan akses `http://localhost:5000`

## Penjelasan File Penting

- [`app.py`](app.py): Seluruh logika backend (Flask), routing, dan interaksi database MongoDB.
- [`templates/index.html`](templates/index.html): Halaman utama untuk upload dan menampilkan foto.
- [`templates/editPost.html`](templates/editPost.html): Halaman untuk mengedit postingan.
- [`templates/footer.html`](templates/footer.html): Footer dengan informasi developer.
- [`static/`](static/): Menyimpan file statis seperti CSS, JS, dan gambar hasil upload.
- [`start.sh`](start.sh): Script otomatis untuk setup virtual environment dan menjalankan aplikasi.

## API Endpoint

- `GET /diary`Mengambil seluruh postingan dalam format JSON.
- `POST /diary`Menyimpan postingan baru (dengan upload file).
- `POST /diary/random`Menyimpan postingan acak dari API eksternal.
- `POST /diary/delete`Menghapus postingan berdasarkan ID.
- `GET,POST /diary/edit/<id>`
  Mengambil data postingan untuk diedit dan menyimpan perubahan.

## Catatan

- Semua file gambar yang diupload akan disimpan di folder `static/` dan `static/profile/`.
- Pastikan MongoDB sudah berjalan dan URI sudah benar di file `.env`.
- Untuk fitur random, aplikasi membutuhkan koneksi internet untuk mengakses API eksternal.
