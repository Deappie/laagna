# Shared ReportLab styles and building blocks for the course PDFs.
# Needs ReportLab (pip install reportlab) and the macOS system fonts Arial and Menlo.
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Flowable, KeepTogether, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

FONTS = '/System/Library/Fonts/Supplemental/'
pdfmetrics.registerFont(TTFont('Sans', FONTS + 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Sans-Bold', FONTS + 'Arial Bold.ttf'))
pdfmetrics.registerFont(TTFont('Sans-Italic', FONTS + 'Arial Italic.ttf'))
pdfmetrics.registerFont(TTFont('Mono', '/System/Library/Fonts/Menlo.ttc', subfontIndex=0))
pdfmetrics.registerFontFamily('Sans', normal='Sans', bold='Sans-Bold', italic='Sans-Italic')

NAVY = HexColor('#112D4E')
BLUE = HexColor('#3F72AF')
PALE = HexColor('#F1F4FA')
LINE = HexColor('#D6DEEA')
FIELD = HexColor('#F8FAFF')
NOTE_BG = HexColor('#FDF1DC')
NOTE_BAR = HexColor('#E8A33D')

WIDTH = A4[0] - 40 * mm - 12

title = ParagraphStyle('title', fontName='Sans-Bold', fontSize=22, leading=26, textColor=NAVY)
sub = ParagraphStyle('sub', fontName='Sans', fontSize=8.5, leading=11, textColor=BLUE, spaceAfter=14)
intro = ParagraphStyle('intro', fontName='Sans', fontSize=9, leading=12.5, textColor=BLUE)
h2 = ParagraphStyle('h2', fontName='Sans-Bold', fontSize=14, leading=18, textColor=BLUE, spaceBefore=12, spaceAfter=4,
                    keepWithNext=1)
body = ParagraphStyle('body', fontName='Sans', fontSize=10, leading=14, textColor=NAVY, spaceAfter=5)
cell = ParagraphStyle('cell', fontName='Sans', fontSize=8.5, leading=11.5, textColor=NAVY)
cell_b = ParagraphStyle('cell_b', parent=cell, fontName='Sans-Bold')
bullet = ParagraphStyle('bullet', parent=body, leftIndent=12, bulletIndent=2)
label = ParagraphStyle('label', fontName='Sans', fontSize=9.5, leading=12, textColor=NAVY)
label_b = ParagraphStyle('label_b', parent=label, fontName='Sans-Bold')
caption = ParagraphStyle('caption', fontName='Mono', fontSize=8.5, leading=11, textColor=BLUE, spaceBefore=2, spaceAfter=3)
code_style = ParagraphStyle('code', fontName='Mono', fontSize=8.5, leading=11.5, textColor=NAVY)
code_cell = ParagraphStyle('code_cell', fontName='Mono', fontSize=7.8, leading=10.5, textColor=NAVY)


def c(text):
    return f'<font name="Mono" size="9" color="#3F72AF">{escape(text)}</font>'


def p(text, style=body):
    return Paragraph(text, style)


def bullets(*items):
    return [Paragraph(i, bullet, bulletText='•') for i in items]


def code_parts(text, filename=None):
    box = Table([[Preformatted(text.strip('\n'), code_style)]], colWidths=[WIDTH])
    box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PALE),
        ('LINEBEFORE', (0, 0), (0, -1), 3, BLUE),
        ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    box.hAlign = 'LEFT'
    parts = [Paragraph(escape(filename), caption)] if filename else []
    return parts + [box, Spacer(1, 6)]


def code(text, filename=None):
    return KeepTogether(code_parts(text, filename))


def table(header, rows, widths, code_cols=()):
    data = [[Paragraph(h, cell_b) for h in header]]
    for r in rows:
        data.append([Preformatted(v, code_cell) if i in code_cols else Paragraph(v, cell) for i, v in enumerate(r)])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PALE),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    t.hAlign = 'LEFT'
    return t


def explain(rows):
    """Kood | Mida see teeb table, as in the söökla guide."""
    return table(['Kood', 'Mida see teeb'], rows, [WIDTH * 0.47, WIDTH * 0.53], code_cols=(0,))


def note(text):
    t = Table([[Paragraph(text, body)]], colWidths=[WIDTH - 12])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NOTE_BG),
        ('LINEBEFORE', (0, 0), (0, -1), 3, NOTE_BAR),
        ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    t.hAlign = 'LEFT'
    return KeepTogether([Spacer(1, 2), t, Spacer(1, 8)])


def build(path, doc_title, footer_text, story, subject='11IT · Veebirakendused'):
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Sans', 8)
        canvas.setFillColor(BLUE)
        canvas.drawString(20 * mm, 12 * mm, footer_text)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                            bottomMargin=20 * mm, title=doc_title, author='Maksim Tsõpov',
                            subject=subject)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


class Field(Flowable):
    def __init__(self, name, width=WIDTH, height=16, multiline=False):
        super().__init__()
        self.name, self.width, self.height, self.multiline = name, width, height, multiline

    def wrap(self, *_):
        return self.width, self.height

    def draw(self):
        x, y = self.canv.absolutePosition(0, 0)
        self.canv.acroForm.textfield(
            name=self.name, x=x, y=y, width=self.width, height=self.height,
            fontName='Helvetica', fontSize=10, textColor=NAVY,
            borderColor=BLUE, fillColor=FIELD, borderWidth=0.8, borderStyle='solid',
            fieldFlags='multiline' if self.multiline else '', forceBorder=True, maxlen=None,
        )


def row(cells, widths, background=None):
    t = Table([cells], colWidths=widths)
    style = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]
    if background:
        style += [('BACKGROUND', (0, 0), (-1, -1), background), ('LEFTPADDING', (0, 0), (0, 0), 6),
                  ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]
    t.setStyle(TableStyle(style))
    t.hAlign = 'LEFT'
    return t


def question(text, name, height=16, extra=()):
    return KeepTogether([p(text), *extra, Field(name, height=height, multiline=height > 16), Spacer(1, 10)])
