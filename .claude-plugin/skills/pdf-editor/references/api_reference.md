# PDF Editor API Reference

This document provides detailed API documentation for the libraries used in the PDF editor skill.

## PyPDF2 - PDF Manipulation

PyPDF2 is a Python library for reading and writing PDF files. It's used for page rotation and text replacement operations.

**Installation:**
```bash
pip install PyPDF2
```

**Key Classes:**

### PdfReader
Reads PDF files and provides access to pages and content.

```python
from PyPDF2 import PdfReader

reader = PdfReader("document.pdf")
pages = reader.pages
for page in pages:
    print(page["/MediaBox"])  # Get page dimensions
```

**Common Attributes:**
- `pages` - List of all pages in the PDF
- `metadata` - Document metadata (title, author, etc.)

### PdfWriter
Creates new PDFs and merges/modifies pages.

```python
from PyPDF2 import PdfWriter

writer = PdfWriter()
writer.add_page(page)
with open("output.pdf", "wb") as f:
    writer.write(f)
```

**Common Methods:**
- `add_page(page)` - Add a page to the PDF
- `write(file)` - Write PDF to file

### Page Rotation

Rotate a page in-place:

```python
page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
```

**Rotation angles:**
- `90` - Quarter turn (clockwise)
- `180` - Half turn (upside down)
- `270` - Three-quarter turn (clockwise)
- `360` or `0` - No rotation

### Text Stream Modification

Access and modify page content streams for text replacement:

```python
page = reader.pages[0]
if page["/Contents"] is not None:
    content = page["/Contents"].get_object().get_data()

    # Replace text
    modified = content.replace(b"old_text", b"new_text")
    page["/Contents"].get_object().set_data(modified)
```

**Limitations:**
- Only works with text that's stored as text streams (not rendered as images)
- Character encoding may affect replacement accuracy
- OCR'd PDFs often have text as images and cannot be modified this way

## ReportLab - PDF Generation & Image Insertion

ReportLab is used to generate new PDF elements (like footers) and overlay them on existing pages.

**Installation:**
```bash
pip install reportlab
```

### Canvas
The Canvas class is used to draw graphics, text, and images.

```python
from reportlab.pdfgen import canvas
from io import BytesIO

buffer = BytesIO()
c = canvas.Canvas(buffer, pagesize=(8.5 * 72, 11 * 72))  # Letter size
c.drawString(100, 750, "Hello World")
c.drawImage("image.png", 100, 100, width=100, height=100)
c.save()
```

**Key Methods:**
- `drawString(x, y, text)` - Draw text at coordinates
- `drawImage(filename, x, y, width, height)` - Draw an image
- `drawRect(x, y, width, height)` - Draw a rectangle
- `save()` - Finalize and save the canvas

### Page Merging

Merge a footer canvas onto an existing page:

```python
from PyPDF2 import PdfReader

footer_reader = PdfReader(footer_buffer)
footer_page = footer_reader.pages[0]

# Merge footer onto main page
main_page.merge_page(footer_page)
```

### Coordinate System

ReportLab uses points (1/72 inch) with origin at bottom-left:

```python
# For a standard letter-size page (8.5" x 11"):
width_points = 8.5 * 72  # 612 points
height_points = 11 * 72   # 792 points

# Position 50 points from right, 30 points from bottom:
x = width_points - 50
y = 30
```

## Common Workflows

### Rotating Specific Pages

```python
from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

rotations = {1: 90, 3: 180}  # Rotate page 1 by 90°, page 3 by 180°

for i, page in enumerate(reader.pages, 1):
    if i in rotations:
        page.rotate(rotations[i])
    writer.add_page(page)

with open("output.pdf", "wb") as f:
    writer.write(f)
```

### Adding a Footer Image to All Pages

```python
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)

    # Create footer
    footer_buffer = BytesIO()
    c = canvas.Canvas(footer_buffer, pagesize=(width, height))
    c.drawImage("logo.svg", width - 50, 30, width=30, height=30)
    c.save()

    # Merge footer
    footer_buffer.seek(0)
    footer_reader = PdfReader(footer_buffer)
    page.merge_page(footer_reader.pages[0])
    writer.add_page(page)

with open("output.pdf", "wb") as f:
    writer.write(f)
```

### Replacing Text in PDF

```python
from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    if page["/Contents"] is not None:
        content = page["/Contents"].get_object().get_data()
        modified = content.replace(b"old_wiki", b"new_wiki")
        page["/Contents"].get_object().set_data(modified)

    writer.add_page(page)

with open("output.pdf", "wb") as f:
    writer.write(f)
```

## Troubleshooting

### "Module not found" errors
Install missing dependencies:
```bash
pip install PyPDF2 reportlab
```

### Text replacement not working
- Check if text is selectable in a PDF viewer
- If not selectable, it's rendered as an image (OCR or scanned PDF)
- These cannot be modified with text stream replacement

### Image doesn't appear in output
- Verify image path is correct and file exists
- Check that reportlab can handle the image format
- For SVG: May need additional library `svglib`

### Page dimensions issues
- PDFs may have different page sizes on different pages
- Use `page.mediabox` to get individual page dimensions
- Calculate positions relative to actual page size, not assumed standard size
