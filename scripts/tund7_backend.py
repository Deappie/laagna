# Builds the 11IT lesson 7 PDFs in public/files/:
#   backend-konspekt.pdf, tunnijuhend-backend.pdf and the fillable kodutoo-backend.pdf.
# Needs ReportLab (pip install reportlab) and the macOS system fonts Arial and Menlo.
# Run from the project root: python scripts/tund7_backend.py
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (CondPageBreak, Flowable, KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

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


def build(path, doc_title, footer_text, story):
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Sans', 8)
        canvas.setFillColor(BLUE)
        canvas.drawString(20 * mm, 12 * mm, footer_text)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                            bottomMargin=20 * mm, title=doc_title, author='Maksim Tsõpov',
                            subject='11IT · Veebirakendused')
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


# ---------------------------------------------------------------- konspekt

HELLO = '''
import express from 'express';

const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('Tere! Söökla server töötab.');
});

app.listen(PORT, () => {
  console.log(`Server töötab: http://localhost:${PORT}`);
});
'''

konspekt = [
    p('Node.js ja Express', title),
    p('11IT · Veebirakendused · seitsmes tund · konspekt', sub),
    note('<b>Selle tunni suur mõte:</b> backend ei ole võlukast kuskil kaugel andmekeskuses. See on tavaline '
         'JavaScripti programm, mis käivitub, jääb ootama ja vastab igale päringule, mis tema poole tuleb. '
         'Täna kirjutad sellise ise.'),

    p('Kes seal teisel pool vastab?', h2),
    p('API tunnis küsisid andmeid PokeAPI-lt. Sinu ' + c('fetch') + ' läks kuhugi teele ja natukese aja pärast tuli '
      'JSON tagasi. Aga kes seal vastas? Mitte inimene ja mitte andmebaas ise. Vastas programm, mille keegi on '
      'kirjutanud umbes nii: „kui keegi küsib aadressi ' + c('/api/v2/pokemon/pikachu') + ', otsi Pikachu andmed '
      'üles ja saada need JSON-ina tagasi“.'),
    p('Selline programm käitub teisiti kui kõik, mida oled seni kirjutanud. ' + c('node tere.js') + ' trükkis kaks rida '
      'ja lõpetas, terminal oli kohe jälle vaba. Server ei lõpeta. Ta käivitub, ütleb „olen valmis“ ja jääb ootama. '
      'Esimene päring võib tulla sekundi pärast või tunni pärast. Kui see tuleb, teeb server oma töö ära ja ootab '
      'edasi.'),
    p('Seda oled tegelikult juba näinud. Pärast ' + c('npm run dev') + ' ei andnud terminal ' + c('PS …>') + ' rida '
      'tagasi, sest Vite on ka server ja ta jäi ootama. ' + c('Ctrl+C') + ' paneb serveri kinni. Restorani keeles: '
      'köök on lukus. Kelner võib tellimusi tuua palju tahab, keegi ei vasta.'),

    p('Node.js: JavaScript ilma brauserita', h2),
    p('Seni elas su JavaScript brauseris. Node.js on programm, mis käivitab JavaScripti otse arvutis. Keel on täpselt '
      'sama: muutujad, funktsioonid, ' + c('if') + ', massiivid ja ' + c('map') + ' töötavad nagu ennegi. Muutunud on '
      'see, mis ümberringi on.'),
    table(['', 'Brauseris', 'Node’is'], [
        ['Leht, nupud, ' + c('document'), 'on olemas', 'puuduvad, Node’il pole ekraani ega lehte'],
        [c('console.log'), 'läheb F12 konsooli', 'läheb terminali'],
        ['Failid arvutis', 'ei pääse ligi (turvalisuse pärast)', 'saab lugeda ja kirjutada'],
        ['Võrk', 'saab päringuid saata (' + c('fetch') + ')', '<b>saab päringuid saata ja ka vastu võtta</b>'],
        ['Kes käivitab', 'kasutaja, kui lehe avab', 'sina, käsuga ' + c('node fail.js')],
    ], [WIDTH * 0.22, WIDTH * 0.36, WIDTH * 0.42]),
    Spacer(1, 6),
    p('Kõige olulisem on tabeli neljas rida. Node oskab päringuid vastu võtta ehk olla server. Seepärast saab '
      'backendi kirjutada samas keeles, mida juba oskad.'),

    p('npm ja paketid', h2),
    p('Serveri saaks kirjutada puhta Node’iga, aga see on üsna tülikas. Kõik kirjutavad sama koodi: loe päringust '
      'aadress välja, otsusta, mida teha, pane vastusele õiged päised. Nii et keegi kirjutas selle ühe korra valmis '
      'ja pani npm-i üles. Sellist valmis koodi nimetatakse <b>paketiks</b>. Meie kasutame paketti nimega '
      '<b>Express</b>, see on Node’i serverite seas kõige levinum.'),
    code('npm install express'),
    p('See üks käsk teeb kolm asja:'),
    *bullets(
        'laeb Expressi alla kausta ' + c('node_modules') + '. Koos Expressiga tuleb kaasa mitukümmend teist paketti, '
        'mida Express ise vajab. Ära ehmu, kui seal on palju kaustu;',
        'kirjutab ' + c('package.json') + '-isse rea ' + c('"express": "^5.3.0"') + ' (versioon võib olla teine). '
        'See on nimekiri: „sellel projektil on vaja Expressi“;',
        'teeb faili ' + c('package-lock.json') + ', kuhu on kirjas kõigi pakettide täpsed versioonid.'),
    p('Tänu sellele nimekirjale ei pea ' + c('node_modules') + '-it kellelegi saatma ega Gitti panema. Kes iganes '
      'projekti saab, kirjutab ' + c('npm install') + ' ja npm laeb samad paketid ise alla. Reacti projektiga tegid '
      'sa täpselt sama asja, lihtsalt siis juhendi järgi.'),
    note('<b>Õige kaust!</b> Söökla projektis on nüüd kaks ' + c('package.json') + '-it: üks projekti juurkaustas '
         '(frontend) ja teine kaustas ' + c('server') + ' (backend). Express kuulub backendile. Enne installimist '
         'kirjuta ' + c('cd server') + ' ja kontrolli ' + c('pwd') + '-ga, kus oled.'),

    p('Esimene server', h2),
    p('Terve server, mis vastab ühele aadressile, mahub kümnesse ritta:'),
    code(HELLO, 'server/index.js'),
    explain([
        ["import express from 'express';", 'Toob Expressi paketist sisse. Sama ' + c('import') + ', mida kasutasid '
         'Reactis, aga Node vajab selleks ' + c('package.json') + '-isse rida ' + c('"type": "module"') + '.'],
        ['const app = express();', 'Teeb uue serveri. ' + c('app') + ' ongi meie server, kõik reeglid paneme talle.'],
        ["app.get('/', (req, res) => {", 'Reegel: kui keegi teeb GET-päringu aadressile ' + c('/') + ', käivita see '
         'funktsioon.'],
        ["res.send('Tere! ...');", 'Saadab vastuseks teksti.'],
        ['app.listen(PORT, () => {', 'Käivitab serveri pordil 3000 ja jääb päringuid ootama. Funktsioon käivitub '
         'üks kord, kui server on valmis.'],
    ]),
    Spacer(1, 6),
    p('Käivita ' + c('node index.js') + ' ja ava brauseris ' + c('http://localhost:3000') + '. Ekraanil on sinu '
      'tekst. Sinu brauser saatis päringu, sinu programm vastas.'),

    p('Marsruut: meetod, aadress ja funktsioon', h2),
    p('Expressi server on sisuliselt reeglite nimekiri. Iga reegel ütleb: kui tuleb <i>selline</i> päring '
      '<i>sellele</i> aadressile, tee <i>seda</i>. Ühte sellist reeglit nimetatakse <b>marsruudiks</b> '
      '(ingl <i>route</i>).'),
    code('''
app.get('/api/arvustused', (req, res) => {
  res.json(arvustused);
});
'''),
    table(['Tükk', 'Mis see on'], [
        [c('app.get'), 'Meetod. ' + c('get') + ' vastab GET-päringutele. Järgmises tunnis tuleb juurde '
         + c('app.post') + '.'],
        [c("'/api/arvustused'"), 'Aadress, millele see reegel vastab.'],
        [c('(req, res) => { … }'), 'Funktsioon, mille Express käivitab iga sellise päringu peale.'],
        [c('req'), '<b>Request</b> ehk päring: kõik, mida klient küsis (aadress, parameetrid, saadetud andmed).'],
        [c('res'), '<b>Response</b> ehk vastus: sellega saadad kliendile midagi tagasi.'],
    ], [WIDTH * 0.3, WIDTH * 0.7]),
    Spacer(1, 6),
    p('Vastuse saatmiseks on mõned käsud:'),
    table(['Käsk', 'Mida teeb'], [
        [c("res.send('Tere')"), 'Saadab teksti.'],
        [c('res.json(andmed)'), 'Saadab andmed JSON-ina. Teeb ise ' + c('JSON.stringify') + ' ja ütleb brauserile, '
         'et tuleb JSON. Seda kasutame kõige rohkem.'],
        [c('res.status(404).json({ … })'), 'Paneb vastusele staatusekoodi ja saadab siis JSON-i. Kui staatust ei pane, '
         'on see 200.'],
    ], [WIDTH * 0.36, WIDTH * 0.64]),
    Spacer(1, 6),
    note('<b>Igale päringule täpselt üks vastus.</b> Kui funktsioon ei jõua kunagi ' + c('res.json') + '-i ega '
         + c('res.send') + '-ini, ei saa brauser midagi ja ootab. Ring keerleb, leht laeb ja laeb. Viga ei tule, '
         'sest server ei tea, et ta midagi unustas. Kui leht jääb laadima, otsi kõigepealt puuduvat vastust.'),

    p('Aadressi osad', h2),
    p('Võtame ühe aadressi tükkideks:'),
    code('http://localhost:3000/api/arvustused/2?min=4'),
    table(['Osa', 'Nimi', 'Tähendus'], [
        [c('http://'), 'protokoll', 'kuidas räägitakse'],
        [c('localhost'), 'host', 'mis arvutiga. ' + c('localhost') + ' on see arvuti, kus sa ise istud'],
        [c('3000'), 'port', 'millise programmiga selles arvutis'],
        [c('/api/arvustused/2'), 'tee', 'selle järgi valib Express, milline marsruut käivitub'],
        [c('?min=4'), 'päringu parameetrid', 'lisasoovid, mitu tükki eraldatakse ' + c('&') + '-ga: '
         + c('?min=4&sort=toit')],
    ], [WIDTH * 0.27, WIDTH * 0.2, WIDTH * 0.53]),
    Spacer(1, 6),
    p('Ühe arvustuse jaoks ei tee keegi eraldi marsruuti ' + c('/api/arvustused/1') + ', ' + c('/api/arvustused/2')
      + ' ja nii edasi. Selle asemel pannakse aadressi muutuv osa, mille ees on koolon:'),
    code('''
app.get('/api/arvustused/:id', (req, res) => {
  console.log(req.params.id);   // aadressi /api/arvustused/2 puhul: '2'
});
'''),
    p('Koolon tähendab: siin võib olla mida iganes, pane see ' + c('req.params.id') + '-sse. Päringu parameetrid '
      + c('?min=4') + ' jõuavad samamoodi ' + c('req.query.min') + '-i.'),
    note('<b>Lõks, millesse peaaegu kõik esimesel korral astuvad:</b> aadress on alati tekst. ' + c('req.params.id')
         + ' on ' + c("'2'") + ', mitte ' + c('2') + '. Ja ' + c("'2' === 2") + ' on JavaScriptis ' + c('false')
         + '. Kui võrdled seda arvuga, ei leia sa kunagi midagi. Tee enne ' + c('Number(req.params.id)') + '.'),

    p('Staatusekoodid', h2),
    p('Need tunned juba frontendi ja backendi konspektist. Nüüd paned neid ise:'),
    table(['Kood', 'Tähendus', 'Millal sina selle saadad'], [
        ['200', 'OK', 'kõik läks hästi. ' + c('res.json') + ' paneb selle ise'],
        ['201', 'Created, loodud', 'uus asi lisati. Järgmises tunnis, kui tuleb POST'],
        ['400', 'Bad Request, vigane päring', 'klient saatis jama, näiteks hinde 7'],
        ['404', 'Not Found, ei leitud', 'sellise id-ga arvustust pole'],
        ['500', 'Server Error', 'seda sa ise ei saada. See tuleb siis, kui sinu kood jookseb kokku'],
    ], [WIDTH * 0.1, WIDTH * 0.32, WIDTH * 0.58]),
    Spacer(1, 6),
    p('Üks 404 tuleb ka ilma sinuta. Kui ükski marsruut aadressile ei sobi, vastab Express ise: '
      + c('Cannot GET /api/arvustus') + '. See on Expressi teade, mitte sinu oma. Tavaliselt tähendab see kirjaviga '
      'aadressis või marsruudis.'),

    p('Kaks serverit, kaks porti', h2),
    p('Söökla projektis töötab nüüd korraga kaks programmi. Neid on lihtne segi ajada, nii et siin on nad kõrvuti:'),
    table(['', 'Frontend', 'Backend'], [
        ['Kaust', 'projekti juurkaust', c('server')],
        ['Käivitamine', c('npm run dev'), c('npm run dev') + ' (kaustas ' + c('server') + ')'],
        ['Programm', 'Vite', 'Node + Express'],
        ['Aadress', c('localhost:5173'), c('localhost:3000')],
        ['Mida annab', 'HTML, CSS ja Reacti kood', 'andmed JSON-ina'],
    ], [WIDTH * 0.2, WIDTH * 0.4, WIDTH * 0.4]),
    Spacer(1, 6),
    p('Mõtle pordist kui korteri numbrist. Maja on sama (' + c('localhost') + '), aga uksed on eri numbritega ja '
      'iga ukse taga elab eri programm. Ühe ukse taga saab elada ainult üks. Kui proovid teist serverit samale '
      'pordile panna, saad vea ' + c('EADDRINUSE') + '.'),
    p('Täna need kaks veel omavahel ei räägi. Backend vastab ainult brauseri aadressiribale.'),

    p('node --watch', h2),
    p('Server loeb su koodi sisse üks kord, käivitamisel. Kui muudad faili ja salvestad, töötab edasi vana kood. '
      'Pead serveri ' + c('Ctrl+C') + '-ga kinni panema ja uuesti käivitama. Seda unustab igaüks vähemalt korra '
      'ja otsib siis pool tundi viga, mida tegelikult enam pole. ' + c('node --watch index.js') + ' teeb '
      'taaskäivituse ise iga salvestuse peale. Paneme selle ' + c('package.json') + '-isse skriptiks ' + c('dev')
      + ', siis on käsk sama mis frontendil: ' + c('npm run dev') + '.'),

    p('Kui terminal ütleb midagi hirmsat', h2),
    p('Backendi vead ei tule F12 konsooli, vaid <b>terminali</b>, kus server töötab. Hoia see silma all.'),
    table(['Teade', 'Mida see tähendab', 'Mida teha'], [
        [c('EADDRINUSE') + ' … ' + c(':3000'), 'Port 3000 on juba kellegi käes. Tavaliselt sinu enda server '
         'teises terminalis.', 'Leia see terminal ja vajuta ' + c('Ctrl+C') + '.'],
        [c("Cannot find package 'express'"), 'Selles kaustas pole Expressi paigaldatud.',
         c('cd server') + ', siis ' + c('npm install express') + '.'],
        [c('Cannot use import statement outside a module'), 'Node ei tea, et kasutad ' + c('import') + '-i. '
         'Uuem Node annab vea asemel hoiatuse ' + c('MODULE_TYPELESS_…') + ' ja töötab edasi.',
         c('package.json') + '-isse ' + c('"type": "module"') + '.'],
        [c('Cannot GET /api/…') + ' (brauseris)', 'Sellist marsruuti pole.', 'Võrdle aadressi ja ' + c('app.get')
         + ' rida täht-tähelt.'],
        [c('ERR_CONNECTION_REFUSED') + ' (brauseris)', 'Server ei tööta.', 'Vaata terminali: kas server käib või '
         'kukkus veaga kokku?'],
        ['Leht laeb ja laeb', 'Marsruut ei saatnud vastust.', 'Kontrolli, kas kood jõuab ' + c('res.json')
         + '-ini.'],
        [c('SyntaxError'), 'Kirjaviga koodis.', 'Terminal näitab faili nime ja rea numbrit. Mine sinna.'],
    ], [WIDTH * 0.34, WIDTH * 0.33, WIDTH * 0.33]),

    p('Mis edasi?', h2),
    p('Täna vastab sinu server brauseri aadressiribale. Järgmises tunnis paneme Reacti küsima arvustusi sinu '
      'serverilt ja fail ' + c('andmed.ts') + ' läheb prügikasti. Siis tuleb ka ' + c('POST') + ': uus arvustus '
      'läheb serverisse ja server otsustab, kas hinne 7 on lubatud. Spoiler: ei ole.'),
]

