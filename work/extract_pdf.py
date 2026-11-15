import pymupdf, sys, json, os
def extract(pdf_path, out_txt, out_json):
    doc = pymupdf.open(pdf_path)
    pages = []
    chunks = []
    empty = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        n_img = len(page.get_images(full=True))
        n_draw = len(page.get_drawings())
        rec = {"page": i+1, "chars": len(text.strip()), "images": n_img, "drawings": n_draw}
        pages.append(rec)
        if len(text.strip()) < 20:
            empty.append(i+1)
        chunks.append(f"\n===== [PAGE {i+1}] =====\n{text}")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"# SOURCE FILE: {os.path.basename(pdf_path)}\n# PAGES: {len(doc)}\n" + "".join(chunks))
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"pdf": os.path.basename(pdf_path), "page_count": len(doc), "pages": pages, "low_text_pages": empty}, f, indent=2)
    print(os.path.basename(pdf_path), "pages=", len(doc), "chars=", sum(p['chars'] for p in pages), "low_text_pages=", empty)
    print("  first-page sample:", pages[0])
root = os.getcwd()
extract(os.path.join(root, "CS477 - Assignment_2.pdf"), "work/extracted/assignment_text.txt", "work/extracted/assignment_pages.json")
extract(os.path.join(root, "CS477 (6-13).pdf"), "work/extracted/slides_text.txt", "work/extracted/slides_pages.json")
