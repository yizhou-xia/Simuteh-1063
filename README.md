# SIMUTEH

Proyek pengolahan citra daun teh sintetis untuk evaluasi kanal warna,
histogram, penapisan, praproses, deteksi tepi, dan analisis morfologi bercak.

## Persiapan lingkungan

Gunakan Python 3.12 atau 3.13 (notebook B1–B5 dijalankan dengan Python 3.13.14;
P5 dan P6 dijalankan ulang dengan Python 3.12.3 dan paket yang sama persis
dengan `requirements.txt`), lalu pasang dependensi dari folder utama repo:

```powershell
python -m pip install -r requirements.txt
```

## Alur eksekusi

Jalankan semua perintah berikut dari folder utama repo:

```powershell
python src/buat_dataset_sintetis.py
```

Seluruh sumber keacakan proyek menggunakan seed tetap `1063`. Perintah tersebut
menghasilkan 60 citra pada
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
`src/utils_tepi.py`, dan `src/bercak.py`. Jalankan setiap notebook dengan kernel
Python 3.12 atau 3.13. Ketujuh notebook di atas telah diverifikasi dengan
Restart & Run All dari awal sampai akhir tanpa error (nomor eksekusi dimulai
dari 1), dan hasil analisis disimpan di folder `hasil/`.

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
`b3_panel_v_vs_bgr.png`, `b4_psnr_normal.csv`, `b4_psnr_waktu.png`,
`b4_di_bercak.png`, `b5_kb_ringkasan.csv`, `b5_bercak_palsu.csv`,
`b5_panel_praproses.png`, `b5_diagram_final.png`, dan
`param_praproses.json`.

Hasil P5 meliputi:

- `p5_tabel_tepi.csv`, `p5_tabel6_f1.csv`, dan `p5_f1_kondisi.png` untuk
  perbandingan Sobel, Prewitt, LoG, dan Canny (Tabel 6);
- `p5_canny_eksperimen.csv`, `p5_tabel7_canny.csv`, `p5_canny_otomatis.csv`,
  `p5_f1_ambang_per_kondisi.csv`, dan `p5_canny_persentil.csv` untuk
  pemilihan parameter Canny (Tabel 7 dan Langkah 2.4);
- `p5_gradien_magnitudo_tepi_daun.csv`, `p5_gradien_tepi_daun.csv`,
  `p5_median_kanal_kondisi.csv`, `p5_tepi_palsu.csv`, dan
  `p5_tepi_palsu_teh011.png` untuk bukti gradien tepi daun dan tepi palsu
  pada daun sehat.

Keputusan pemakaian deteksi tepi (Tabel 8) ada pada sel markdown terakhir
`notebook/P5_tepi.ipynb`.

Hasil P6 meliputi:

- `p6_operasi_morfologi.csv`, `p6_operasi_teh_021.png`,
  `p6_operasi_teh_011.png`, `p6_eksperimen_se.csv`, `p6_tabel9_se_k4.csv`,
  dan `p6_panel_se.png` untuk Kode 3.2, Tabel 9, dan elemen penstruktur;
- `p6_gradien_morfologi.csv` untuk perbandingan gradien morfologi dan Canny;
- `p6_ukuran_teh041.csv`, `p6_penyaringan.csv`, dan `p6_sebar_komponen.png`
  (kebulatan vs rasio aspek dan luas vs kebulatan, lengkap dengan garis
  ambang) untuk pengukuran dan penyaringan komponen (Tabel 10 dan 11);
- `p6_evaluasi_bercak.csv`, `p6_akurasi_per_kondisi.csv`,
  `p6_persen_prediksi_vs_acuan.png`, dan `param_bercak.json` untuk evaluasi
  akhir analisis bercak (Tabel 12);
- `p6_diagnosis_salah_kelas.csv` (penyebab terukur per citra),
  `p6_salah_kelas_1.png` sampai `p6_salah_kelas_3.png` (panel kesepuluh citra
  salah kelas), dan `p6_sensitivitas_param.csv` (bahan Tabel 13).

Justifikasi parameter (Tabel 13) ada pada sel markdown terakhir
`notebook/P6_morfologi.ipynb`.

## Tag rilis

- `v0.2-tepi`: Pertemuan 5 (deteksi tepi, Canny, dan keputusan pemakaian tepi).
- `v0.3-morfologi`: Pertemuan 6 (morfologi, komponen terhubung, dan `src/bercak.py`).

