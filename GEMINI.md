# 프로젝트 가이드 (GEMINI.md)

## 기술 스택
- Python 3.x
- PyMuPDF (fitz)
- Pandas

## 작업 규칙
- 모든 코드는 `src/` 폴더 내에 위치시킨다.
- 학생 명단 샘플은 `data/students.csv`에 저장한다.
- 생성된 결과물은 `output/` 폴더에 저장하며, Git 관리에서 제외한다.

## 설계안
(이전 설계안 내용 포함)
1. PDF 좌표 분석을 통해 이름/학번 위치 파악
2. 텍스트 오버레이 기능을 사용하여 새로운 PDF 생성