# ---------------------------------------------------------------- tunnijuhend

SERVER_FULL = '''
import express from 'express';

const app = express();
const PORT = 3000;

const arvustused = [
  { id: 1, toit: 'Kanakaste riisiga', hinne: 5, kommentaar: 'Parim toit sel nädalal!' },
  { id: 2, toit: 'Hernesupp', hinne: 3, kommentaar: 'Natuke liiga paks.' },
  { id: 3, toit: 'Makaronid hakklihaga', hinne: 4, kommentaar: 'Klassika, alati hea.' },
];

app.get('/', (req, res) => {
  res.send('Tere! Söökla server töötab.');
});

app.get('/api/arvustused', (req, res) => {
  res.json(arvustused);
});

app.get('/api/arvustused/:id', (req, res) => {
  const id = Number(req.params.id);
  const arvustus = arvustused.find((a) => a.id === id);
  if (!arvustus) {
    return res.status(404).json({ viga: 'Sellist arvustust ei ole' });
  }
  res.json(arvustus);
});

app.listen(PORT, () => {
  console.log(`Server töötab: http://localhost:${PORT}`);
});
'''

juhend = [
    p('Tunnijuhend: söökla backend', title),
    p('11IT · Veebirakendused · seitsmes tund · tunnis', sub),
    p('Viiendas tunnis tegid söökla arvustuste frontendi. Arvustused olid failis ' + c('andmed.ts') + ', mis tegi '
      'näo, et on backend. Täna teed päris backendi: Node’i programmi, mis annab samad arvustused JSON-ina. Reacti '
      'ühendame sellega järgmises tunnis.', intro),
    Spacer(1, 4),
    note('<b>Kuidas töötada.</b> Nagu eelmisel korral: kirjuta kood ise ümber, ära kopeeri, ja loe seletus kõrvalt '
         'läbi. Üks asi on uus. <b>Backendi vead ei ilmu brauseri konsooli, vaid terminali</b>, kus server töötab. '
         'Kui midagi ei tööta, vaata kõigepealt sinna. Konspekti lõpus on tabel levinumate vigadega.'),

    p('Samm 0: ettevalmistus', h2),
    p('Ava söökla projekt VS Code’is (File → Open Folder). Kui tegid terminali tunniülesannete 4. osa, on projektis '
      'juba kaust ' + c('server') + ' ja selle sees ' + c('package.json') + '. Ava terminal ja kontrolli:'),
    code('''
cd server
ls
'''),
    p('Kui ' + c('ls') + ' näitab ' + c('package.json') + '-it, on kõik korras. Kui kausta ' + c('server')
      + ' pole, tee see nüüd (projekti juurkaustas):'),
    code('''
mkdir server
cd server
npm init -y
'''),
    p('Kontrolli ka Node’i versiooni käsuga ' + c('node -v') + '. Vaja on vähemalt ' + c('v20') + '. Kui on vanem, '
      'ütle õpetajale.'),

    p('Samm 1: Express', h2),
    p('Terminal peab olema kaustas ' + c('server') + ' (' + c('pwd') + ' näitab lõpus ' + c('\\server') + '). Siis:'),
    code('npm install express'),
    p('Vaata ' + c('ls') + '-iga, mis tekkis. Kaust ' + c('node_modules') + ' ja fail ' + c('package-lock.json')
      + '. Ava ' + c('package.json') + ' (' + c('code package.json') + ') ja leia lõpust ' + c('dependencies')
      + '. Seal on nüüd Express.'),
    note('<b>Proovi:</b> mine ' + c('cd ..') + '-ga projekti juurkausta ja kirjuta ' + c('git status') + '. Kas '
         + c('server/node_modules') + ' on muutunud failide seas? Ei ole. Vite pani projekti tegemisel juurkausta '
         'faili ' + c('.gitignore') + ' ja seal on rida ' + c('node_modules') + '. See kehtib kõigile alamkaustadele. '
         'Mine ' + c('cd server') + '-ga tagasi.'),

    p('Samm 2: package.json korda', h2),
    p('Kaks muudatust. Esiteks peab Node teadma, et kasutame ' + c('import') + '-i nagu Reactis. Teiseks tahame '
      'käsku ' + c('npm run dev') + ', mis paneb serveri käima ja taaskäivitab selle iga salvestuse peale. Muuda '
      + c('server/package.json') + ' selliseks:'),
    code('''
{
  "name": "server",
  "version": "1.0.0",
  "type": "module",
  "main": "index.js",
  "scripts": {
    "dev": "node --watch index.js"
  },
  "dependencies": {
    "express": "^5.3.0"
  }
}
''', 'server/package.json'),
    explain([
        ['"type": "module",', 'Lubab ' + c('import') + '-i. Kui failis on juba ' + c('"type": "commonjs"')
         + ', muuda see ' + c('"module"') + '-iks. Kui sellist rida pole, lisa see.'],
        ['"scripts": {\n  "dev": "node --watch index.js"\n}', 'Rea ' + c('"test": …') + ' asemele tuleb '
         + c('"dev"') + '. ' + c('--watch') + ' taaskäivitab serveri, kui salvestad.'],
        ['"express": "^5.3.0"', 'Selle kirjutas npm. Ära muuda. Versioon võib sul olla teine.'],
    ]),
    Spacer(1, 6),
    p('Kui sinu failis on veel ridu (' + c('description') + ', ' + c('author') + ', ' + c('license') + '), võivad '
      'need jääda.'),
    note('<b>JSON on range.</b> Iga rea lõpus on koma, välja arvatud ploki viimasel real enne ' + c('}')
         + '-sulgu. Üks puuduv või üleliigne koma ja ' + c('npm run dev') + ' ütleb ' + c('JSON.parse')
         + '-i kohta midagi segast. Siis loe komad üle.'),

    p('Samm 3: esimene server', h2),
    p('Tee kausta ' + c('server') + ' fail ' + c('index.js') + ' (' + c('ni index.js') + ', siis '
      + c('code index.js') + ') ja kirjuta sinna:'),
    code(HELLO, 'server/index.js'),
    explain([
        ["import express from 'express';", 'Toob Expressi paketist.'],
        ['const app = express();', 'Teeb serveri. Kõik reeglid paneme ' + c('app') + '-ile.'],
        ['const PORT = 3000;', 'Port, millel server kuulab. Vite on 5173, meie võtame teise.'],
        ["app.get('/', (req, res) => {", 'Reegel: GET-päring aadressile ' + c('/') + ' käivitab selle funktsiooni. '
         + c('req') + ' on päring, ' + c('res') + ' vastus.'],
        ["res.send('Tere! ...');", 'Saadab vastuseks teksti.'],
        ['app.listen(PORT, () => {\n  console.log(...);\n});', 'Paneb serveri käima ja ootama. Kui server on valmis, '
         'kirjutab terminali aadressi. Tagurpidi ülakomad ' + c('`…`') + ' ja ' + c('${PORT}') + ' panevad muutuja '
         'teksti sisse, nagu Pythoni f-string.'],
    ]),
    Spacer(1, 6),
    p('Pane server käima. Terminal peab ikka olema kaustas ' + c('server') + ':'),
    code('npm run dev'),
    p('Terminal ütleb ' + c('Server töötab: http://localhost:3000') + '. Ctrl-klõpsa aadressil või kirjuta see '
      'brauserisse. Ekraanil on sinu tekst.'),
    note('<b>Proovi:</b> muuda tekst ' + c("'Tere! …'") + ' millekski muuks ja salvesta. Mis juhtus terminalis? '
         'Värskenda brauserit. Siis vajuta terminalis ' + c('Ctrl+C') + ' ja värskenda brauserit uuesti. Mida '
         'brauser nüüd ütleb ja miks? Pane server ' + c('npm run dev') + '-ga tagasi käima.'),

    p('Samm 4: arvustused JSON-ina', h2),
    p('Nüüd paneme serverisse samad arvustused, mis on frontendis failis ' + c('andmed.ts') + ', ja teeme neile '
      'aadressi. Lisa ' + c('index.js') + '-i ' + c('const PORT') + ' rea alla massiiv ja esimese marsruudi alla '
      'teine marsruut:'),
    code('''
const arvustused = [
  { id: 1, toit: 'Kanakaste riisiga', hinne: 5, kommentaar: 'Parim toit sel nädalal!' },
  { id: 2, toit: 'Hernesupp', hinne: 3, kommentaar: 'Natuke liiga paks.' },
  { id: 3, toit: 'Makaronid hakklihaga', hinne: 4, kommentaar: 'Klassika, alati hea.' },
];
''', 'server/index.js, const PORT rea alla'),
    code('''
app.get('/api/arvustused', (req, res) => {
  res.json(arvustused);
});
''', "server/index.js, app.get('/') marsruudi alla"),
    explain([
        ['const arvustused = [ … ];', 'Täpselt sama massiiv, mis ' + c('andmed.ts') + '-is, ainult tüübita, sest '
         'see fail on JavaScript, mitte TypeScript. Andmed elavad nüüd serveri mälus.'],
        ["app.get('/api/arvustused',", 'Uus reegel uuele aadressile. ' + c('/api') + ' alguses on kokkulepe: kõik, '
         'mis annab andmeid, algab nii. Nii on kohe näha, mis on leht ja mis on andmed.'],
        ['res.json(arvustused);', 'Saadab terve massiivi JSON-ina.'],
    ]),
    Spacer(1, 6),
    p('Salvesta. Server taaskäivitub ise. Ava ' + c('http://localhost:3000/api/arvustused') + '. Kas see '
      'meenutab midagi? Täpselt nii nägi välja PokeAPI vastus. Ainult et nüüd oled sina see, kes vastab.'),
    p('Ava F12 → <b>Network</b> ja värskenda lehte. Klõpsa päringul ' + c('arvustused') + '. Leia staatusekood '
      '(peaks olema 200) ja ' + c('Content-Type') + '. Selle päise pani ' + c('res.json') + ' ise.'),
    note('<b>Proovi:</b> kirjuta aadressiks ' + c('/api/arvustus') + ' (lõpust puudub ' + c('-ed') + '). Mida '
         'leht ütleb? Kes selle teate kirjutas? Sina igatahes mitte.'),

    p('Samm 5: üks arvustus', h2),
    p('Päris API annab ka ühe asja korraga, näiteks ' + c('/api/arvustused/2') + '. Lisa ' + c('index.js')
      + '-i eelmise marsruudi alla:'),
    code('''
app.get('/api/arvustused/:id', (req, res) => {
  const id = Number(req.params.id);
  const arvustus = arvustused.find((a) => a.id === id);
  if (!arvustus) {
    return res.status(404).json({ viga: 'Sellist arvustust ei ole' });
  }
  res.json(arvustus);
});
''', 'server/index.js'),
    explain([
        ["'/api/arvustused/:id'", 'Koolon teeb ' + c('id') + '-st muutuja. See reegel sobib aadressidele '
         + c('/api/arvustused/1') + ', ' + c('/2') + ', ' + c('/abc') + ' ja nii edasi.'],
        ['const id =\n  Number(req.params.id);', c('req.params.id') + ' on see, mis aadressis koolonikohal oli. '
         'Aadress on alati tekst, nii et ' + c("'2'") + '. ' + c('Number()') + ' teeb sellest arvu 2.'],
        ['arvustused.find((a) =>\n  a.id === id)', c('find') + ' käib massiivi läbi ja annab esimese, mille kohta '
         'tingimus on tõene. Kui ühtegi pole, annab ' + c('undefined') + '.'],
        ['if (!arvustus) {', c('!') + ' on „ei“. Kui arvustust ei leitud…'],
        ['return res.status(404)\n  .json({ viga: … });', '…saadame 404 ja selgituse. ' + c('return')
         + ' on oluline: see lõpetab funktsiooni, et kood ei jõuaks allolevale ' + c('res.json') + '-ile. '
         'Ühele päringule saab vastata ainult üks kord.'],
        ['res.json(arvustus);', 'Leiti, saadame selle ühe arvustuse.'],
    ]),
    Spacer(1, 6),
    p('Proovi brauseris ' + c('/api/arvustused/2') + ', ' + c('/api/arvustused/7') + ' ja ' + c('/api/arvustused/abc')
      + '. Mis staatusekoodi näitab Network? Mis on ' + c('Number(\'abc\')') + ' ja miks läheb ka see 404-sse?'),
    note('<b>Proovi:</b> kustuta ' + c('Number(') + ' ja ' + c(')') + ', nii et rida on ' + c('const id = req.params.id;')
         + '. Ava ' + c('/api/arvustused/2') + '. Arvustus 2 on ju olemas, miks siis 404? Vihje: ' + c('===')
         + ' võrdleb ka tüüpi. Pane ' + c('Number') + ' tagasi.'),

    p('Samm 6: salvesta Gitti', h2),
    p('Mine projekti juurkausta ja tee commit:'),
    code('''
cd ..
git status
git add .
git commit -m "Esimene backend: arvustused JSON-ina"
'''),
    p(c('git status') + ' peab lõpuks ütlema ' + c('nothing to commit') + '. Ja ' + c('node_modules') + '-it seal '
      'ei olnud, nagu samm 1 lubas.'),

    PageBreak(),
    p('Kogu fail', h2),
    p('Kui midagi ei tööta, võrdle oma faili sellega. Ära kopeeri seda sisse, otsi, kus on erinevus.'),
    code(SERVER_FULL, 'server/index.js'),

    p('Kui jõuad varem valmis', h2),
    p('Need on väljakutsed: koodi pole, ainult vihjed. Iga väljakutse on uus marsruut ' + c('index.js') + '-is. '
      'Proovi brauseris järele.'),
    *bullets(
        '<b>Statistika.</b> ' + c('GET /api/statistika') + ' vastab ' + c('{ "arv": 3, "keskmine": 4 }')
        + '. Vihje: ' + c('arvustused.length') + ' ja ' + c('for') + '-tsükkel, mis liidab hinded kokku.',
        '<b>Ainult head.</b> ' + c('GET /api/arvustused?min=4') + ' annab ainult need, mille hinne on vähemalt 4. '
        'Vihje: ' + c('req.query.min') + ' ja ' + c('.filter()') + '. Mõtle, mis peab juhtuma, kui ' + c('?min')
        + ' aadressis üldse puudub. Seda tuleb muuta olemasolevas marsruudis, mitte uues.',
        '<b>Menüü.</b> ' + c('GET /api/toidud') + ' annab ainult toitude nimed: '
        + c('["Kanakaste riisiga", "Hernesupp", …]') + '. Vihje: ' + c('.map()') + '.',
        '<b>Soovitus.</b> ' + c('GET /api/soovitus') + ' annab ühe juhusliku arvustuse, mille hinne on vähemalt 4. '
        'Iga värskendusega võib tulla erinev. Vihje: ' + c('Math.random()') + ' ja ' + c('Math.floor()') + '.'),
    Spacer(1, 4),
    note('<b>Hoia projekt alles!</b> Järgmises tunnis paneme kaks serverit omavahel rääkima: React küsib arvustused '
         'sinu backendilt ja ' + c('andmed.ts') + ' läheb prügikasti.'),
]

