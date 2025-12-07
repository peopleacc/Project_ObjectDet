Perbaikan fitur upload video dan kamera

Ringkasan perubahan:
- Ditambahkan endpoint `/upload-video/` pada `detector/urls.py` untuk menerima video upload.
- Ditambahkan `upload_video` view di `detector/views.py` yang memproses video frame-by-frame menggunakan OpenCV (cv2) dan menjalankan model YOLO pada setiap frame, lalu mengembalikan file MP4 yang telah dianotasi.
- Template `templates/detector/index.html`:
  - Camera capture sekarang mengarah ke endpoint image (`/upload-image/`) karena kamera hanya menangkap frame gambar satuan.
  - Perbaikan pesanan validasi file agar kamera tidak memblokir upload karena tidak memiliki file input.
  - Kamera tampilan hasil diperlakukan seperti gambar, bukan video.

Langkah pengujian:
1. Jalankan server Django:

```powershell
# Atur environment Python yang sesuai dan jalankan
python manage.py runserver
```

2. Buka halaman utama dan uji:
- Upload gambar: pilih file gambar, klik Upload & Prediksi -> hasil yang dianotasi akan ditampilkan.
- Upload video: pilih file video (mp4), klik Upload & Prediksi -> tunggu proses, hasil video MP4 yang dianotasi akan otomatis diputar dan tersedia untuk di-download.
- Gunakan kamera: pilih Camera, klik Start Camera -> ijinkan akses kamera. Setelah tampilan muncul, klik Capture & Prediksi -> hasil gambar akan ditampilkan.

Catatan penting:
- Untuk kemampuan pemrosesan video (upload-video), proyek ini membutuhkan OpenCV untuk Python (package `opencv-python`). Jika video upload gagal dan server mengembalikan error terkait OpenCV, install package berikut pada environment Anda:

```powershell
pip install opencv-python
```

- Pemrosesan video dapat memakan waktu tergantung ukuran video dan kapasitas hardware.

Jika ingin saya juga menambahkan progress bar atau mengubah penanganan video menjadi pemrosesan asinkron (mis. Celery) untuk menghindari waktu respons lama, beri tahu saya dan saya akan bantu implementasikan.