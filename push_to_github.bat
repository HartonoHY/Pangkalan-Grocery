@echo off
echo ======================================================================
echo   PENYIAPAN DEPLOY GROCERY SALES DWH DASHBOARD KE GITHUB & STREAMLIT
echo ======================================================================
echo.
echo Langkah 1: Buat repository baru di GitHub (https://github.com/new)
echo            Beri nama, misalnya: grocery-sales-dashboard
echo            (Biarkan kosong tanpa README/license)
echo.
set /p REPO_URL="Masukkan URL Repository GitHub Anda (contoh: https://github.com/username/repo.git): "

if "%REPO_URL%"=="" (
    echo [ERROR] URL repository tidak boleh kosong!
    pause
    exit /b
)

echo.
echo [1/3] Menghubungkan remote GitHub...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [2/3] Mengirim (push) data dashboard ke GitHub...
git branch -M main
git push -u origin main

echo.
echo ======================================================================
echo   [SUKSES] KODE DASHBOARD TELAH BERADA DI GITHUB!
echo ======================================================================
echo Langkah Terakhir (Deploy 24/7):
echo 1. Buka: https://share.streamlit.io
echo 2. Login menggunakan akun GitHub Anda
echo 3. Klik tombol "New app"
echo 4. Pilih repository tadi, Main file path: app.py
echo 5. Klik "Deploy!"
echo.
echo Dashboard Anda akan aktif 24 jam nonstop di internet!
pause