# ---------------------------------------------------------------- kodutöö


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
            fieldFlags='multiline' if self.multiline else '', forceBorder=True,
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


RAAMATUD = '''
import express from 'express';

const app = express();

const raamatud = [
  { id: 1, pealkiri: 'Kevade', autor: 'Oskar Luts', laos: 3 },
  { id: 2, pealkiri: 'Tõde ja õigus', autor: 'A. H. Tammsaare', laos: 0 },
  { id: 3, pealkiri: 'Rehepapp', autor: 'Andrus Kivirähk', laos: 5 },
];

app.get('/api/raamatud', (req, res) => {
  res.json(raamatud);
});

app.get('/api/raamatud/:id', (req, res) => {
  const raamat = raamatud.find((r) => r.id === Number(req.params.id));
  if (!raamat) {
    return res.status(404).json({ viga: 'Sellist raamatut pole' });
  }
  res.json(raamat);
});

app.get('/api/laos', (req, res) => {
  res.json(raamatud.filter((r) => r.laos > 0));
});

app.listen(4000);
'''

kodutoo = [
    p('Kodutöö: esimene backend', title),
    p('11IT · Veebirakendused · seitsmes tund · kodutöö', sub),
    row([p('Nimi', label_b), Field('nimi', 220), '', p('Kuupäev', label_b), Field('kuupaev', 110), ''],
        [51, 220, 18, 51, 110, WIDTH + 12 - 450], PALE),
    Spacer(1, 8),
    p('Midagi paigaldama ei pea, piisab brauserist. Kõik vastused leiad tunnijuhendist ja konspektist. Kui sul on '
      'arvuti käepärast, võid koodi ka päriselt järele proovida, aga see pole kohustuslik. Ava see fail kursuse lehel '
      'nupuga „Vaata“, täida lahtrid, vajuta „<b>Laadi täidetud PDF alla</b>“ ja saada fail aadressile '
      '<b>mtsopo@taltech.ee</b> enne 3.11.', intro),

    p('1. Raamatukogu server', h2),
    p('Kooli raamatukogu tegi endale backendi. Loe kood läbi:'),
    code(RAAMATUD, 'index.js'),
    p('Server töötab. Mida saad vastuseks, kui avad brauseris need aadressid? Kirjuta staatusekood ja lühidalt, mis '
      'tuleb. Kui vastust ei tule üldse, kirjuta koodi lahtrisse kriips ja selgita kõrvale, miks.'),
]

