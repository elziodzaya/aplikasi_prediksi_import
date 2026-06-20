from fpdf import FPDF
from io import BytesIO
from datetime import datetime


class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(
            0, 10,
            "Laporan Sistem Pendukung Keputusan Impor",
            ln=True,
            align="C"
        )
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(
            0, 10,
            f"Halaman {self.page_no()}",
            align="C"
        )


def export_summary_pdf(
    title: str,
    metrics: dict,
    conclusion: str,
    method_summary: str = None
):
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # =========================
    # JUDUL
    # =========================
    pdf.set_font("Arial", "B", 14)
    pdf.multi_cell(0, 10, title, align="C")
    pdf.ln(3)

    pdf.set_font("Arial", "", 10)
    pdf.cell(
        0, 8,
        f"Tanggal Laporan: {datetime.now().strftime('%d %B %Y')}",
        ln=True,
        align="C"
    )
    pdf.ln(5)

    # =========================
    # RINGKASAN EKSEKUTIF
    # =========================
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "1. Ringkasan Eksekutif", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(
        0, 7,
        "Laporan ini menyajikan hasil analisis sistem pendukung keputusan impor "
        "yang mengintegrasikan metode Fuzzy Logic dan Dynamic Programming (DP). "
        "Pendekatan ini digunakan untuk menentukan kebijakan impor yang optimal "
        "dengan mempertimbangkan permintaan pasar, stok, kapasitas produksi, "
        "serta biaya impor dan biaya penyimpanan."
    )
    pdf.ln(3)

    # =========================
    # METODOLOGI
    # =========================
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "2. Metodologi", ln=True)
    pdf.set_font("Arial", "", 11)

    if method_summary:
        pdf.multi_cell(0, 7, method_summary)
    else:
        pdf.multi_cell(
            0, 7,
            "Metode penelitian terdiri dari dua tahap utama. "
            "Tahap pertama menggunakan sistem Fuzzy untuk memprediksi "
            "kebutuhan impor bulanan berdasarkan kondisi permintaan dan stok. "
            "Tahap kedua menggunakan Dynamic Programming untuk mengoptimalkan "
            "keputusan impor dengan tujuan meminimalkan total biaya sistem."
        )
    pdf.ln(3)

    # =========================
    # KPI
    # =========================
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "3. Ringkasan Kinerja Sistem", ln=True)
    pdf.set_font("Arial", "", 11)

    for key, value in metrics.items():
        pdf.cell(0, 7, f"- {key}: {value}", ln=True)

    pdf.ln(3)

    # =========================
    # KESIMPULAN
    # =========================
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "4. Kesimpulan", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, conclusion)

    # =========================
    # EXPORT KE BYTES
    # =========================
    buffer = BytesIO()
    pdf_output = pdf.output(dest="S")

    if isinstance(pdf_output, (bytes, bytearray)):
        buffer.write(pdf_output)
    else:
        buffer.write(pdf_output.encode("latin-1"))

    buffer.seek(0)
    return buffer
