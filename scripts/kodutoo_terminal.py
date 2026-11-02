# Builds the fillable homework PDF public/files/kodutoo-terminal.pdf.
# Needs ReportLab (pip install reportlab) and the macOS system fonts Arial and Menlo.
# Run from the project root: python scripts/kodutoo_terminal.py
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

FONTS = '/System/Library/Fonts/Supplemental/'
pdfmetrics.registerFont(TTFont('Sans', FONTS + 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Sans-Bold', FONTS + 'Arial Bold.ttf'))
pdfmetrics.registerFont(TTFont('Mono', '/System/Library/Fonts/Menlo.ttc', subfontIndex=0))
pdfmetrics.registerFontFamily('Sans', normal='Sans', bold='Sans-Bold')

NAVY = HexColor('#112D4E')
BLUE = HexColor('#3F72AF')
PALE = HexColor('#F1F4FA')
FIELD = HexColor('#F8FAFF')
NOTE_BG = HexColor('#FDF1DC')
NOTE_BAR = HexColor('#E8A33D')

FOOTER = '11IT · Veebirakendused · Kodutöö: terminal'
WIDTH = A4[0] - 40 * mm - 12

title = ParagraphStyle('title', fontName='Sans-Bold', fontSize=22, leading=26, textColor=NAVY)
sub = ParagraphStyle('sub', fontName='Sans', fontSize=8.5, leading=11, textColor=BLUE, spaceAfter=14)
intro = ParagraphStyle('intro', fontName='Sans', fontSize=9, leading=12.5, textColor=BLUE)
h2 = ParagraphStyle('h2', fontName='Sans-Bold', fontSize=14, leading=18, textColor=BLUE, spaceBefore=12, spaceAfter=4)
body = ParagraphStyle('body', fontName='Sans', fontSize=10, leading=14, textColor=NAVY, spaceAfter=4)
label = ParagraphStyle('label', fontName='Sans', fontSize=9.5, leading=12, textColor=NAVY)
label_b = ParagraphStyle('label_b', parent=label, fontName='Sans-Bold')


def c(text):
    return f'<font name="Mono" size="9" color="#3F72AF">{text}</font>'


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


def note(text):
    t = Table([[Paragraph(text, body)]], colWidths=[WIDTH - 12])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NOTE_BG),
        ('LINEBEFORE', (0, 0), (0, -1), 3, NOTE_BAR),
        ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    t.hAlign = 'LEFT'
    return t


def question(text, name, height=16):
    return KeepTogether([Paragraph(text, body), Field(name, height=height, multiline=height > 16), Spacer(1, 9)])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Sans', 8)
    canvas.setFillColor(BLUE)
    canvas.drawString(20 * mm, 12 * mm, FOOTER)
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


story = [
    Paragraph('Kodutöö: terminal', title),
    Paragraph('11IT · Veebirakendused · Tööriistad · kodutöö', sub),
    row([Paragraph('Nimi', label_b), Field('nimi', 220), '', Paragraph('Kuupäev', label_b), Field('kuupaev', 110), ''],
        [51, 220, 18, 51, 110, WIDTH + 12 - 450], PALE),
    Spacer(1, 8),
    Paragraph(
        'Selle kodutöö jaoks ei pea midagi alla laadima ega paigaldama. Piisab brauserist, sobib ka telefon. '
        '1. osa teed kursuse lehel olevas <b>terminalimängus</b>, 2. ja 3. osa küsimustele vastad peast või konspekti ja '
        'abilehe abil. Ava see fail kursuse lehel nupuga „Vaata“, täida lahtrid, vajuta „<b>Laadi täidetud PDF alla</b>“ '
        'ja saada fail aadressile <b>mtsopo@taltech.ee</b> enne 20.10.', intro),

    Paragraph('1. Terminalimäng', h2),
    Paragraph('Mängi kursuse lehel terminalimäng lõpuni, kõik 10 missiooni. Mängu terminalis ei saa midagi katki teha, '
              'nii et proovi julgelt. Vastused allpool leiad mängust.', body),
    row([Paragraph('Salasõna failist ' + c('parool.txt'), label), Field('mang_sona', 150)], [150, 150]),
    Spacer(1, 4),
    question('Mis kaustas ' + c('parool.txt') + ' oli? Kirjuta täielik tee, nagu ' + c('pwd') + ' seda näitab.', 'mang_tee'),
    Paragraph('Mis käsk on mängu ' + c('package.json') + '-is nimede ' + c('dev') + ' ja ' + c('build') + ' taga?', body),
    row([Paragraph(c('dev'), label), Field('script_dev', 150), '', Paragraph(c('build'), label), Field('script_build', 150)],
        [34, 150, 20, 40, 150]),
    Spacer(1, 6),
    question('Mitu vihjet kasutasid? Milline missioon oli kõige raskem ja miks?', 'mang', 30),

    Paragraph('2. Mida see käsk teeb?', h2),
    Paragraph('Kirjuta iga käsu kõrvale ühe lausega, mida see teeb.', body),
]

commands = [
    ('k_cd', 'cd ..'),
    ('k_ni', 'ni server.js'),
    ('k_cat', 'cat package.json'),
    ('k_rm', 'rm -r vana-test'),
    ('k_install', 'npm install'),
    ('k_status', 'git status'),
    ('k_ctrlc', 'Ctrl+C'),
]
for name, cmd in commands:
    story.append(row([Paragraph(c(cmd), label), Field(name, WIDTH - 110)], [110, WIDTH - 110]))

story += [
    PageBreak(),
    Paragraph('3. Kas said aru?', h2),
    question('<b>a)</b> Oled kaustas ' + c('C:\\Users\\opilane\\projektid\\sookla-arvustused\\src')
             + '. Kirjuta <b>üks</b> käsk, mis viib sind kausta ' + c('projektid') + '.', 'q_cd'),
    question('<b>b)</b> Võta lahti käsk ' + c('git commit -m "Lisasin vormi"') + ': mis on siin programm, mis alamkäsk ja '
             'mis lipp? Miks on sõnum jutumärkides?', 'q_ehitus', 40),
    question('<b>c)</b> Kirjutad ' + c('npm run dev') + ' ja terminal ütleb ' + c('ENOENT … package.json')
             + '. Mis on kõige tõenäolisem põhjus ja kuidas seda kontrollida?', 'q_enoent', 40),
    question('<b>d)</b> Miks ei panda kausta ' + c('node_modules') + ' Gitti? Mis käsuga saab selle tagasi?', 'q_modules', 40),
    question('<b>e)</b> Kirjuta käsud järjest: tee kausta ' + c('server') + ' sisse kaust ' + c('api') + ', selle sisse fail '
             + c('index.js') + ' ja kontrolli, et fail on olemas. Eelda, et oled projekti kaustas.', 'q_kasud', 56),
    question('<b>f)</b> Käivitasid ' + c('npm run dev') + ' ja terminal ei näita enam uut ' + c('PS …>')
             + ' rida. Kas midagi on katki? Kuidas saad samal ajal kirjutada ' + c('git status') + '?', 'q_terminalid', 40),
    question('<b>g)</b> Mida tähendavad aadressis ' + c('http://localhost:5173') + ' sõna ' + c('localhost') + ' ja number '
             + c('5173') + '?', 'q_port', 40),
    Spacer(1, 2),
    note('Tunniülesannete 3. ja 4. osa (Node ja söökla projekt) kodus tegema ei pea, nendega jätkame järgmises tunnis. '
         'Hoia söökla projekt alles.'),
]

doc = SimpleDocTemplate('public/files/kodutoo-terminal.pdf', pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                        bottomMargin=20 * mm, title='Kodutöö: terminal', author='Maksim Tsõpov',
                        subject='11IT · Veebirakendused')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
