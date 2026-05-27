import fitz

def analyze_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    print(f"Page size: {page.rect}")
    
    # Extract text and their coordinates
    text_instances = page.get_text("dict")["blocks"]
    for block in text_instances:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    print(f"Text: '{span['text']}' at {span['bbox']}")

    doc.close()

if __name__ == "__main__":
    analyze_pdf("ANS 4 Choices.pdf")
