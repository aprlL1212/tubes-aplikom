# 🏗️ Structura — Web-Based Structural Analysis

Aplikasi pembelajaran analisis **portal 2D** (balok & kolom) dengan **metode kekakuan matriks**, elastis linier statik.
> Hanya alat bantu belajar — bukan pengganti analisis dan verifikasi insinyur profesional.

## Menjalankan
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
python -m pytest -q          # uji terhadap solusi teoritis
```

## Struktur folder
```
app.py                    # antarmuka Streamlit (Dashboard, Beban Bergerak, Input, Analisis, Proyek, Laporan)
structura/moving_load.py  # modul beban bergerak & simulasi interaktif (animasi 60 FPS, SFD/BMD, garis pengaruh)
structura/engine.py       # mesin analisis: matriks kekakuan, solusi, reaksi, gaya dalam
structura/validation.py   # konversi tabel→model, validasi input
structura/plots.py        # visualisasi Plotly (model, deformasi, N/V/M)
structura/report.py       # laporan PDF (ReportLab)
structura/storage.py      # proyek di SQLite (structura.db; ganti dengan env STRUCTURA_DB)
structura/examples.py     # contoh soal
tests/test_engine.py      # verifikasi vs rumus teoritis
tests/test_moving_load.py # verifikasi analitis beban bergerak & integrasi matriks
```

## Fitur Unggulan
1. **🚚 Simulasi Beban Bergerak (Moving Load Simulation)**:
   - Visualisasi interaktif 60 FPS truk melintasi jembatan rangka (Warren truss) dengan tumpuan sendi & rol.
   - Reaksi tumpuan dinamis $R_1(x)$ dan $R_2(x)$ dengan panah gaya proporsional.
   - Grafik kurva momen bertumbuh (*A moving load. A growing graph*) $M(x) = \frac{P \cdot x \cdot (L - x)}{L}$ dengan puncak $M_{\max} = \frac{PL}{4}$ di tengah bentang.
   - Kartu perhitungan statika dinamis (*The load stays balanced*) dengan verifikasi keseimbangan $R_1 + R_2 = P$.
   - Kontrol pemutar video interaktif: Play/Pause, Scrubber timeline, step forward/backward, pengaturan kecepatan (0.5x, 1x, 1.5x, 2x), dan transkrip penjelasan.
   - Diagram gaya geser (SFD) & momen lentur (BMD) seketika serta selubung momen maksimum (*envelope*).
   - Analisis Garis Pengaruh (*Influence Line*) reaksi, gaya geser, dan momen pada sembarang potongan.
   - Integrasi 1-klik untuk mentransfer jembatan beban bergerak ke solver metode kekakuan langsung (*direct stiffness method*).
2. **🏗️ Analisis Portal 2D (Direct Stiffness Matrix Method)**:
   - Input berbasis tabel interaktif: node, elemen, tumpuan, beban titik buhul, dan beban elemen (UDL & terpusat).
   - Solusi deformasi elastis linier orde-1, diagram gaya aksial (N), geser (V), dan momen (M).
   - Ekspor laporan profesional siap cetak dalam format PDF.

## Satuan & konvensi
m, kN, kN·m; E dalam MPa; b, h dalam mm; perpindahan ditampilkan mm, rotasi rad.
Sumbu global x ke kanan, y ke atas. N tarik (+); V (+) bila gaya kiri-potongan ke atas pada sumbu lokal y; M sagging (+) dan digambar di sisi tarik.
Beban: Fx, Fy (+ ke kanan/atas), M (+ berlawanan jarum jam). Beban elemen: UDL atau titik; arah *Gravitasi* (ke bawah), *Lokal-y*, *Lokal-x*.

## Rumus
- Sistem: **K·u = F**, K = Σ Tᵀ·k·T. Reaksi **R = K·u − F** pada DOF tertahan.
- k lokal (3 DOF/node): EA/L; 12EI/L³; 6EI/L²; 4EI/L; 2EI/L. A = b·h; I = b·h³/12.
- Beban elemen → gaya ujung jepit f_e (UDL: wL/2, wL²/12; titik: Pb²(3a+b)/L³, Pab²/L², dst.), beban ekivalen = −Tᵀ·f_e.
- Gaya ujung: f = k·T·u_e + f_e. Gaya dalam dari keseimbangan potongan kiri:
  N(x) = −(f₁ + ∫pₓ); V(x) = f₂ + ∫p_y; M(x) = −m₁ + f₂·x + ∬p_y.
- Deformasi di dalam elemen: interpolasi Hermite kubik (nilai di node eksak; antar node pendekatan untuk beban merata).

## Asumsi & batasan
Elastis linier, perpindahan kecil (orde-1), Euler–Bernoulli (tanpa deformasi geser), sambungan kaku (tanpa sendi/release), tumpuan kaku (tanpa pegas/penurunan), penampang persegi, beban statik. Tidak ada kombinasi beban, P-Δ, atau desain penampang.

## Validasi & stabilitas
Cek: ID duplikat, referensi node, elemen nol, properti ≤ 0, node terisolasi, posisi `a` beban titik, minimal 3 reaksi. Ketidakstabilan (mekanisme) dideteksi lewat eigenvalue matriks kekakuan tereduksi ternormalisasi (λmin/λmaks ≤ 1e-10).

## Verifikasi (tests/test_engine.py)
Kantilever (δ=PL³/3EI, θ=PL²/2EI), balok sederhana UDL (δ=5wL⁴/384EI, Mmaks=wL²/8), jepit-jepit (wL²/12, wL²/24; Pab²/L²), lompatan geser beban titik, portal balok kaku (V=H/2, M=Hh/4), keseimbangan ΣF/ΣM pada contoh & elemen miring, deteksi struktur tidak stabil, penyimpanan SQLite dan pembuatan PDF.
