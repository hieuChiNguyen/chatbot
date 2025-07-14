""""
    Khi xử lý file PDF, cần phân biệt hai trường hợp phổ biến:

    * PDF not scan: Sử dụng thư viện fitz / PyMuPDF để trích xuất trực tiếp nội dung văn bản được nhúng trong file
    * PDF scan: Tiến hành chuyển từng trang PDF thành ảnh, sau đó áp dụng OCR để trích xuất văn bản, theo quy trình đã mô tả ở bước trước
"""

import io
import fitz  # PyMuPDF
from pdf2image import convert_from_path  # Sử dụng convert_from_path thay vì convert_from_bytes
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor
from PIL import Image


# Khởi tạo các predictor cho OCR
def initialize_ocr_predictors(device: str="cpu"):
    """Khởi tạo các predictor của Surya OCR."""
    recognition_predictor = RecognitionPredictor(device=device)
    detection_predictor = DetectionPredictor(device=device)
    return recognition_predictor, detection_predictor


# Hàm trích xuất văn bản từ ảnh bằng OCR
def get_full_text(recognition_predictor, detection_predictor, image_bytes):
    """
    Trích xuất văn bản từ ảnh bằng Surya OCR.
    - Input: image_bytes (bytes), langs (danh sách ngôn ngữ)
    - Output: Văn bản trích xuất dưới dạng chuỗi
    """

    image = Image.open(io.BytesIO(image_bytes))
    predictions = recognition_predictor([image], ["ocr_with_boxes"], detection_predictor)
    predictions_text_lines = predictions[0].text_lines
    full_text = "\n".join(line.text for line in predictions_text_lines)
    return full_text


# Hàm kiểm tra xem một trang có phải là trang scan không
def is_scanned_page(page):
    """
    Kiểm tra xem một trang PDF có phải là trang scan không.
    - Input: page (fitz.Page)
    - Output: True nếu là trang scan, False nếu không
    """
    text = page.get_text().strip()
    has_meaningful_text = bool(text and any(c.isalpha() for c in text))
    fonts = page.get_fonts()
    has_fonts = bool(fonts)

    images = page.get_image_info(hashes=True)
    page_area = page.rect.width * page.rect.height
    image_area = sum(img['width'] * img['height'] for img in images)
    image_ratio = image_area / page_area if page_area > 0 else 0

    if not has_meaningful_text and not has_fonts and image_ratio > 0.8:
        return True
    if not has_meaningful_text and image_ratio > 0.5:
        return True
    return False


# Hàm chính để xử lý file PDF
def parse_pdf_file(file_path: str):
    """
    Xử lý file PDF và trích xuất văn bản từ từng trang.
    - PDF không scan: Trích xuất trực tiếp bằng PyMuPDF.
    - PDF scan: Chuyển thành ảnh và dùng OCR để trích xuất văn bản.
    - Input: file_path (đường dẫn file), device (thiết bị chạy OCR), langs (danh sách ngôn ngữ)
    - Output: Danh sách các chuỗi văn bản, mỗi chuỗi là nội dung của một trang
    """
    # Mở file PDF một lần
    doc = fitz.open(file_path)
    full_text = []
    recognition_predictor, detection_predictor = None, None

    # Duyệt qua từng trang
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        scanned_page = is_scanned_page(page)
        print(page_num+1, scanned_page)

        if scanned_page:
            # Trang scan: Khởi tạo predictor nếu chưa có và áp dụng OCR
            if recognition_predictor is None:
                recognition_predictor, detection_predictor = initialize_ocr_predictors()

            # Chuyển trang hiện tại thành ảnh
            images = convert_from_path(file_path, dpi=300, fmt="png", first_page=page_num + 1, last_page=page_num + 1, thread_count=1)
            image = images[0]
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            image_data = image_bytes.read()
            ocr_text = get_full_text(recognition_predictor, detection_predictor, image_data)
            full_text.append(ocr_text)
        else:
            # Trang không scan: Trích xuất trực tiếp
            full_text.append(text)

    # Đóng document
    doc.close()
    return full_text


# Run script
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <pdf_path>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    texts = parse_pdf_file(pdf_path)
    for i, text in enumerate(texts):
        print(f"Trang {i + 1}:\n{text}\n")
