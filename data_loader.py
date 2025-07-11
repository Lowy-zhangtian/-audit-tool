# data_processing/data_loader.py
import os
import pandas as pd
import PyPDF2

class DataLoader:
    def __init__(self):
        pass

    def load_structured_data(self, file_path):
        """Loads structured data (e.g., CSV, Excel) from various sources like ERP or audit reports."""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format for structured data.")
            print(f"Successfully loaded structured data from: {file_path}")
            return df
        except Exception as e:
            print(f"Error loading structured data from {file_path}: {e}")
            return None

    def load_image_data(self, image_path):
        """Loads image data (e.g., scanned vouchers). Placeholder for actual image loading."""
        # In a real application, this would use a library like Pillow (PIL)
        try:
            # Example: from PIL import Image; img = Image.open(image_path)
            print(f"Simulating loading image data from: {image_path}")
            # For now, just return the path as a placeholder
            return image_path
        except Exception as e:
            print(f"Error loading image data from {image_path}: {e}")
            return None

    def load_document_data(self, doc_path):
        """Loads document data (e.g., PDF attachments) and extracts text content."""
        import signal
        import time
        
        def timeout_handler(signum, frame):
            raise TimeoutError("PDF处理超时")
        
        try:
            if doc_path.lower().endswith('.pdf'):
                # 检查文件大小
                file_size = os.path.getsize(doc_path) / (1024 * 1024)  # MB
                print(f"Processing PDF: {doc_path} (Size: {file_size:.1f}MB)")
                
                # 对于大文件设置超时
                timeout_seconds = min(60, max(10, int(file_size * 2)))  # 根据文件大小动态设置超时
                
                # 设置超时处理（仅在非Windows系统上）
                if os.name != 'nt':  # 非Windows系统
                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(timeout_seconds)
                
                start_time = time.time()
                
                with open(doc_path, 'rb') as file:
                    try:
                        reader = PyPDF2.PdfReader(file)
                        total_pages = len(reader.pages)
                        
                        # 限制处理页数以避免超长处理时间
                        max_pages = min(total_pages, 100)  # 最多处理100页
                        
                        text = ''
                        for page_num in range(max_pages):
                            # 检查处理时间
                            if time.time() - start_time > timeout_seconds:
                                print(f"PDF处理超时，已处理 {page_num} 页")
                                break
                                
                            try:
                                page_text = reader.pages[page_num].extract_text() or ''
                                text += page_text
                                
                                # 每10页输出一次进度
                                if (page_num + 1) % 10 == 0:
                                    print(f"已处理 {page_num + 1}/{max_pages} 页")
                                    
                            except Exception as page_error:
                                print(f"处理第 {page_num + 1} 页时出错: {page_error}")
                                continue
                        
                        if total_pages > max_pages:
                            text += f"\n\n[注意: 文档共{total_pages}页，仅处理了前{max_pages}页]"
                            
                    except Exception as pdf_error:
                        if os.name != 'nt':
                            signal.alarm(0)  # 取消超时
                        raise pdf_error
                
                if os.name != 'nt':
                    signal.alarm(0)  # 取消超时
                    
                processing_time = time.time() - start_time
                print(f"Successfully extracted text from PDF: {doc_path} (处理时间: {processing_time:.1f}秒)")
                
                if not text.strip():
                    print(f"警告: PDF文件 {doc_path} 可能是扫描版本，无法提取文本")
                    return "[PDF文件无法提取文本内容，可能需要OCR处理]"
                    
                return text
            else:
                # For other document types, just return the path for now or raise an error
                print(f"Simulating loading document data from: {doc_path} (unsupported format for text extraction)")
                return doc_path
                
        except TimeoutError as te:
            print(f"PDF处理超时: {doc_path} - {te}")
            return f"[PDF处理超时: {os.path.basename(doc_path)}]"
        except Exception as e:
            print(f"Error loading document data from {doc_path}: {e}")
            return None

if __name__ == '__main__':
    loader = DataLoader()
    # Example usage (assuming you have dummy files)
    # Create dummy files for testing if they don't exist
    try:
        with open("dummy_structured_data.csv", "w") as f:
            f.write("报告编号,报告类型,被审计单位\nAR202501,年度审计报告,ABC公司")
        structured_data = loader.load_structured_data("dummy_structured_data.csv")
        if structured_data is not None:
            print("Structured Data:")
            print(structured_data.head())

        # Create a dummy PDF file for testing
        # This requires a more complex setup or a pre-existing PDF
        # For now, we'll just simulate the path
        # You can replace this with a path to a real PDF for testing
        dummy_pdf_path = "dummy_audit_report.pdf"
        # If you want to create a real dummy PDF for testing PyPDF2, you'd need a library like reportlab
        # from reportlab.pdfgen import canvas
        # c = canvas.Canvas(dummy_pdf_path)
        # c.drawString(100, 750, "This is a dummy audit report.")
        # c.save()

        doc_content = loader.load_document_data(dummy_pdf_path)
        if doc_content is not None:
            print("Document Content (first 200 chars):")
            print(str(doc_content)[:200])

        # Simulate image and document loading
        # You would replace these with actual paths to image/document files
        img_data = loader.load_image_data("dummy_voucher.png")
        doc_data = loader.load_document_data("dummy_attachment.pdf")

    except Exception as e:
        print(f"Error in example usage: {e}")