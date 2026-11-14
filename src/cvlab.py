"""cvlab.py: utilitas praktikum Computer Vision, Teknik Informatika UMMI 2026/2027.

Berisi fungsi tampilan untuk Google Colab, audit mutu citra, dan pembangkit
citra studi kasus daun teh dengan kondisi lapangan yang dapat diatur.
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

TINGGI, LEBAR = 480, 640


def tampil(*citra, judul=None, kolom=3, lebar=4.5):
    """Menampilkan satu atau beberapa citra di Colab (pengganti cv2.imshow).
    Citra 3 kanal dianggap berurutan BGR seperti hasil cv2.imread."""
    n = len(citra)
    k = min(n, kolom)
    b = (n + kolom - 1) // kolom
    rasio = max(c.shape[0] / c.shape[1] for c in citra)   # tinggi baris mengikuti bentuk citra
    fig, ax = plt.subplots(b, k, figsize=(lebar * k, (lebar * rasio + 0.45) * b), squeeze=False)
    for i, a in enumerate(ax.ravel()):
        a.axis("off")
        if i < n:
            c = citra[i]
            if c.ndim == 3:
                a.imshow(cv2.cvtColor(c, cv2.COLOR_BGR2RGB))
            else:
                a.imshow(c, cmap="gray", vmin=0, vmax=255)
            if judul:
                a.set_title(judul[i])
    plt.tight_layout()
    plt.show()


def tampil_hist(*gray, judul=None, lebar=4.5):
    """Menampilkan histogram 256 level dari satu atau beberapa citra keabuan."""
    n = len(gray)
    fig, ax = plt.subplots(1, n, figsize=(lebar * n, 2.8), squeeze=False)
    for i, g in enumerate(gray):
        h = np.bincount(g.ravel(), minlength=256)
        ax[0, i].bar(np.arange(256), h, width=1.0, color="#2F6FDE")
        ax[0, i].set_xlim(0, 255)
        if judul:
            ax[0, i].set_title(judul[i])
    plt.tight_layout()
    plt.show()


def ke_abu(citra):
    """Mengubah citra BGR menjadi keabuan; citra keabuan dikembalikan apa adanya."""
    return citra if citra.ndim == 2 else cv2.cvtColor(citra, cv2.COLOR_BGR2GRAY)


def audit_mutu(citra):
    """Indikator mutu citra (Bahan Ajar Pertemuan 3, Tabel 13)."""
    g = ke_abu(citra)
    h, w = g.shape
    rerata_area = [g[i * h // 4:(i + 1) * h // 4, j * w // 4:(j + 1) * w // 4].mean()
                   for i in range(4) for j in range(4)]
    p2, p98 = np.percentile(g, [2, 98])
    return {"rerata": round(float(g.mean()), 1),
            "simp_baku": round(float(g.std()), 1),
            "p2": int(p2), "p98": int(p98),
            "jenuh_0_%": round(float((g == 0).mean() * 100), 2),
            "jenuh_255_%": round(float((g == 255).mean() * 100), 2),
            "selisih_area": round(float(max(rerata_area) - min(rerata_area)), 1)}


def diagnosis(m):
    """Diagnosis awal berdasarkan patokan indikatif Tabel 13."""
    hasil = []
    if m["jenuh_0_%"] + m["jenuh_255_%"] > 2:
        hasil.append("jenuh: perbaiki akuisisi")
    if m["selisih_area"] > 70:
        hasil.append("cahaya tidak merata")
    if m["rerata"] < 70:
        hasil.append("gelap")
    elif m["rerata"] > 185:
        hasil.append("terang")
    if m["simp_baku"] < 30 or m["p98"] - m["p2"] < 100:
        hasil.append("kontras rendah")
    return ", ".join(hasil) if hasil else "baik"


def _halus(rng, skala, h=TINGGI, w=LEBAR):
    kecil = rng.random((h // skala + 2, w // skala + 2)).astype(np.float32)
    return cv2.resize(kecil, (w, h), interpolation=cv2.INTER_CUBIC)


def buat_daun(kondisi="normal", seed=1063):
    """Membangkitkan foto sintetis daun teh berbercak 640 x 480 (BGR, uint8).

    kondisi: normal, teduh, terik, kabut, bayangan, iso, rusak, goyang.
    Mengembalikan (citra, info). info berisi citra bersih, mask daun, mask
    bercak, dan daftar bercak (x, y, r) sebagai kebenaran dasar (ground truth).
    """
    rng = np.random.default_rng(seed)
    h, w = TINGGI, LEBAR
    # Latar: tanah bertekstur dan gerumbul daun lain
    t = 0.45 + 0.55 * _halus(rng, 40) + 0.25 * _halus(rng, 8)
    rgb = np.dstack([175 * t, 145 * t, 110 * t])
    gerumbul = np.clip((_halus(rng, 60) - 0.62) * 12, 0, 1)[..., None]
    rgb = rgb * (1 - gerumbul) + np.array([28, 62, 26]) * gerumbul
    # Daun: elips miring dengan gradasi cahaya dan tulang daun
    daun = np.zeros((h, w), np.uint8)
    cv2.ellipse(daun, (330, 240), (240, 125), -20, 0, 360, 255, -1)
    alfa = cv2.GaussianBlur(daun, (5, 5), 0)[..., None] / 255.0
    gradasi = np.linspace(0.7, 1.3, h)[:, None] * (0.88 + 0.24 * _halus(rng, 12))
    warna_daun = np.dstack([70 * gradasi, 150 * gradasi, 55 * gradasi])
    urat = np.zeros((h, w), np.uint8)
    cv2.line(urat, (106, 322), (554, 158), 255, 3)
    for s in np.linspace(0.12, 0.88, 9):
        x0, y0 = int(106 + s * 448), int(322 - s * 164)
        cv2.line(urat, (x0, y0), (x0 + 55, y0 + 70), 255, 1)
        cv2.line(urat, (x0, y0), (x0 - 35, y0 - 80), 255, 1)
    urat = cv2.bitwise_and(urat, daun)[..., None] / 255.0
    warna_daun = warna_daun * (1 - urat) + np.array([150, 195, 110]) * urat
    rgb = rgb * (1 - alfa) + warna_daun * alfa
    # Bercak gejala penyakit: radius 2 sampai 14 piksel, cokelat dengan halo kuning
    daftar = [(180, 270, 2), (230, 220, 3), (300, 280, 4), (360, 200, 6),
              (420, 250, 8), (470, 160, 11), (270, 180, 14)]
    bercak = np.zeros((h, w), np.uint8)
    for x, y, r in daftar:
        cv2.circle(rgb, (x, y), r + 2, (170, 170, 60), -1)
        cv2.circle(rgb, (x, y), r, (110, 70, 35), -1)
        cv2.circle(bercak, (x, y), r, 255, -1)
    bersih = np.clip(rgb + rng.normal(0, 2, rgb.shape), 0, 255)
    f = bersih / 255.0
    if kondisi == "teduh":
        f = f ** 2.2
    elif kondisi == "terik":
        f = np.clip(f ** 0.5 * 1.12, 0, 1)
        kilap = np.zeros((h, w), np.uint8)
        cv2.ellipse(kilap, (360, 300), (90, 22), -20, 0, 360, 255, -1)
        cv2.ellipse(kilap, (250, 200), (70, 16), -20, 0, 360, 255, -1)
        cv2.rectangle(kilap, (560, 0), (639, 70), 255, -1)
        f[kilap > 0] = 1.0
    elif kondisi == "kabut":
        f = 0.30 * f + 0.45
    elif kondisi == "bayangan":
        x = np.arange(w)[None, :] - (300 + 40 * np.sin(np.arange(h)[:, None] / 50))
        f = f * (0.30 + 0.75 / (1 + np.exp(-x / 8)))[..., None]
    elif kondisi == "iso":
        f = f ** 2.2 + rng.normal(0, 12 / 255, f.shape)
    elif kondisi == "rusak":
        u = rng.random((h, w))
        f[u < 0.015] = 0.0
        f[u > 0.985] = 1.0
    elif kondisi == "goyang":
        f = cv2.GaussianBlur(f, (0, 0), 2.0) + rng.normal(0, 2 / 255, f.shape)
    elif kondisi != "normal":
        raise ValueError("kondisi tidak dikenal: " + kondisi)
    citra = np.clip(np.round(f * 255), 0, 255).astype(np.uint8)
    info = {"bersih": cv2.cvtColor(bersih.astype(np.uint8), cv2.COLOR_RGB2BGR),
            "daun": daun, "bercak": bercak, "daftar_bercak": daftar}
    return cv2.cvtColor(citra, cv2.COLOR_RGB2BGR), info


def bercak_terlihat(citra, info, ambang=0.5):
    """Menghitung bercak yang masih tampak: pusat bercak tetap lebih gelap dari
    daun di sekitarnya minimal `ambang` kali kontras aslinya."""
    g = ke_abu(citra).astype(np.float32)
    b = ke_abu(info["bersih"]).astype(np.float32)
    hasil = []
    for x, y, r in info["daftar_bercak"]:
        cincin = np.zeros(g.shape, np.uint8)
        cv2.circle(cincin, (x, y), r + 10, 255, 4)
        kontras_awal = b[cincin > 0].mean() - b[y, x]
        kontras = g[cincin > 0].mean() - g[y, x]
        hasil.append(bool(kontras >= ambang * kontras_awal))
    return hasil
