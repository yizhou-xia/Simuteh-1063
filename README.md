# SIMUTEH

Proyek pengolahan citra daun teh sintetis untuk evaluasi kanal warna,
histogram, penapisan, praproses, deteksi tepi, dan analisis morfologi bercak.

## Persiapan lingkungan

Gunakan Python 3.10 atau lebih baru (hasil eksekusi terakhir diverifikasi pada
Python 3.13), lalu pasang dependensi dari folder utama repo:

```powershell
python -m pip install -r requirements.txt
```

## Alur eksekusi

Jalankan semua perintah berikut dari folder utama repo:

```powershell
python src/buat_dataset_sintetis.py
```

Perintah tersebut menggunakan `SEED = 1063` dan menghasilkan 60 citra pada
`data/sintetis/`, lengkap dengan citra bersih, mask daun, mask bercak, dan
`label.csv`.

Buka notebook secara berurutan di VS Code atau Jupyter:

1. `notebook/B1_lingkungan.ipynb`
2. `notebook/B2_citra_warna.ipynb`
3. `notebook/B3_histogram.ipynb`
4. `notebook/B4_penapisan.ipynb`
5. `notebook/B5_praproses.ipynb`
6. `notebook/P5_tepi.ipynb`
7. `notebook/P6_morfologi.ipynb`

Notebook mengimpor fungsi bersama dari `src/utils_cv.py`, `src/praproses.py`,
`src/utils_tepi.py`, dan `src/bercak.py`. Jalankan setiap notebook dengan kernel Python 3.10
atau lebih baru. Seluruh notebook di atas telah dijalankan ulang dari awal
sampai akhir, dan hasil analisis disimpan di folder `hasil/`.

### Langkah 5.5: analisis bercak yang dapat dipakai ulang

`src/bercak.py` menyediakan `analisis_daun(img_praproses, p=None)`. Masukan adalah
citra BGR hasil `praproses`; keluaran berupa kamus berisi `mask_daun`,
`mask_bercak`, `jumlah_bercak`, `persen_bercak`, `kelas`, dan daftar ukuran
komponen pada kunci `bercak`. Parameter opsional menimpa nilai bawaan:

```python
from bercak import analisis_daun
hasil = analisis_daun(praproses(citra, PARAM), {"luas_min": 20})
print(hasil["kelas"], hasil["persen_bercak"])
```

Hasil utama P1–P4 meliputi `b2_kb_kanal.csv`, `b3_histogram_5kondisi.png`,
`b4_psnr_waktu.png`, `b4_di_bercak.png`, `b5_panel_praproses.png`,
`b5_diagram_final.png`, dan `param_praproses.json`.

Hasil P5 meliputi:

- `p5_tabel_tepi.csv` dan `p5_f1_kondisi.png` untuk perbandingan Sobel,
  Prewitt, LoG, dan Canny;
- `p5_canny_eksperimen.csv`, `p5_canny_otomatis.csv`, dan
  `p5_canny_persentil.csv` untuk pemilihan parameter Canny;
- `p5_tepi_palsu.csv` untuk evaluasi tepi palsu pada daun sehat.

Hasil P6 meliputi:

- `p6_operasi_morfologi.csv`, `p6_eksperimen_se.csv`, dan `p6_panel_se.png`;
- `p6_gradien_morfologi.csv` untuk perbandingan gradien morfologi dan Canny;
- `p6_ukuran_teh041.csv`, `p6_penyaringan.csv`, dan
  `p6_sebar_komponen.png` untuk pengukuran dan penyaringan komponen;
- `p6_evaluasi_bercak.csv`, `p6_persen_prediksi_vs_acuan.png`, dan
  `param_bercak.json` untuk evaluasi akhir analisis bercak dan parameter
  analisis yang dipakai ulang.

## Ringkasan hasil evaluasi

- Kanal terpilih adalah **R** pada lima kondisi pencahayaan.
- Pada P2.3, **H > V** pada gelap/terang/bayangan
  (5,53 / 6,68 / 5,75 dibanding 3,33 / 1,38 / 1,18), tetapi H turun
  menjadi 1,91 pada kontras rendah sehingga dukungannya hanya sebagian.
- Pada P4.3, `gauss_5` bukan PSNR tertinggi. Untuk `gauss_20` urutannya
  `median_9` 35,91 > `rerata_5` 34,92 > `median_5` 33,55 >
  `gauss_5` 32,64; `median_3` terendah (29,76).
- Pada P4.5, urutan redam lalu tajam tidak selalu lebih baik:
  Gaussian 30,32 vs 30,20 dan Median 30,21 vs 31,17.
- Pada P5.1, hanya kondisi terang yang mengalami penurunan KB (-16,8%).
- Pada P3.5, ambang “rerata < 80” tidak pernah aktif; rerata terendah 128,0.
- P1.1 menggunakan piksel BGR `[175 185 189]`. Akuisisi dan P2.1 tetap:
  jarak ≤ 22 cm untuk lebar 640 px, atau ≥ 840 px untuk 30 cm.
- Tabel 12 (kanal R) mencatat KB sebelum/sesudah:
  normal 8,15→10,13; gelap 9,15→15,87; terang 7,04→5,86;
  kontras rendah 3,19→4,63; bayangan 5,54→8,57.
- Uji 20 citra sehat tidak menunjukkan titik terang palsu pada semua kondisi.
- Pada P5, Canny kanal R sesudah praproses menghasilkan F1 rerata 0,970;
  eksperimen sigma 1 dan ambang 100/200 menghasilkan F1 rerata 0,978,
  sedangkan ambang tetap 30/90 menghasilkan F1 0,970 pada sigma 2.
- Ambang Canny berbasis persentil memberi hasil terbaik pada kanal R untuk
  `q=98`, dengan F1 rerata 0,937.
- Pada evaluasi tepi palsu, kanal R menghasilkan lebih sedikit tepi internal
  daripada Gray pada pengujian 20 citra sehat.
- Pada P6, integrasi analisis bercak menghasilkan galat absolut rerata
  persen bercak 0,646%, korelasi prediksi-acuan 0,939, dan akurasi kelas
  0,833 pada 60 citra.
- Aturan penyaringan `luas + kebulatan + rasio` menghasilkan galat jumlah
  rata-rata terendah pada daun sehat (0,40) dibandingkan aturan tanpa
  penyaringan (3,35).

## Struktur data sintetis

- `data/sintetis/citra/`: citra dengan gangguan pencahayaan dan derau
- `data/sintetis/bersih/`: citra acuan tanpa gangguan
- `data/sintetis/mask_daun/`: mask area daun
- `data/sintetis/mask_bercak/`: mask area bercak
- `data/sintetis/label.csv`: label kelas, kondisi cahaya, dan persentase bercak

Untuk mengulang dataset dari kondisi bersih, hapus `data/sintetis/` lalu jalankan
kembali generator. Jangan menghapus `data/sintetis/bersih/` jika citra acuan
ingin dipertahankan.
