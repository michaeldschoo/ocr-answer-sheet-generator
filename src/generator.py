import fitz
import pandas as pd
import os

def generate_answer_sheets(template_path, student_csv, output_dir):
    """
    학생 명단을 기반으로 OCR 답안지 PDF를 생성하고 OMR 버블을 마킹합니다.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 학생 데이터 로드
    try:
        students = pd.read_csv(student_csv)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # 좌표 설정 (분석 결과 기반)
    Y_ROWS = [236, 250, 263, 277, 291, 303, 317, 331, 345, 358]
    
    # Grade Column
    X_GRADE = 48.8
    
    # Student ID Columns (5 digits)
    X_SID = [71.1, 103.3, 125.4, 147.6, 169.8]
    
    # Centre ID Columns (3 digits)
    X_CID = [225.6, 248.0, 270.5]

    for index, row in students.iterrows():
        full_sid_cid = str(row['student_id']) # 형식: "12345-113"
        name = row['name']
        grade = str(row['grade'])
        
        # ID 분리
        if '-' in full_sid_cid:
            sid_str, cid_str = full_sid_cid.split('-')
        else:
            sid_str = full_sid_cid[:5]
            cid_str = full_sid_cid[5:8]
            
        # 이름 분리
        parts = name.split()
        given_name = parts[0] if len(parts) > 0 else ""
        surname = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        # 템플릿 열기
        doc = fitz.open(template_path)
        page = doc[0]
        
        # 1. 텍스트 기입
        page.insert_text((120, 115), given_name, fontsize=11, color=(0, 0, 0))
        page.insert_text((120, 135), surname, fontsize=11, color=(0, 0, 0))
        page.insert_text((120, 155), grade, fontsize=11, color=(0, 0, 0))
        
        # 2. OMR 마킹 (버블 채우기)
        def mark_bubble(x, digit):
            try:
                d = int(digit)
                if 0 <= d <= 9:
                    center = fitz.Point(x, Y_ROWS[d])
                    # 작은 원을 그려서 버블을 채움
                    page.draw_circle(center, 4, color=(0, 0, 0), fill=(0, 0, 0))
            except ValueError:
                pass

        # Grade 마킹
        mark_bubble(X_GRADE, grade)
        
        # Student ID 마킹 (5자리)
        for i, digit in enumerate(sid_str[:5]):
            mark_bubble(X_SID[i], digit)
            
        # Centre ID 마킹 (3자리)
        for i, digit in enumerate(cid_str[:3]):
            mark_bubble(X_CID[i], digit)
            
        # 결과 저장
        output_filename = f"{sid_str}_{name.replace(' ', '_')}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        doc.save(output_path)
        doc.close()
        
        print(f"[{index+1}/{len(students)}] 생성 완료: {output_path}")

if __name__ == "__main__":
    TEMPLATE = "ANS 4 Choices.pdf"
    STUDENTS_CSV = "data/students_list.csv"
    OUTPUT_DIR = "output"
    
    generate_answer_sheets(TEMPLATE, STUDENTS_CSV, OUTPUT_DIR)
