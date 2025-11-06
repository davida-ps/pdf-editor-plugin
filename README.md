# PDF Editor Plugin

Professional PDF editing plugin for Claude Code that enables page rotation, link/URL replacement, and company branding on footers.

## Features

- **Rotate Pages** - Fix page orientation issues by rotating specific pages
- **Replace URLs/Text** - Update all instances of old links/text (e.g., legacy wiki URLs)
- **Add Footer Branding** - Add company logo/SVG to footer on all pages
- **Batch Processing** - Process multiple PDFs with identical operations
- **Combined Operations** - Rotate, replace links, and add branding in a single command

## Installation

### Method 1: Git Repository (Recommended for Teams)

1. Clone or add this plugin to your project:
```bash
git clone https://github.com/your-org/pdf-editor-plugin .claude-plugins/pdf-editor
```

2. Commit and push to your repository:
```bash
git add .claude-plugins/pdf-editor
git commit -m "Add PDF Editor plugin"
git push
```

3. Team members pull the latest code:
```bash
git pull
```

4. Use Claude Code and ask Claude to fix PDFs - the plugin will automatically be available!

### Method 2: Local Installation

1. Place the plugin in your local Claude Code plugins directory
2. In Claude Code, run: `/plugin install ./pdf-editor-plugin`

## Quick Start

Once installed, simply ask Claude naturally:

```
"Fix this PDF - rotate page 3 and update all wiki links"
"Update the old wiki links in this document and add our company footer"
"Make sure this PDF is oriented correctly, has updated links, and includes our branding"
```

Upload your PDF file in the chat, and Claude will automatically use the PDF Editor plugin to process it.

## Usage Examples

### Rotate Pages
```
"Rotate page 3 of this PDF by 90 degrees clockwise"
```

### Replace Links
```
"Update all instances of team-wiki.local to team-wiki.etc.com in this PDF"
```

### Add Footer Branding
```
"Add our company logo to the footer of all pages in this PDF"
```

### Combined Operation (Most Common)
```
"Fix this PDF - rotate page 2, update wiki links, and add branding"
```

## Configuration

### Customize Company Logo

Replace the default placeholder logo with your company's SVG:

1. Locate: `.claude-plugin/skills/pdf-editor/assets/footer_logo.svg`
2. Replace with your SVG file
3. Commit and push changes
4. Team members' next pull will have the updated logo

### Adjust Footer Position

Edit `.claude-plugin/skills/pdf-editor/scripts/pdf_editor.py`:

```python
footer_x = page_width_pts - 50     # Distance from right edge (points)
footer_y = 30                       # Distance from bottom (points)
image_size = 30                     # Width/height in points
```

## System Requirements

- Python 3.8+
- Dependencies:
  - PyPDF2 (>= 3.0.0)
  - reportlab (>= 4.0.0)

Install dependencies:
```bash
pip install PyPDF2 reportlab
```

## Troubleshooting

### Text replacement isn't working
- The PDF may have text rendered as images (scanned or OCR'd PDFs)
- Try verifying if you can select and copy text in a PDF viewer
- If text isn't selectable, it's an image and cannot be modified

### Footer image isn't appearing
- Verify the image file path is correct
- Ensure the image format is supported (SVG, PNG, JPG)
- Check that the footer Y position isn't outside page bounds

### Page rotation isn't working
- Double-check page numbers (first page = 1, not 0)
- Verify the page exists in the PDF

## Documentation

For detailed API documentation and technical reference, see:
- `.claude-plugin/skills/pdf-editor/SKILL.md` - Complete skill guide
- `.claude-plugin/skills/pdf-editor/references/api_reference.md` - PyPDF2 & ReportLab API docs

## Support

For issues, feature requests, or questions:
- GitHub Issues: https://github.com/your-org/pdf-editor-plugin/issues
- Repository: https://github.com/your-org/pdf-editor-plugin

## License

MIT License - See LICENSE file for details

## Version

Current Version: 1.0.0

Last Updated: November 6, 2025
