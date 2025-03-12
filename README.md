# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis **Bike Sharing Dataset** untuk menjawab pertanyaan bisnis berikut:

1. **Pada jam berapa penyewaan sepeda paling banyak dan paling sedikit terjadi?**
2. **Pada musim apa penyewaan sepeda paling banyak terjadi?**

Analisis dilakukan dalam Jupyter Notebook `Proyek_Analisis_Data.ipynb`, dan hasilnya disajikan dalam bentuk dashboard interaktif menggunakan **Streamlit**.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
---

## Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.10
conda activate main-ds
pip install -r requirements.txt

## Setup Environment - Shell/Terminal

mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

## Menjalankan Aplikasi Streamlit

streamlit run dashboard/dashboard.py

submission/
├── Proyek_Analisis_Data.ipynb
├── README.md
├── dashboard/
│   └── dashboard.py
├── data/
│   ├── day.csv
│   └── hour.csv
├── requirements.txt
└── url.txt(url hosting streamlit)

