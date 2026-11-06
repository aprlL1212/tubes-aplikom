"""Entry point deployment untuk aplikasi Structura."""

from pathlib import Path
import runpy


# Jalankan UI utama sebagai script Streamlit, bukan hanya sebagai modul impor.
# Ini membuat entry point deployment konsisten saat dijalankan dari folder lain.
runpy.run_path(str(Path(__file__).with_name("app.py")), run_name="__main__")