## Ringkasan hasil evaluasi

- Kanal terpilih adalah **R** pada lima kondisi pencahayaan.
- Pada P2.3, **H > V** pada gelap/terang/bayangan
  (5,53 / 6,68 / 5,75 dibanding 3,33 / 1,38 / 1,18), tetapi H turun
  menjadi 1,91 pada kontras rendah sehingga dukungannya hanya sebagian.
- Pada P4.3, `gauss_5` bukan PSNR tertinggi. Untuk `gauss_20` urutannya
  `median_9` 35,89 > `rerata_5` 34,93 > `median_5` 33,51 >
  `gauss_5` 32,67; `median_3` terendah (29,78).
- Pada P4.5, urutan redam lalu tajam tidak selalu lebih baik:
  Gaussian 30,35 vs 30,24 dan Median 30,18 vs 31,15.
- Pada B5.1, hanya kondisi terang yang mengalami penurunan KB (-16,8%).
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
- Pada P2.3, angka data tidak sepenuhnya mengikuti premis soal: pada
  kontras rendah, otomatis/tetap 30/90 menghasilkan F1 Gray 0,686/0,927
  dan R 0,571/0,971. Berdasarkan rerata keluaran
  `p5_gradien_magnitudo_tepi_daun.csv`, norma L1 gradien tepi daun adalah
  Gray 177,0 dibanding ambang otomatis 99,2/197,2, dan R 222,9 dibanding
  101,5/201,5. Ambang otomatis berasal dari intensitas, bukan magnitudo
  gradien.
- Pada P2.5, kanal R menghasilkan 0 piksel tepi internal pada bayangan,
  gelap, dan kontras rendah, tetapi 176 pada normal dan 260,5 pada terang.
  Kanal Gray berada pada kisaran 328–950, sehingga premis hanya berlaku
  sebagian.
- Keputusan Tabel 8: Canny kanal R, sigma 2, ambang 30/90 dipakai untuk batas
  daun, batas bercak, dan kontur calon fitur bentuk; tepi tidak dipakai untuk
  mengisi wilayah bercak.
- Pada P6, integrasi analisis bercak menghasilkan galat absolut rerata
  persen bercak 0,646%, korelasi prediksi-acuan 0,939, dan akurasi kelas
  0,833 pada 60 citra.
- Run All menghasilkan 10 citra salah kelas (2 daun sehat dinilai berbercak,
  5 bercak ringan dinilai sehat, 3 bercak berat dinilai ringan). Empat di
  antaranya berada pada kondisi kontras rendah dengan IoU `mask_daun_awal`
  hanya 0,52–0,77 (citra lain minimal 0,996); penyebab per citra ada pada
  `p6_diagnosis_salah_kelas.csv`. Untuk Tabel 11, jumlah daun sehat dengan
  bercak palsu berturut-turut sesuai aturan adalah 10, 10, 10, dan 3.
- Aturan penyaringan `luas + kebulatan + rasio` menghasilkan galat jumlah
  rata-rata terendah pada daun sehat (0,40) dibandingkan aturan tanpa
  penyaringan (3,35).
- Uji sensitivitas (`p6_sensitivitas_param.csv`): akurasi kelas bergerak
  0,750–0,850 saat satu parameter diubah; yang paling berpengaruh adalah
  `batas_berat` (3,0 menurunkan akurasi menjadi 0,750) dan `batas_ringan`
  (0,2 menjadi 0,783). Nilai final tetap nilai bawaan karena memilih
  parameter dengan data evaluasi yang sama membuat akurasi terlalu
  optimistis (P5.2).

## Struktur data sintetis

- `data/sintetis/citra/`: citra dengan gangguan pencahayaan dan derau
- `data/sintetis/bersih/`: citra acuan tanpa gangguan
- `data/sintetis/mask_daun/`: mask area daun
- `data/sintetis/mask_bercak/`: mask area bercak
- `data/sintetis/label.csv`: label kelas, kondisi cahaya, dan persentase bercak

Untuk mengulang dataset dari kondisi bersih, hapus `data/sintetis/` lalu jalankan
kembali generator. Jangan menghapus `data/sintetis/bersih/` jika citra acuan
ingin dipertahankan.
