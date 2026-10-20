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
from reportlab.platypus import (CondPageBreak, Flowable, KeepTogether, Paragraph, Preformatted, SimpleDocTemplate, Spacer,
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
const express = require('express');

const app = express();

app.get('/', (req, res) => {
  res.send('Tere! Söökla server töötab.');
});

app.listen(3000, () => {
  console.log('Server töötab: http://localhost:3000');
});
'''

ARVUSTUSED = '''
const arvustused = [
  { id: 1, toit: 'Kanakaste riisiga', hinne: 5, kommentaar: 'Parim toit sel nädalal!' },
  { id: 2, toit: 'Hernesupp', hinne: 3, kommentaar: 'Natuke liiga paks.' },
  { id: 3, toit: 'Makaronid hakklihaga', hinne: 4, kommentaar: 'Klassika, alati hea.' },
];
'''

ROUTE = '''
app.get('/api/arvustused', (req, res) => {
  res.json(arvustused);
});
'''

konspekt = [
    p('Server ja Node.js', title),
    p('11IT · Veebirakendused · seitsmes tund · konspekt', sub),
    note('<b>Selle tunni suur mõte:</b> server on lihtsalt programm, mis ootab küsimusi ja vastab neile. '
         'Täna kirjutad sellise ise. See tuleb umbes kümme rida pikk.'),

    p('Mis juhtub, kui avad veebilehe?', h2),
    p('Kirjutad brauserisse ' + c('tahvel.edu.ee') + ' ja vajutad Enterit. Sekundi pärast on leht ees. Selle sekundi '
      'jooksul juhtus kaks asja.'),
    p('Kõigepealt saatis sinu brauser kuhugi kaugele arvutisse küsimuse: „palun anna mulle see leht“. Seda küsimust '
      'nimetatakse <b>päringuks</b>. Seal kaugel arvutis töötab programm, mis päringu kätte sai, otsis õige asja '
      'üles ja saatis selle tagasi. Seda, mis tagasi tuleb, nimetatakse <b>vastuseks</b>.'),
    p('Programmi, mis päringutele vastab, nimetatakse <b>serveriks</b>. Seda, kes küsib (meil brauser), '
      'nimetatakse <b>kliendiks</b>.'),
    table(['Restoranis', 'Veebis'], [
        ['Klient istub laua taga ja tellib', '<b>Klient</b> ehk brauser'],
        ['Tellimus: „üks hernesupp, palun“', '<b>Päring</b>'],
        ['Köök, kus tellimus täidetakse', '<b>Server</b>'],
        ['Supitaldrik, mis lauale tuuakse', '<b>Vastus</b>'],
    ], [WIDTH * 0.5, WIDTH * 0.5]),
    Spacer(1, 6),
    p('Pane tähele, et köök ei tee midagi enne, kui keegi tellib. Samamoodi server. Ta käivitub, ütleb „olen '
      'valmis“ ja jääb ootama. Võib-olla tuleb esimene päring kohe, võib-olla tunni pärast. Iga päringu peale teeb ta '
      'oma töö ja ootab jälle edasi.'),
    p('Üks server on sul tegelikult juba olnud. Kui kirjutasid Reacti projektis ' + c('npm run dev') + ', ei tulnud '
      'terminali uut ' + c('PS …>') + ' rida. See oli sellepärast, et Vite on server ja ta jäi ootama. '
      + c('Ctrl+C') + ' paneb serveri kinni, nagu köögi uks lukku.'),

    p('Milleks meil server?', h2),
    p('Söökla rakenduses olid arvustused failis ' + c('andmed.ts') + ' ja uued arvustused ainult brauseri mälus. '
      'Vajutasid F5 ja kõik uued arvustused olid kadunud. Pinginaaber ei näinud neid kunagi, sest need olid ainult '
      'sinu arvutis.'),
    p('Server lahendab selle. Kui arvustused on serveris, küsivad kõik brauserid neid samast kohast. Sinu lisatud '
      'arvustust näeb ka pinginaaber. Täna teeme esimese sammu: server, mis annab arvustused välja.'),

    p('Node.js: JavaScript ilma brauserita', h2),
    p('Seni käivitas sinu JavaScripti alati brauser. Serveris pole aga brauserit, pole akent ega nuppe. Seal käivitab '
      'JavaScripti programm nimega <b>Node.js</b>. Keel on täpselt sama: muutujad, funktsioonid ja massiivid '
      'töötavad nagu ennegi.'),
    p('Kaks erinevust tuleb meelde jätta. Esiteks ' + c('console.log') + ' ei kirjuta enam F12 konsooli, vaid '
      '<b>terminali</b>. Teiseks pole Node’is lehte, nii et ' + c('document') + ' ja ' + c('querySelector')
      + ' ei tööta. Neid ei ole serveris vaja.'),
    KeepTogether([p('Node’i programm käivitatakse terminalis nii:'), *code_parts('node index.js')]),

    p('JSON: andmed tekstina', h2),
    p('Server võib saata vastuseks HTML-lehe, aga meie server saadab andmeid. Andmed liiguvad serverist brauserisse '
      'kujul, mida nimetatakse <b>JSON</b>-iks. See näeb välja peaaegu nagu JavaScripti massiiv ja objektid:'),
    code('''
[
  { "id": 1, "toit": "Kanakaste riisiga", "hinne": 5 },
  { "id": 2, "toit": "Hernesupp", "hinne": 3 }
]
'''),
    p('Nurksulud on massiiv, loogelised sulud on üks objekt. Ainus erinevus JavaScriptist on see, et JSON-is on ka '
      'väljade nimed jutumärkides. Seda ei pea ise kirjutama, Express teeb selle meie eest.'),

    p('Pakett ja npm', h2),
    p('Serveri saaks kirjutada ka puhta Node’iga, aga see on pikk ja tülikas. Seepärast kasutame <b>Expressi</b>. '
      'Express on <b>pakett</b> ehk kellegi teise kirjutatud kood, mille saad oma projekti ühe käsuga:'),
    code('npm install express'),
    p(c('npm') + ' on programm, mis toob pakette internetist. Pärast seda käsku on kaustas kaks uut asja:'),
    *bullets(
        c('node_modules') + ' on kaust, kus on Express ja kõik, mida Express ise vajab. Seal on palju kaustu. '
        'Ära ehmu ja ära sinna midagi muuda;',
        c('package.json') + '-isse tekib rida ' + c('"express"') + '. See on nimekiri: „sellel projektil on vaja '
        'Expressi“.'),
    p('Tänu sellele nimekirjale ei pea ' + c('node_modules') + '-it kellelegi saatma. Kes projekti saab, kirjutab '
      + c('npm install') + ' ja npm toob kõik ise.'),

    p('Aadress', h2),
    p('Meie server töötab sinu enda arvutis. Tema aadress on selline:'),
    code('http://localhost:3000/api/arvustused'),
    table(['Osa', 'Mida tähendab'], [
        [c('localhost'), 'See arvuti, mille taga sa istud. Server ei ole internetis, vaid sinu juures.'],
        [c('3000'), '<b>Port</b> ehk ukse number. Ühes arvutis võib töötada mitu serverit ja igaüks on oma ukse '
         'taga. Reacti Vite on uksel 5173, meie server on uksel 3000.'],
        [c('/api/arvustused'), 'Mida küsitakse. Ühel serveril võib olla palju aadresse, igaühe taga on midagi muud. '
         + c('/api') + ' alguses on kokkulepe: siit tulevad andmed.'],
    ], [WIDTH * 0.28, WIDTH * 0.72]),

    p('Esimene server', h2),
    p('Terve server mahub kümnesse ritta. Loe see läbi ja siis rida-realt seletus:'),
    code(HELLO, 'server/index.js'),
    explain([
        ["const express =\n  require('express');", 'Toob Expressi paketi sisse. ' + c('require') + ' tähendab '
         '„võta see pakett kasutusse“.'],
        ['const app = express();', 'Teeb uue serveri ja paneb selle muutujasse ' + c('app') + '.'],
        ["app.get('/', (req, res) => {", 'Reegel: kui keegi küsib aadressi ' + c('/') + ', käivita see funktsioon. '
         + c('get') + ' tähendab, et klient tahab midagi <i>saada</i>.'],
        ['(req, res)', 'Funktsioon saab kaks asja. ' + c('req') + ' on päring ehk see, mida küsiti. ' + c('res')
         + ' on vastus ehk sellega saadad midagi tagasi.'],
        ["res.send('Tere! ...');", 'Saadab vastuseks teksti.'],
        ['app.listen(3000, () => {', 'Paneb serveri uksel 3000 käima ja ootama.'],
        ["console.log('Server töötab...');", 'Kirjutab terminali, et server on valmis.'],
    ]),
    Spacer(1, 6),
    p('Reeglit „see aadress käivitab selle funktsiooni“ nimetatakse <b>marsruudiks</b>. Iga uue aadressi jaoks '
      'teed uue marsruudi, kõik täpselt sama kujuga.'),

    p('Andmed JSON-ina', h2),
    p('Teksti saatmine on tore, aga meie tahame saata arvustusi. Paneme serverisse massiivi ja teeme sellele '
      'marsruudi:'),
    code(ARVUSTUSED + ROUTE),
    p('Ainus uus asi on ' + c('res.json') + '. See teeb massiivist JSON-i ja saadab selle. Ava brauseris '
      + c('http://localhost:3000/api/arvustused') + ' ja näed oma arvustusi JSON-ina.'),

    p('Kaks käsku, mida vajad kogu aeg', h2),
    table(['Käsk', 'Mida teeb'], [
        [c('node --watch index.js'), 'Paneb serveri käima. ' + c('--watch') + ' tähendab: kui salvestad faili, '
         'käivitab server end ise uuesti. Ilma selleta töötaks edasi vana kood.'],
        [c('Ctrl+C'), 'Paneb serveri kinni. Terminal on jälle vaba.'],
    ], [WIDTH * 0.32, WIDTH * 0.68]),

    p('Kui midagi ei tööta', h2),
    p('Serveri vead ei tule F12 konsooli, vaid <b>terminali</b>, kus server töötab. Vaata alati kõigepealt sinna.'),
    table(['Mida näed', 'Mida see tähendab', 'Mida teha'], [
        [c('Cannot find module') + ' ' + c("'express'"), 'Selles kaustas pole Expressi.',
         'Kontrolli ' + c('pwd') + '-ga, et oled kaustas ' + c('server') + '. Siis ' + c('npm install express') + '.'],
        [c('EADDRINUSE') + ' … ' + c('3000'), 'Uks 3000 on juba kinni. Sinu server töötab juba teises terminalis.',
         'Leia see terminal ja vajuta ' + c('Ctrl+C') + '.'],
        [c('require is not defined'), 'Sinu ' + c('package.json') + '-is on rida ' + c('"type": "module"') + '.',
         'Kustuta see rida ' + c('package.json') + '-ist.'],
        [c('Cannot GET /api/…') + ' brauseris', 'Sellist marsruuti pole.', 'Võrdle aadressi ja ' + c('app.get')
         + ' rida täht-tähelt.'],
        ['Brauser ütleb, et lehte ei saa avada', 'Server ei tööta.', 'Vaata terminali. Kas server käib või kukkus '
         'veaga kokku?'],
        ['Leht laeb ja laeb', 'Marsruut ei saatnud vastust.', 'Kas funktsioonis on ' + c('res.send') + ' või '
         + c('res.json') + '?'],
        [c('SyntaxError'), 'Kirjaviga koodis.', 'Terminal näitab rea numbrit. Mine sinna.'],
    ], [WIDTH * 0.32, WIDTH * 0.34, WIDTH * 0.34]),

    p('Sõnastik', h2),
    table(['Sõna', 'Tähendus'], [
        ['<b>klient</b>', 'see, kes küsib. Meil brauser'],
        ['<b>server</b>', 'programm, mis ootab päringuid ja vastab neile'],
        ['<b>päring</b>', 'küsimus, mille klient serverile saadab'],
        ['<b>vastus</b>', 'see, mille server tagasi saadab'],
        ['<b>Node.js</b>', 'programm, mis käivitab JavaScripti ilma brauserita'],
        ['<b>Express</b>', 'pakett, millega on lihtne serverit teha'],
        ['<b>pakett</b>', 'kellegi teise kirjutatud kood, mille saad ' + c('npm install') + '-iga'],
        ['<b>JSON</b>', 'andmed tekstina, näevad välja nagu JavaScripti massiivid ja objektid'],
        ['<b>port</b>', 'ukse number, mille taga server arvutis ootab'],
        ['<b>marsruut</b>', 'reegel: see aadress käivitab selle funktsiooni'],
    ], [WIDTH * 0.22, WIDTH * 0.78]),
]

# ---------------------------------------------------------------- tunnijuhend

SERVER_FULL = '''
const express = require('express');

const app = express();

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

app.get('/api/menyy', (req, res) => {
  res.json(['Hernesupp', 'Kanakaste riisiga', 'Pannkoogid']);
});

app.listen(3000, () => {
  console.log('Server töötab: http://localhost:3000');
});
'''

juhend = [
    p('Tunnijuhend: söökla server', title),
    p('11IT · Veebirakendused · seitsmes tund · tunnis', sub),
    p('Täna teed söökla rakendusele serveri. Server annab arvustused välja JSON-ina. Reacti ühendame sellega '
      'järgmises tunnis, täna vaatame serveri vastuseid otse brauseris.', intro),
    Spacer(1, 4),
    note('<b>Kuidas töötada.</b> Kirjuta kood ise ümber, ära kopeeri, ja loe seletus kõrvalt läbi. Uus asi: '
         '<b>serveri vead ei ilmu brauseri konsooli, vaid terminali</b>, kus server töötab. Kui midagi ei tööta, '
         'vaata sinna. Konspekti lõpus on tabel levinumate vigadega.'),

    p('Samm 0: ettevalmistus', h2),
    p('Ava söökla projekt VS Code’is (File → Open Folder) ja ava terminal (Terminal → New Terminal). Kui tegid '
      'terminali tunniülesannete 4. osa, on projektis kaust ' + c('server') + '. Mine sinna:'),
    code('cd server'),
    p('Kui kausta ' + c('server') + ' veel pole, tee see ja mine sinna:'),
    code('''
mkdir server
cd server
npm init -y
'''),
    p('Kontrolli ' + c('pwd') + '-ga, et oled õiges kohas. Rea lõpus peab olema ' + c('\\server') + '.'),

    p('Samm 1: paigalda Express', h2),
    code('npm install express'),
    p('See võtab mõne sekundi. Siis vaata ' + c('ls') + '-iga, mis tekkis: kaust ' + c('node_modules') + ' ja fail '
      + c('package-lock.json') + '. Need tegi npm. Kaustas ' + c('node_modules') + ' elab nüüd Express.'),

    p('Samm 2: esimene server', h2),
    p('Tee kausta ' + c('server') + ' fail ' + c('index.js') + ' ja ava see:'),
    code('''
ni index.js
code index.js
'''),
    p('Kirjuta faili:'),
    code(HELLO, 'server/index.js'),
    explain([
        ["const express =\n  require('express');", 'Võtab Expressi kasutusse.'],
        ['const app = express();', 'Teeb serveri. ' + c('app') + ' ongi meie server.'],
        ["app.get('/', (req, res) => {", 'Kui keegi küsib aadressi ' + c('/') + ', käivita see funktsioon. '
         + c('req') + ' on päring, ' + c('res') + ' on vastus.'],
        ["res.send('Tere! ...');", 'Saadab vastuseks teksti.'],
        ['app.listen(3000, () => {', 'Paneb serveri uksel ehk pordil 3000 käima.'],
        ["console.log('Server töötab...');", 'Kirjutab terminali, et kõik on valmis.'],
    ]),
    Spacer(1, 6),
    p('Salvesta (' + c('Ctrl+S') + ') ja pane server käima:'),
    code('node --watch index.js'),
    p('Terminal ütleb ' + c('Server töötab: http://localhost:3000') + '. Ava see aadress brauseris. Ekraanil on '
      'sinu tekst. Brauser küsis, sinu programm vastas.'),
    note('<b>Proovi:</b> muuda tekst ' + c("'Tere! …'") + ' millekski muuks ja salvesta. Vaata terminali: server '
         'käivitus ise uuesti, sest ' + c('--watch') + '. Värskenda brauserit (F5).'),
    note('<b>Proovi veel:</b> vajuta terminalis ' + c('Ctrl+C') + ' ja värskenda brauserit. Mis juhtus? Köök on '
         'kinni, keegi ei vasta. Pane server uuesti käima: vajuta terminalis ↑ ja Enter.'),

    p('Samm 3: arvustused JSON-ina', h2),
    p('Paneme serverisse samad arvustused, mis on failis ' + c('andmed.ts') + '. Lisa need ' + c('index.js')
      + '-i rea ' + c('const app = express();') + ' alla:'),
    code(ARVUSTUSED, 'server/index.js'),
    p('Nüüd tee neile marsruut. Lisa see esimese marsruudi alla, enne ' + c('app.listen') + '-i:'),
    code(ROUTE, 'server/index.js'),
    explain([
        ['const arvustused = [ … ];', 'Täpselt sama massiiv, mis ' + c('andmed.ts') + '-is. Ainult tüüp '
         + c(': Arvustus[]') + ' puudub, sest see fail on tavaline JavaScript, mitte TypeScript.'],
        ["app.get('/api/arvustused',", 'Uus marsruut uuele aadressile.'],
        ['res.json(arvustused);', 'Saadab massiivi JSON-ina.'],
    ]),
    Spacer(1, 6),
    p('Salvesta ja ava brauseris ' + c('http://localhost:3000/api/arvustused') + '. Seal on sinu arvustused '
      'JSON-ina. Sellisel kujul saab React need järgmises tunnis kätte.'),
    note('<b>Proovi:</b> lisa massiivi neljas arvustus oma lemmiktoiduga. Ära unusta koma eelmise rea lõpus. '
         'Salvesta ja värskenda brauserit.'),
    note('<b>Proovi veel:</b> kirjuta aadressiks ' + c('/api/arvustus') + ' (lõpust puudub ' + c('ed') + '). Mida '
         'brauser ütleb? Server ei leidnud sellist marsruuti.'),

    p('Samm 4: tee ise üks marsruut', h2),
    p('Nüüd ilma valmis koodita. Tee marsruut aadressile ' + c('/api/menyy') + ', mis annab tänase söökla menüü. '
      'Menüü on lihtsalt massiiv toitude nimedega. Brauseris peab ' + c('http://localhost:3000/api/menyy')
      + ' näitama midagi sellist:'),
    code('["Hernesupp","Kanakaste riisiga","Pannkoogid"]'),
    p('Vihje: vaata samm 3 marsruuti. Sul on vaja sama kuju, ainult aadress ja saadetav asi on teised. Massiivi võid '
      'kirjutada otse ' + c('res.json(…)') + ' sulgude sisse.'),

    p('Samm 5: salvesta Gitti', h2),
    p('Pane server ' + c('Ctrl+C') + '-ga kinni, mine projekti kausta ja tee commit:'),
    code('''
cd ..
git add .
git commit -m "Esimene server"
'''),

    CondPageBreak(400),
    p('Kogu fail', h2),
    p('Kui midagi ei tööta, võrdle oma faili sellega. Otsi, kus on erinevus. Siin on ka samm 4 lahendus, nii et '
      'proovi enne ise!'),
    code(SERVER_FULL, 'server/index.js'),

    p('Kui jõuad varem valmis', h2),
    p('Iga väljakutse on uus marsruut. Koodi pole, ainult vihjed.'),
    *bullets(
        '<b>Minu kohta.</b> ' + c('/api/mina') + ' annab ühe objekti: ' + c('{ "nimi": "Mari", "klass": "11IT" }')
        + '. Vihje: ' + c('res.json') + ' saab saata ka ühe objekti, mitte ainult massiivi.',
        '<b>Mitu arvustust?</b> ' + c('/api/arv') + ' annab ' + c('{ "arv": 3 }') + '. Vihje: '
        + c('arvustused.length') + '. Lisa üks arvustus juurde ja vaata, kas number muutub.',
        '<b>Keskmine hinne.</b> ' + c('/api/keskmine') + ' annab kõigi hinnete keskmise. Vihje: ' + c('for')
        + '-tsükkel, mis liidab hinded kokku, ja siis jaga ' + c('length') + '-iga.'),
    Spacer(1, 4),
    note('<b>Hoia projekt alles!</b> Järgmises tunnis küsib React arvustused sinu serverilt ja fail '
         + c('andmed.ts') + ' läheb prügikasti.'),
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
const express = require('express');

const app = express();

const raamatud = ['Kevade', 'Tõde ja õigus', 'Rehepapp'];

app.get('/', (req, res) => {
  res.send('Tere tulemast raamatukokku!');
});

app.get('/api/raamatud', (req, res) => {
  res.json(raamatud);
});

app.listen(4000, () => {
  console.log('Raamatukogu server töötab');
});
'''

kodutoo = [
    p('Kodutöö: server', title),
    p('11IT · Veebirakendused · seitsmes tund · kodutöö', sub),
    row([p('Nimi', label_b), Field('nimi', 220), '', p('Kuupäev', label_b), Field('kuupaev', 110), ''],
        [51, 220, 18, 51, 110, WIDTH + 12 - 450], PALE),
    Spacer(1, 8),
    p('Midagi paigaldama ei pea, piisab brauserist. Vastused leiad konspektist ja tunnijuhendist. Ava see fail '
      'kursuse lehel nupuga „Vaata“, täida lahtrid, vajuta „<b>Laadi täidetud PDF alla</b>“ ja saada fail aadressile '
      '<b>mtsopo@taltech.ee</b> enne 3.11.', intro),

    p('1. Sõnad', h2),
    p('Seleta oma sõnadega, ühe lausega.'),
]
for key, word in [('server', 'server'), ('klient', 'klient'), ('paring', 'päring'), ('json', 'JSON'),
                  ('port', 'port'), ('npm', 'npm install')]:
    kodutoo.append(row([p(f'<b>{word}</b>', label), Field(f's_{key}', WIDTH - 90)], [90, WIDTH - 90]))

kodutoo += [
    p('2. Raamatukogu server', h2),
    p('Kooli raamatukogu tegi endale serveri. Loe kood läbi:'),
    code(RAAMATUD, 'index.js'),
    p('Server töötab. Mis ilmub brauserisse, kui avad need aadressid? Kui midagi ei ilmu, kirjuta, miks.'),
]
for key, url in [('a', 'http://localhost:4000/'), ('b', 'http://localhost:4000/api/raamatud'),
                 ('c', 'http://localhost:4000/api/raamat'), ('d', 'http://localhost:3000/api/raamatud')]:
    kodutoo.append(row([p(f'<b>{key})</b> ' + c(url), label), Field(f'vastus_{key}', WIDTH - 230)],
                       [230, WIDTH - 230]))
kodutoo += [
    Spacer(1, 8),
    question('<b>e)</b> Kuhu ilmub tekst ' + c('Raamatukogu server töötab') + '? Brauserisse või kuhugi mujale?',
             'q_log'),

    p('3. Leia viga', h2),
    p('Kirjuta, mis on valesti ja kuidas seda parandada.'),
    question('<b>a)</b> Mari tegi marsruudi, aga brauser laeb ja laeb ning midagi ei tule.', 'viga_mari', 40,
             extra=code_parts('''
app.get('/api/toidud', (req, res) => {
  const toidud = ['Hernesupp', 'Pannkoogid'];
});
''')),
    question('<b>b)</b> Jaan kirjutab ' + c('node --watch index.js') + ' ja saab vea, kus on sõna '
             + c('EADDRINUSE') + '. Mida see tähendab ja mida ta peaks tegema?', 'viga_jaan', 40),
    question('<b>c)</b> Karl kirjutas ' + c('npm install express') + ' kohe pärast VS Code’i avamist, projekti '
             'kaustas, mitte kaustas ' + c('server') + '. Nüüd ütleb server ' + c("Cannot find module 'express'")
             + '. Mis käsud ta peaks kirjutama?', 'viga_karl', 40),

    CondPageBreak(200),
    p('4. Kirjuta ise', h2),
    question('Kirjuta marsruut aadressile ' + c('/api/lemmikud') + ', mis annab vastuseks massiivi sinu kolme '
             'lemmiktoiduga. Vaata konspektist, kuidas marsruut välja näeb.', 'lemmikud', 90),
    question('<b>5. Mõtle.</b> Miks on söökla rakendusele serverit vaja? Mis juhtus arvustustega ilma serverita?',
             'motle', 56),
]


if __name__ == '__main__':
    build('public/files/backend-konspekt.pdf', 'Server ja Node.js', '11IT · Veebirakendused · Server ja Node.js',
          konspekt)
    build('public/files/tunnijuhend-backend.pdf', 'Tunnijuhend: söökla server',
          '11IT · Veebirakendused · Tunnijuhend: söökla server', juhend)
    build('public/files/kodutoo-backend.pdf', 'Kodutöö: server', '11IT · Veebirakendused · Kodutöö: server', kodutoo)
