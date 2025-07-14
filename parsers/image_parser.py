import io
import os

from PIL import Image
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor


class TextExtractorFromImage:
    def __init__(self, device="cpu"):
        self.recognition_predictor = RecognitionPredictor(device=device)
        self.detection_predictor = DetectionPredictor(device=device)

    def get_full_text(self, image_bytes):
        """
        Input:
            - Use Surya to detect text in the image
            - Join all detected text segments into a single string, separated by "\n"
        Output:
            - Return a list containing one element: the concatenated text string
        """
        if isinstance(image_bytes, io.BytesIO):
            image_bytes = image_bytes.getvalue()

        image = Image.open(io.BytesIO(image_bytes))
        predictions = self.recognition_predictor([image],["ocr_with_boxes"], self.detection_predictor)
        predictions_text_lines = predictions[0].text_lines
        full_text = "\n".join(line.text for line in predictions_text_lines)
        return full_text

    def parse_img_file(self, file_path):
        def process_image_file(path):
            if isinstance(path, str) and os.path.exists(path):
                with open(path, "rb") as f:
                    return f.read()
            return

        image_bytes = process_image_file(file_path)
        if image_bytes is None:
            return ["Error: File not found or invalid path"]

        return [self.get_full_text(image_bytes)]


# if __name__ == "__main__":
#     image_path = "data/a.jpg"
#     try:
#         # Khởi tạo TextExtractor
#         extractor = TextExtractor(device="cpu")
#
#         # Trích xuất văn bản từ file ảnh
#         result = extractor.parse_img_file(image_path)
#
#         print(f"Kết quả trích xuất văn bản từ {image_path}:")
#         for i, text in enumerate(result, 1):
#             print(f"\nVăn bản trích xuất (Phần {i}):\n{text}")
#     except Exception as e:
#         print(f"Lỗi khi xử lý file: {e}")
