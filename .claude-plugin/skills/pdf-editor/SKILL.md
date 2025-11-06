---
name: pdf-editor
description: This skill should be used when users want to edit PDFs by rotating pages, replacing links/text (such as updating old wiki URLs to new ones), and adding company branding images to footers. Ideal for fixing legacy documents with outdated links or correcting page orientation issues.
---

# PDF Editor Skill

## Overview

This skill enables editing and fixing PDFs through page rotation, link/URL replacement, and footer branding. It's designed to help fix legacy documents—particularly those that were OCR'd or printed with outdated internal links—by automatically updating URLs and adding company branding in one operation.

## When to Use This Skill

Use this skill when:
- Fixing old documents with outdated internal links (e.g., `team-wiki.local` → `team-wiki.etc.com`)
- Correcting page orientation issues (pages scanned sideways or rotated incorrectly)
- Adding company branding (logo/SVG) to document footers consistently across all pages
- Processing batches of legacy articles or printed documents
- Combining any of the above operations in a single "fix" operation

**Example user queries that trigger this skill:**
- "Fix this PDF - rotate page 3 and update all wiki links"
- "Update the old wiki links in this document and add our company footer"
- "Make sure this PDF is oriented correctly, has updated links, and includes our branding"

## Quick Start

When a user provides a PDF for editing, follow this process:

1. **Understand the requirements** - Ask which operations are needed:
   - Page rotation? (and which pages + angles)
   - Link replacement? (typically `team-wiki.local` → `team-wiki.etc.com`)
   - Footer branding? (use the provided SVG from `assets/footer_logo.svg`)

2. **Prepare the input** - Confirm you have:
   - The PDF file to edit
   - Any custom logo/SVG for footer (or use the placeholder)
   - Page numbers and rotation angles if needed

3. **Execute the edit** - Use the `scripts/pdf_editor.py` script with appropriate flags:
   ```bash
   python scripts/pdf_editor.py \
     --input document.pdf \
     --output fixed_document.pdf \
     --rotate "3:90" \
     --replace-url "team-wiki.local" "team-wiki.etc.com" \
     --footer-image assets/footer_logo.svg
   ```

4. **Verify and deliver** - Check the output PDF and provide it to the user

## Core Operations

### 1. Rotate Pages

Rotate specific pages by specifying page number and angle (in degrees).

**Arguments:**
- `--rotate "page:angle,page:angle"` - e.g., `"1:90,3:180"`
- Page numbers are 1-indexed (first page is 1)
- Common angles: 90 (quarter turn), 180 (flip), 270 (three-quarter turn)

**Example:**
```bash
python scripts/pdf_editor.py \
  --input document.pdf \
  --output rotated.pdf \
  --rotate "2:90,5:180"
```

### 2. Replace Links/URLs

Replace all instances of old text/URLs with new ones throughout the PDF. This is useful for updating internal wiki links or fixing broken references.

**Arguments:**
- `--replace-url "OLD_TEXT" "NEW_TEXT"` - replaces all occurrences
- Replacement is automatic and affects all instances in the document
- Common example: `"team-wiki.local" "team-wiki.etc.com"`

**Example:**
```bash
python scripts/pdf_editor.py \
  --input document.pdf \
  --output updated.pdf \
  --replace-url "team-wiki.local" "team-wiki.etc.com"
```

**Limitations:** This operation modifies text streams in the PDF. Some PDFs (especially scanned or heavily OCR'd documents) may have text rendered as images, which cannot be modified with this approach. If text replacement doesn't work, the PDF may need to be regenerated.

### 3. Add Footer Image

Add a company logo or branding image to the footer of all pages. This maintains consistent branding across documents.

**Arguments:**
- `--footer-image path/to/image.svg` - supports SVG, PNG, JPG
- Image is positioned 50 points from the right edge, 30 points from the bottom
- Default size: 30x30 points

**Example:**
```bash
python scripts/pdf_editor.py \
  --input document.pdf \
  --output branded.pdf \
  --footer-image assets/footer_logo.svg
```

**Default Footer SVG:** Use `assets/footer_logo.svg` included with this skill—a placeholder company logo that can be replaced with your actual SVG or image.

### 4. Combine Operations

All three operations can be performed in a single command:

```bash
python scripts/pdf_editor.py \
  --input old_document.pdf \
  --output fixed_document.pdf \
  --rotate "3:90" \
  --replace-url "team-wiki.local" "team-wiki.etc.com" \
  --footer-image assets/footer_logo.svg
```

## Common Workflows

### Fix a Legacy Document ("Fix This PDF")

User provides a document that needs comprehensive updating:

1. Ask user: "Does this document need any page rotation? If so, which pages and in what direction?"
2. Ask user: "Should I update the wiki links from `team-wiki.local` to `team-wiki.etc.com`?"
3. Ask user: "Should I add company branding to the footer?"
4. Execute all operations as a single command
5. Deliver the fixed PDF

### Batch Processing

To process multiple PDFs with the same edits, repeat the script execution for each file with identical parameters.

## Dependencies

The `scripts/pdf_editor.py` script requires:
- **PyPDF2** - PDF manipulation (page rotation, text replacement)
- **reportlab** - Adding footer images

Install with:
```bash
pip install PyPDF2 reportlab
```

**Optional for SVG support:**
- **svglib** - For better SVG rendering (install if needed: `pip install svglib`)

## Customization

### Replace the Footer Logo

To use a custom company logo instead of the placeholder:

1. Prepare your SVG/PNG/JPG file
2. Replace `assets/footer_logo.svg` with your logo
3. Use the same command: `--footer-image assets/footer_logo.svg`

Alternatively, specify any image file directly: `--footer-image /path/to/custom/logo.svg`

### Adjust Footer Position/Size

To modify footer positioning, edit `scripts/pdf_editor.py` function `add_footer_image()`:

```python
footer_x = page_width_pts - 50     # Distance from right edge
footer_y = 30                       # Distance from bottom
image_size = 30                     # Width/height in points
```

## Troubleshooting

**Text replacement isn't working:**
- The PDF may have text rendered as images (especially in scanned/OCR'd documents)
- Try verifying if you can select and copy text in a PDF viewer
- If text isn't selectable, it's rendered as an image and cannot be modified with this script

**Footer image isn't appearing:**
- Ensure the image file path is correct
- Check that the image format is supported (SVG, PNG, JPG)
- Verify the footer_y value isn't positioning the image outside the page bounds

**Page rotation isn't working:**
- Double-check page numbers are 1-indexed (first page = 1, not 0)
- Verify page numbers exist in the PDF
- Try rotating a different page to test

## Resources

### scripts/
- `pdf_editor.py` - Main PDF editing utility with rotation, text replacement, and footer image operations

### assets/
- `footer_logo.svg` - Placeholder company logo for footer branding (replace with your actual logo)

### references/
- `api_reference.md` - Detailed API documentation for PDF editing libraries used (PyPDF2, reportlab)
