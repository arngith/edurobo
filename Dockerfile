# Menggunakan image Python yang ringan
#FROM python:3.11-slim
# Menyiapkan folder kerja di dalam container
#WORKDIR /app
# Menyalin file requirements dan menginstalnya
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
# Menyalin semua kode kita ke dalam container
#COPY . .
# Membuka port 5000
#EXPOSE 5000

# Menjalankan aplikasi
#CMD ["python", "app.py"]

# Gunakan image Python ringan
FROM python:3.11-slim

# Hugging Face merekomendasikan membuat user dengan ID 1000
RUN useradd -m -u 1000 user

# Pindah menggunakan user tersebut
USER user

# Atur environment variable untuk direktori
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Pindah ke dalam folder kerja user
WORKDIR $HOME/app

# Salin semua file dari komputer Anda ke dalam container (dengan hak milik user)
COPY --chown=user . $HOME/app

# Install library Python dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Buka port 7860 (WAJIB untuk Hugging Face)
EXPOSE 7860

# Jalankan aplikasi
CMD ["python", "app.py"]