requests = [
    ('a', 'http://localhost:4000/api/raamatud/3'),
    ('b', 'http://localhost:4000/api/raamatud/9'),
    ('c', 'http://localhost:4000/api/laos'),
    ('d', 'http://localhost:4000/api/raamat'),
    ('e', 'http://localhost:3000/api/raamatud'),
]
kodutoo.append(row([p('<b>Aadress</b>', label), p('<b>Kood</b>', label), '', p('<b>Mis tuleb vastuseks</b>', label)],
                   [190, 40, 8, WIDTH - 238]))
for key, url in requests:
    kodutoo.append(row([p(f'<b>{key})</b> ' + c(url.replace('http://localhost', '…')), label), Field(f'kood_{key}', 40),
                        '', Field(f'vastus_{key}', WIDTH - 238)], [190, 40, 8, WIDTH - 238]))
kodutoo += [
    Spacer(1, 4),
    p('Aadressides on ' + c('…') + ' asemel ' + c('http://localhost') + '. Vaata hoolega porti!', intro),
    Spacer(1, 8),
    question('<b>f)</b> Päringu a) puhul: mis on ' + c('req.params.id') + ' väärtus ja mis tüüpi see on? Miks on '
             'koodis ' + c('Number()') + '?', 'q_params', 40),

    p('2. Leia viga', h2),
    p('Igal õpilasel on üks probleem. Kirjuta, mis on valesti ja kuidas seda parandada.'),
    question('<b>a)</b> Mari tahab, et marsruut annaks ainult head arvustused. Brauser laeb ja laeb, aga midagi ei tule '
             'ja terminalis pole ühtegi viga.', 'viga_mari', 40, extra=code_parts('''
app.get('/api/head', (req, res) => {
  const head = arvustused.filter((a) => a.hinne >= 4);
});
''')),
    question('<b>b)</b> Jaan avab ' + c('/api/arvustused/1') + ' ja saab 404, kuigi arvustus id-ga 1 on kindlasti '
             'olemas.', 'viga_jaan', 40, extra=code_parts('''
const arvustus = arvustused.find((a) => a.id === req.params.id);
''')),
    question('<b>c)</b> Liisa kirjutab ' + c('npm run dev') + ' ja saab vea '
             + c('Error: listen EADDRINUSE: address already in use :::3000') + '. Ta on kindel, et tal pole ühtegi '
             'teist serverit käimas. Mida peaks ta kontrollima?', 'viga_liisa', 40),
    question('<b>d)</b> Karl kirjutas ' + c('npm install express') + ' kohe pärast VS Code’i avamist, projekti '
             'juurkaustas. Nüüd ütleb server ' + c("Cannot find package 'express'") + '. Miks? Mis käsud ta peaks '
             'kirjutama?', 'viga_karl', 40),

    CondPageBreak(230),
    p('3. Kirjuta ise', h2),
    question('Kirjuta söökla serverile marsruut ' + c('GET /api/statistika') + ', mis vastab nii: '
             + c('{ "arv": 3, "keskmine": 4 }') + '. Arvustused on massiivis ' + c('arvustused') + ' nagu tunnis. '
             'Kui sa ei saa päris täpselt valmis, kirjuta nii palju, kui oskad. Ka pool lahendust on parem kui tühi '
             'lahter.', 'statistika', 150),
    question('<b>4. Mõtle.</b> Tunnis andis server täpselt samad arvustused, mis olid juba failis ' + c('andmed.ts')
             + '. Milleks siis backendit vaja on? Too vähemalt kaks põhjust. Frontendi ja backendi konspektis on '
             'abi.', 'motle', 56),
]


if __name__ == '__main__':
    build('public/files/backend-konspekt.pdf', 'Node.js ja Express', '11IT · Veebirakendused · Node.js ja Express',
          konspekt)
    build('public/files/tunnijuhend-backend.pdf', 'Tunnijuhend: söökla backend',
          '11IT · Veebirakendused · Tunnijuhend: söökla backend', juhend)
    build('public/files/kodutoo-backend.pdf', 'Kodutöö: esimene backend',
          '11IT · Veebirakendused · Kodutöö: esimene backend', kodutoo)
