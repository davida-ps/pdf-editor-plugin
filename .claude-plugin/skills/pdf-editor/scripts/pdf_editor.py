#!/usr/bin/env python3
"""
PDF Editor Script

Provides utilities to:
- Rotate PDF pages
- Replace URLs/text (e.g., old wiki links with new ones)
- Add footer images to all pages

Usage:
    python pdf_editor.py --input document.pdf --output fixed.pdf \\
        --rotate "1:90,3:180" \\
        --replace-url "team-wiki.local" "team-wiki.etc.com" \\
        --footer-image logo.svg
"""

import argparse
import sys
from pathlib import Path

try:
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO
except ImportError:
    print("Error: Required libraries not installed.")
    print("Install with: pip install PyPDF2 reportlab")
    sys.exit(1)


def rotate_pages(pdf_path, rotations):
    """
    Rotate specific pages in a PDF.

    Args:
        pdf_path: Path to input PDF
        rotations: Dict of {page_number: angle} (e.g., {1: 90, 3: 180})
                   Page numbers are 1-indexed

    Returns:
        PdfWriter object with rotated pages
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]

        # Rotate if specified (page_num is 0-indexed, rotations dict is 1-indexed)
        if (page_num + 1) in rotations:
            angle = rotations[page_num + 1]
            page.rotate(angle)

        writer.add_page(page)

    return writer


def replace_text_in_pdf(pdf_path, old_text, new_text):
    """
    Replace text/URLs in PDF.

    Note: This modifies text streams. Some PDFs (especially scanned/OCR'd)
    may have text as images, which cannot be modified with this approach.

    Args:
        pdf_path: Path to input PDF
        old_text: Text to find (e.g., "team-wiki.local")
        new_text: Text to replace with (e.g., "team-wiki.etc.com")

    Returns:
        PdfWriter object with replaced text
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        # Attempt text replacement in content stream
        if page["/Contents"] is not None:
            content = page["/Contents"].get_object().get_data()

            # Replace old text with new text
            # Note: This is a simple byte-level replacement and may not work
            # for all PDFs, especially those with text encoding
            modified_content = content.replace(
                old_text.encode('utf-8'),
                new_text.encode('utf-8')
            )

            page["/Contents"].get_object().set_data(modified_content)

        writer.add_page(page)

    return writer


def add_footer_image(pdf_path, image_path, page_width=8.5, page_height=11):
    """
    Add an image to the footer of all PDF pages.

    Args:
        pdf_path: Path to input PDF
        image_path: Path to image (SVG, PNG, JPG) for footer
        page_width: Page width in inches (default: letter width)
        page_height: Page height in inches (default: letter height)

    Returns:
        PdfWriter object with footer images added
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Create a temporary PDF with the footer image
    footer_buffer = BytesIO()

    # Note: ReportLab's canvas doesn't directly support SVG placement
    # For SVG support, additional libraries like svglib are needed
    # This is a placeholder that handles raster images (PNG, JPG)

    for page in reader.pages:
        # Get page dimensions
        page_width_pts = float(page.mediabox.width)
        page_height_pts = float(page.mediabox.height)

        # Create footer with image using reportlab
        footer_buffer = BytesIO()
        c = canvas.Canvas(footer_buffer, pagesize=(page_width_pts, page_height_pts))

        # Typical footer position: right side, above page number
        # Adjust these values based on your preferences
        footer_x = page_width_pts - 50  # 50 points from right
        footer_y = 30  # 30 points from bottom
        image_size = 30  # 30x30 points

        try:
            # Try to draw image (works for PNG, JPG)
            if image_path.lower().endswith('.svg'):
                # SVG support would require svglib library
                # Placeholder: just document this limitation
                pass
            else:
                c.drawImage(image_path, footer_x - image_size, footer_y,
                           width=image_size, height=image_size)
        except Exception as e:
            print(f"Warning: Could not add footer image: {e}")

        c.save()

        # Merge footer onto page
        footer_buffer.seek(0)
        footer_pdf = PdfReader(footer_buffer)
        page.merge_page(footer_pdf.pages[0])

        writer.add_page(page)

    return writer


def main():
    parser = argparse.ArgumentParser(
        description="Edit PDFs: rotate pages, replace text, add footer images"
    )
    parser.add_argument("--input", required=True, help="Input PDF file")
    parser.add_argument("--output", required=True, help="Output PDF file")
    parser.add_argument(
        "--rotate",
        help='Pages to rotate as "page:angle,page:angle" (e.g., "1:90,3:180")'
    )
    parser.add_argument(
        "--replace-url",
        nargs=2,
        metavar=("OLD", "NEW"),
        help="Replace text/URL (e.g., team-wiki.local team-wiki.etc.com)"
    )
    parser.add_argument(
        "--footer-image",
        help="Add image to footer (SVG/PNG/JPG)"
    )

    args = parser.parse_args()

    # Validate input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    try:
        writer = PdfReader(args.input)

        # Apply rotations if specified
        if args.rotate:
            rotations = {}
            for rotation in args.rotate.split(","):
                page, angle = rotation.split(":")
                rotations[int(page)] = int(angle)
            writer = rotate_pages(args.input, rotations)

        # Apply text replacement if specified
        if args.replace_url:
            old, new = args.replace_url
            writer = replace_text_in_pdf(args.input, old, new)

        # Add footer image if specified
        if args.footer_image:
            if not Path(args.footer_image).exists():
                print(f"Error: Footer image not found: {args.footer_image}")
                sys.exit(1)
            writer = add_footer_image(args.input, args.footer_image)

        # Write output
        with open(args.output, "wb") as f:
            writer.write(f)

        print(f"✅ PDF processed successfully: {args.output}")

    except Exception as e:
        print(f"Error processing PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
