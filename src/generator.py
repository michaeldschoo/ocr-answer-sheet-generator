import fitz
import pandas as pd
import os

def generate_answer_sheets(template_path, student_csv, output_dir):
    """
    학생 명단을 기반으로 OCR 답안지 PDF를 생성합니다.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 학생 데이터 로드
    try:
        students = pd.read_csv(student_csv)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    for index, row in students.iterrows():
        sid = str(row['student_id'])
        name = row['name']
        
        # 이름 분리 (간단히 첫 단어를 Given Name, 나머지를 Surname으로 간주)
        parts = name.split()
        given_name = parts[0] if len(parts) > 0 else ""
        surname = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        # 템플릿 열기
        doc = fitz.open(template_path)
        page = doc[0]
        
        # 텍스트 삽입 좌표 (분석 결과 기반 예상치)
        # GIVEN NAME: Y=113 부근
        # SURNAME: Y=132 부근
        # STUDENT ID: Y=196 부근
        
        # Given Name 삽입
        page.insert_text((120, 115), given_name, fontsize=11, color=(0, 0, 0))
        
        # Surname 삽입
        page.insert_text((120, 135), surname, fontsize=11, color=(0, 0, 0))
        
        # Student ID 삽입
        page.insert_text((185, 200), sid, fontsize=11, color=(0, 0, 0))
        
        # 결과 저장
        output_filename = f"{sid}_{name.replace(' ', '_')}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        doc.save(output_path)
        doc.close()
        
        print(f"[{index+1}/{len(students)}] 생성 완료: {output_path}")

if __name__ == "__main__":
    TEMPLATE = "ANS 4 Choices.pdf"
    STUDENTS_CSV = "data/students.csv"
    OUTPUT_DIR = "output"
    
    generate_answer_sheets(TEMPLATE, STUDENTS_CSV, OUTPUT_DIR)
