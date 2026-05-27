import fitz

def create_grid_overlay(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    page = doc[0]
    
    # Draw horizontal lines
    for y in range(0, int(page.rect.height), 20):
        page.draw_line(fitz.Point(0, y), fitz.Point(page.rect.width, y), color=(1, 0, 0), width=0.5)
        page.insert_text(fitz.Point(5, y-2), str(y), fontsize=8, color=(1, 0, 0))
        
    # Draw vertical lines
    for x in range(0, int(page.rect.width), 20):
        page.draw_line(fitz.Point(x, 0), fitz.Point(x, page.rect.height), color=(0, 0, 1), width=0.5)
        page.insert_text(fitz.Point(x+2, 10), str(x), fontsize=8, color=(0, 0, 1))

    doc.save(output_pdf)
    doc.close()

if __name__ == "__main__":
    create_grid_overlay("ANS 4 Choices.pdf", "output/grid_overlay.pdf")
    print("Grid overlay created at output/grid_overlay.pdf")
