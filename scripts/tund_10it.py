# Builds the 10IT PDFs for lessons 7-11 in public/files/:
#   protsessor-konspekt.pdf, kodutoo-protsessor.pdf (fillable),
#   pildid-heli-konspekt.pdf and internet-konspekt.pdf.
# Needs ReportLab (pip install reportlab) and the macOS system fonts Arial and Menlo.
# Run from the project root: python scripts/tund_10it.py
import math

from reportlab.graphics.shapes import Circle, Drawing, Line, PolyLine, Polygon, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import CondPageBreak, KeepTogether, Spacer

from pdf_common import (BLUE, LINE, NAVY, PALE, WIDTH, Field, build, bullets, c, code, h2, intro, label, label_b,
                        note, p, question, row, sub, title)
from pdf_common import table as plain_table

SUBJECT = '10IT · Sissejuhatus infotehnoloogiasse'
YELLOW = HexColor('#FFD34D')
GREEN = HexColor('#2E8B57')
MUTED = HexColor('#7A8BA3')


def table(*args, **kwargs):
    # The tables here are short, so never split one across pages.
    return KeepTogether([plain_table(*args, **kwargs)])


def subtitle(lesson, kind):
    return p(f'{SUBJECT} · {lesson} · {kind}', sub)


figcap = ParagraphStyle('figcap', fontName='Sans', fontSize=8.5, leading=11, textColor=BLUE, alignment=1,
                        spaceBefore=2, spaceAfter=4)


def figure(drawing, text):
    return KeepTogether([drawing, p(text, figcap), Spacer(1, 6)])


def text(d, x, y, s, size=9, color=NAVY, font='Sans', anchor='middle'):
    d.add(String(x, y, s, fontName=font, fontSize=size, fillColor=color, textAnchor=anchor))


def arrow(d, x1, y1, x2, y2, color=BLUE):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.4))
    ang = math.atan2(y2 - y1, x2 - x1)
    s = 6
    d.add(Polygon([x2, y2, x2 - s * math.cos(ang - 0.4), y2 - s * math.sin(ang - 0.4),
                   x2 - s * math.cos(ang + 0.4), y2 - s * math.sin(ang + 0.4)], fillColor=color, strokeColor=color))


# ---------------------------------------------------------------- joonised

def cpu_drawing():
    d = Drawing(WIDTH, 150)
    # protsessor
    d.add(Rect(10, 30, 150, 105, rx=8, fillColor=PALE, strokeColor=BLUE, strokeWidth=1.4))
    text(d, 85, 118, 'PROTSESSOR', 10, BLUE, 'Sans-Bold')
    for i, (name, val) in enumerate([('A', '8'), ('PC', '2'), ('Käsk', '2F')]):
        y = 90 - i * 24
        d.add(Rect(25, y - 4, 120, 20, rx=4, fillColor=white, strokeColor=LINE))
        text(d, 32, y + 2, name, 8.5, MUTED, anchor='start')
        text(d, 138, y + 2, val, 10, NAVY, 'Mono', anchor='end')
    # mälu
    cells = [('1E', 'LOAD 14'), ('2F', 'ADD 15'), ('50', 'OUT'), ('00', 'HALT'), ('00', ''), ('…', ''), ('05', '= 5'),
             ('03', '= 3')]
    addrs = ['0', '1', '2', '3', '4', '', '14', '15']
    x0, w = 215, 32
    text(d, x0 + 4 * w, 118, 'MÄLU (RAM)', 10, BLUE, 'Sans-Bold')
    for i, ((val, meaning), addr) in enumerate(zip(cells, addrs)):
        x = x0 + i * w
        fill = PALE if i < 4 else white
        d.add(Rect(x, 60, w - 3, 42, rx=4, fillColor=fill, strokeColor=BLUE if i == 2 else LINE,
                   strokeWidth=1.8 if i == 2 else 0.8))
        text(d, x + 4, 93, addr, 7, MUTED, anchor='start')
        text(d, x + (w - 3) / 2, 74, val, 11, NAVY, 'Mono')
        text(d, x + (w - 3) / 2, 48, meaning, 6.5, MUTED)
    arrow(d, x0 - 8, 88, 166, 88)
    text(d, 188, 93, 'too käsk', 8, BLUE)
    arrow(d, 166, 70, x0 - 8, 70)
    text(d, 188, 60, 'kirjuta', 8, BLUE)
    text(d, x0 + 2 * w + 14, 18, 'PC näitab pesale 2: seal on järgmine käsk', 8, MUTED)
    return d


def pixel_drawing():
    smile = ['00111100', '01000010', '10100101', '10000001', '10100101', '10011001', '01000010', '00111100']
    d = Drawing(WIDTH, 150)
    s = 15
    x0, y0 = 40, 135
    for r, line in enumerate(smile):
        for col, bit in enumerate(line):
            d.add(Rect(x0 + col * s, y0 - (r + 1) * s, s, s, fillColor=NAVY if bit == '1' else white,
                       strokeColor=LINE, strokeWidth=0.5))
    arrow(d, x0 + 8 * s + 15, 75, x0 + 8 * s + 60, 75)
    for r, line in enumerate(smile):
        text(d, x0 + 8 * s + 75, y0 - (r + 1) * s + 4, ' '.join(line), 9.5, NAVY, 'Mono', anchor='start')
    return d


def wave_drawing():
    d = Drawing(WIDTH, 140)
    x0, mid, amp, length = 20, 70, 50, WIDTH - 40
    d.add(Line(x0, mid, x0 + length, mid, strokeColor=LINE))
    pts = []
    for i in range(0, 301):
        x = x0 + length * i / 300
        y = mid + amp * (0.7 * math.sin(i / 300 * 4 * math.pi) + 0.3 * math.sin(i / 300 * 11 * math.pi))
        pts += [x, y]
    d.add(PolyLine(pts, strokeColor=MUTED, strokeWidth=1.2))
    for k in range(0, 25):
        i = k * 12.5
        x = x0 + length * i / 300
        y = mid + amp * (0.7 * math.sin(i / 300 * 4 * math.pi) + 0.3 * math.sin(i / 300 * 11 * math.pi))
        d.add(Line(x, mid, x, y, strokeColor=BLUE, strokeWidth=1.6))
        d.add(Circle(x, y, 2.4, fillColor=BLUE, strokeColor=BLUE))
    return d


def network_drawing():
    d = Drawing(WIDTH, 130)

    def box(x, y, w, h, label_text, fill=PALE):
        d.add(Rect(x, y, w, h, rx=6, fillColor=fill, strokeColor=BLUE, strokeWidth=1.2))
        text(d, x + w / 2, y + h / 2 - 3, label_text, 8.5, NAVY, 'Sans-Bold')

    box(5, 60, 70, 32, 'Sinu arvuti')
    box(105, 60, 60, 32, 'Kodu ruuter')
    routers = [(200, 95), (260, 40), (300, 100), (360, 55)]
    for x, y in routers:
        d.add(Circle(x, y, 13, fillColor=white, strokeColor=BLUE, strokeWidth=1.2))
        text(d, x, y - 3, 'R', 9, BLUE, 'Sans-Bold')
    box(395, 60, 70, 32, 'Server')
    links = [((75, 76), (105, 76)), ((165, 76), (187, 92)), ((165, 76), (247, 43)), ((213, 95), (287, 100)),
             ((273, 43), (347, 55)), ((210, 87), (250, 49)), ((313, 98), (350, 64)), ((373, 57), (395, 72)),
             ((313, 100), (395, 82))]
    for (a, b) in links:
        d.add(Line(a[0], a[1], b[0], b[1], strokeColor=MUTED, strokeWidth=1))
    for x, y, n in [(176, 84, '1'), (232, 74, '2'), (330, 75, '3')]:
        d.add(Rect(x - 7, y - 6, 14, 12, rx=2, fillColor=YELLOW, strokeColor=NAVY, strokeWidth=0.6))
        text(d, x, y - 3, n, 7, NAVY, 'Sans-Bold')
    return d


# ---------------------------------------------------------------- 7. tund: protsessor

protsessor = [
    p('Kuidas protsessor programmi täidab', title),
    subtitle('7. tund', 'konspekt'),

    p('Liitja oskab liita. Aga kes vajutab nuppe?', h2),
    p('Eelmises tunnis ehitasime väravatest liitja. Anna talle kaks arvu ja ta liidab need. Kalkulaator töötab '
      'umbes nii: sina vajutad 5, pluss, 3, võrdub ja tema arvutab.'),
    p('Arvuti teeb aga palju rohkem. Ta mängib videot, kontrollib õigekirja, liigutab mängus tegelast. Ja keegi ei '
      'istu tema sees nuppe vajutamas. Kust ta siis teab, mida järgmiseks teha?'),
    p('Vastus on <b>programm</b>. Programm on nimekiri käskudest: „võta see arv“, „liida juurde see“, „näita '
      'tulemust“. Protsessor loeb käske ükshaaval ja teeb täpselt seda, mis kirjas. Huvitav on see, kus see nimekiri '
      'asub ja mis kujul. Tuleb välja, et ka käsud on lihtsalt arvud.'),

    p('Mälu on rida nummerdatud kappe', h2),
    p('Mõtle koolikoridori riidekappidele. Igal kapil on number ja igas kapis on üks asi. Arvuti mälu (RAM, mida '
      'valisid 5. tunnis) on täpselt selline, ainult kappe on miljardeid. Igas kapis on üks bait ehk arv 0 kuni 255, '
      '16-süsteemis 00 kuni FF.'),
    p('Kapi numbrit nimetatakse <b>aadressiks</b>. Kui protsessor tahab mingit arvu, ütleb ta mälule aadressi: „anna '
      'mulle pesa 14 sisu“. Mälu ei tea, mis seal on: arv, täht, pildi täpp või käsk. Ta lihtsalt annab baidi.'),

    p('Meie mänguprotsessor', h2),
    p('Päris protsessor on liiga keeruline, et seda tunniga läbi vaadata. Seepärast on kursuse lehel pisike '
      'mänguprotsessor. See on ehitatud samade põhimõtete järgi, ainult palju väiksem. Tal on:'),
    *bullets(
        '<b>16 mälupesa</b>, aadressid 0 kuni 15;',
        '<b>register A</b>. See on protsessori enda pisike mälu, üks arv, millega ta parasjagu töötab. Nagu arv, '
        'mida hoiad peast arvutades meeles;',
        '<b>PC</b> (ingl <i>program counter</i>) ehk järjehoidja. See on aadress, kust tuleb järgmine käsk.'),
    figure(cpu_drawing(), 'Protsessor ja mälu. Protsessor võtab mälust käske ja andmeid ning kirjutab tulemusi '
                          'tagasi.'),

    p('Käsud on arvud', h2),
    p('Mänguprotsessor oskab ainult kaheksat käsku. See on vähe, aga nagu näed, piisab neist isegi korrutamiseks.'),
    table(['Kood', 'Käsk', 'Mida teeb'], [
        [c('0_'), c('HALT'), 'peatab programmi'],
        [c('1x'), c('LOAD x'), 'A = pesa x sisu'],
        [c('2x'), c('ADD x'), 'A = A + pesa x sisu'],
        [c('3x'), c('SUB x'), 'A = A − pesa x sisu'],
        [c('4x'), c('STORE x'), 'kirjutab A väärtuse pessa x'],
        [c('5_'), c('OUT'), 'paneb A väärtuse väljundisse (ekraanile)'],
        [c('6x'), c('JUMP x'), 'järgmine käsk tuleb pesast x'],
        [c('7x'), c('JZ x'), 'kui A on 0, järgmine käsk tuleb pesast x. Muidu lähe edasi'],
    ], [WIDTH * 0.12, WIDTH * 0.2, WIDTH * 0.68]),
    Spacer(1, 6),
    p('Vaata koodi veergu. Iga käsk on üks bait, kaks 16-süsteemi numbrit. <b>Esimene number ütleb, mida teha, '
      'teine ütleb, millise pesaga.</b> ' + c('LOAD 14') + ' on ' + c('1') + ' (LOAD) ja ' + c('E')
      + ' (14), kokku ' + c('1E') + '. Siin tuleb välja, miks programmeerijad 16-süsteemi armastavad: üks number on '
      'täpselt neli bitti, nii et baidi saab pooleks lõigata ja mõlemad pooled on kohe näha.'),
    p('Sellist arvudest koosnevat programmi nimetatakse <b>masinkoodiks</b>. See on ainus keel, millest protsessor '
      'aru saab. Programm, mis liidab 5 ja 3 ning näitab tulemust, on mälus neli baiti:'),
    table(['Aadress', 'Mälus', 'Tähendab'], [
        ['0', c('1E'), c('LOAD 14') + ': võta A-sse pesa 14 sisu'],
        ['1', c('2F'), c('ADD 15') + ': liida pesa 15 sisu juurde'],
        ['2', c('50'), c('OUT') + ': näita A-d'],
        ['3', c('00'), c('HALT') + ': lõpp'],
        ['14', c('05'), 'arv 5 (andmed, mitte käsk)'],
        ['15', c('03'), 'arv 3'],
    ], [WIDTH * 0.15, WIDTH * 0.15, WIDTH * 0.7]),
    Spacer(1, 6),
    note('<b>Pane tähele:</b> pesas 14 olev ' + c('05') + ' ja pesas 2 olev ' + c('50') + ' on mälu jaoks täpselt '
         'samasugused baidid. Käsuks muutub bait alles siis, kui PC sinna jõuab ja protsessor selle käsuna läbi '
         'loeb. Kui programm kogemata andmete peale jookseb, proovib protsessor neid käskudena täita. Tulemus on '
         'tavaliselt naljakas või katastroofiline.'),

    p('Too, dekodeeri, täida', h2),
    p('Protsessor teeb kogu oma elu ühte ja sama tsüklit. Igal ringil on kolm sammu:'),
    *bullets(
        '<b>Too</b> (ingl <i>fetch</i>): loe mälust bait aadressilt, kuhu PC näitab. Liiguta PC ühe võrra edasi;',
        '<b>Dekodeeri</b> (<i>decode</i>): vaata, mis käsk see on. Siin töötavad väravad, mis bitid lahti '
        'harutavad;',
        '<b>Täida</b> (<i>execute</i>): tee käsk ära. Liitmise teeb sama liitja, mille eelmisel nädalal ehitasime.'),
    p('Vaatame ülemist programmi samm-sammult. Alguses on A = 0 ja PC = 0.'),
    table(['Takt', 'PC', 'Toodud', 'Mida tehti', 'A', 'Väljund'], [
        ['1', '0', c('1E'), 'LOAD 14: A-sse 5', '5', ''],
        ['2', '1', c('2F'), 'ADD 15: 5 + 3', '8', ''],
        ['3', '2', c('50'), 'OUT: näitab 8', '8', '8'],
        ['4', '3', c('00'), 'HALT: peatub', '8', '8'],
    ], [WIDTH * 0.09, WIDTH * 0.08, WIDTH * 0.13, WIDTH * 0.42, WIDTH * 0.1, WIDTH * 0.18]),
    Spacer(1, 6),
    p('Mängus näed sama tabelit elusalt: vajuta „Samm“ ja protsessor kirjutab iga kolme sammu kohta, mida ta tegi.'),

    p('Hüpped: tsüklid ja otsused', h2),
    p('Kui käsud tuleks alati järjest, jookseks iga programm ühe korra läbi ja lõpetaks. Päris programmid kordavad '
      'asju ja teevad otsuseid. Selleks on hüpped.'),
    p(c('JUMP x') + ' paneb PC-sse x-i. Järgmine käsk ei tule enam järgmisest pesast, vaid sealt, kuhu hüppasime. Nii '
      'saab programm minna tagasi algusesse ja sama asja uuesti teha. See on <b>tsükkel</b>.'),
    p(c('JZ x') + ' hüppab ainult siis, kui A on null. See on <b>otsus</b>: kui midagi kehtib, mine sinna, muidu '
      'jätka. Iga ' + c('if') + ', ' + c('for') + ' ja ' + c('while') + ', mida kunagi programmeerides kirjutad, '
      'muutub protsessoris lõpuks selliseks hüppeks.'),
    code('''
0  ADD 15     ; A = A + 1      (pesas 15 on 1)
1  OUT        ; näita A-d
2  JUMP 0     ; mine tagasi algusesse
'''),
    p('See kolmerealine programm loeb 1, 2, 3, 4… ja ei lõpe kunagi. Mängus on see 5. ülesanne. 6. ülesandes '
      'paned ta kümnel peatuma, ja siis läheb vaja ' + c('JZ') + '-i.'),

    p('Takt ja gigahertsid', h2),
    p('Iga tsükli sammu juhib <b>kell</b>: elektriline signaal, mis lööb ühtlases tempos nagu metronoom. Iga löök '
      'on üks <b>takt</b>. Mängus näed taktiloendurit. Kui vajutad „Käivita“, teeb mänguprotsessor umbes kolm takti '
      'sekundis, et jõuaksid silmaga järgi.'),
    p('Nüüd tead lõpuks, mida tähendas PCPartPickeris number 4,5 GHz. Giga on miljard, herts on kord sekundis. '
      '4,5 GHz protsessoril lööb kell <b>4,5 miljardit</b> korda sekundis. Mängu 6. ülesanne võttis 70 takti. Sinu '
      'silme all kulus selleks umbes 20 sekundit, päris protsessoril kuluks 16 nanosekundit.'),
    p('Päris protsessor on veel kiirem, kui gigahertsid ütlevad. Tal on mitu <b>tuuma</b> ja iga tuum on nagu eraldi '
      'protsessor, mis töötab oma programmiga. Iga tuum suudab ühe taktiga teha mitu käsku korraga.'),

    CondPageBreak(200),
    p('Miks keegi masinkoodi ei kirjuta?', h2),
    p('Proovi mängus korrutada ja saad aru. Kaksteist rida selleks, et arvutada 4 × 3! Esimesed programmeerijad '
      'kirjutasid tõesti arve, kuid kiiresti mõeldi välja, kuidas iseennast aidata. Sama programm kolmel tasemel:'),
    table(['Tase', 'Kuidas välja näeb', 'Kes sellest aru saab'], [
        ['Masinkood', c('1E 2F 50 00'), 'protsessor'],
        ['Assembler', c('LOAD 14') + ', ' + c('ADD 15') + ', ' + c('OUT') + ', ' + c('HALT'),
         'inimene, kellel on käsutabel käepärast. Programm nimega <i>assembler</i> teeb sõnadest arvud. Mängus '
         'teeb seda nupp „Lae mällu“'],
        ['Python', c('print(5 + 3)'), 'peaaegu igaüks. Python teeb sellest ise masinkoodi'],
    ], [WIDTH * 0.18, WIDTH * 0.35, WIDTH * 0.47]),
    Spacer(1, 6),
    p('Kui kirjutad Pythonis üheainsa rea, teeb arvuti sellest sadu või tuhandeid masinkoodi käske. Protsessor näeb '
      'ainult neid. Tema jaoks pole kunagi olnud Pythonit, JavaScripti ega Minecrafti. On ainult baidid mälus, PC ja '
      'tsükkel: too, dekodeeri, täida.'),

    p('Sõnastik', h2),
    table(['Sõna', 'Tähendus'], [
        ['<b>aadress</b>', 'mälupesa number'],
        ['<b>register</b>', 'protsessori enda pisike ja väga kiire mälu. Meie mängus on üks: A'],
        ['<b>PC</b>', '<i>program counter</i>: aadress, kust tuleb järgmine käsk'],
        ['<b>käsk</b>', 'üks samm, mida protsessor oskab teha, näiteks LOAD või ADD'],
        ['<b>masinkood</b>', 'programm arvudena, ainus keel, mida protsessor mõistab'],
        ['<b>assembler</b>', 'masinkood sõnadena: LOAD 14 asemel 1E'],
        ['<b>hüpe</b>', 'käsk, mis muudab PC-d. Sellest tulevad tsüklid ja otsused'],
        ['<b>takt</b>', 'üks kella löök. Gigaherts = miljard takti sekundis'],
    ], [WIDTH * 0.2, WIDTH * 0.8]),
]

# ---------------------------------------------------------------- 7. tund: kodutöö


kodutoo = [
    p('Kodutöö: protsessor', title),
    subtitle('7. tund', 'kodutöö'),
    row([p('Nimi', label_b), Field('nimi', 220), '', p('Kuupäev', label_b), Field('kuupaev', 110), ''],
        [51, 220, 18, 51, 110, WIDTH + 12 - 450], PALE),
    Spacer(1, 8),
    p('Täida lahtrid otse kursuse veebilehel: ava fail nupuga „Vaata“, kirjuta vastused ja vajuta „Laadi täidetud PDF '
      'alla“. Saada täidetud fail aadressile <b>mtsopo@taltech.ee</b> enne 10.11. Abiks on konspekt ja veebilehe '
      'protsessorimäng: kõike, mida siin küsitakse, saad mängus järele proovida.', intro),

    p('1. Mis käsk see on?', h2),
    p('Iga bait on üks mänguprotsessori käsk. Kirjuta see assembleris, näiteks ' + c('1E') + ' → ' + c('LOAD 14')
      + '. Käsutabel on konspektis.'),
]
for i, b in enumerate(['1D', '2E', '50', '4C', '3F', '63', '00']):
    kodutoo.append(row([p(c(b), label), Field(f'dek_{i}', 120)], [60, 120]))
kodutoo += [
    p('2. Tee arvuks', h2),
    p('Nüüd vastupidi: kirjuta käsk 16-süsteemi baidina.'),
]
for i, cmd in enumerate(['LOAD 15', 'SUB 14', 'OUT', 'STORE 11', 'JZ 10']):
    kodutoo.append(row([p(c(cmd), label), Field(f'kod_{i}', 60)], [90, 60]))

TRACE = '''
0  LOAD 13
1  ADD 13
2  OUT
3  SUB 14
4  OUT
5  HALT
   ...
13 DAT 6
14 DAT 4
'''
kodutoo += [
    CondPageBreak(330),
    p('3. Ole ise protsessor', h2),
    p('Mälus on see programm. Alguses on A = 0 ja PC = 0. Täida tabel: mis on A pärast igat takti ja mis tuleb '
      'väljundisse. Esimene rida on tehtud.'),
    code(TRACE),
    row([p('<b>Takt</b>', label), p('<b>Käsk</b>', label), p('<b>A pärast</b>', label), p('<b>Väljund</b>', label)],
        [50, 110, 80, 120]),
    row([p('1', label), p(c('LOAD 13'), label), p('6', label), p('–', label)], [50, 110, 80, 120]),
]
for i, cmd in enumerate(['ADD 13', 'OUT', 'SUB 14', 'OUT']):
    kodutoo.append(row([p(str(i + 2), label), p(c(cmd), label), Field(f'jalg_a_{i}', 60), '',
                        Field(f'jalg_out_{i}', 100)], [50, 110, 60, 20, 100]))
kodutoo += [
    Spacer(1, 8),
    CondPageBreak(250),
    p('4. Leia viga', h2),
    question('<b>a)</b> Mari tahtis näha väljundis 9, aga väljund jääb tühjaks. Miks? Kuidas parandada?', 'viga_a', 40,
             extra=[code('''
0  LOAD 14     ; pesas 14 on 7
1  ADD 15      ; pesas 15 on 2
2  HALT
3  OUT
''')]),
    question('<b>b)</b> Mängus peatub programm ka siis, kui HALT on puudu ja programm jõuab tühja pessa. Miks? '
             'Vihje: mis arv on tühjas pesas ja mis käsk see on?', 'viga_b', 40),

    p('5. Kirjuta ise', h2),
    question('Pesas 15 on arv 10. Kirjuta programm, mis paneb väljundisse 10, 20 ja 30 ning peatub. Proovi see mängus '
             'järele. Mängus pane arv 10 programmi lõppu reaga ' + c('DAT 10') + ' ja kasuta 15 asemel selle rea '
             'aadressi.', 'ise', 90),
    question('<b>6. Arvuta.</b> Sinu arvuti protsessor teeb 4 miljardit takti sekundis. Mänguprotsessor teeb 3 takti '
             'sekundis. Kui kaua peaks mänguprotsessor töötama, et teha sama palju takte kui päris protsessor ühe '
             'sekundiga? Kirjuta ka arvutuskäik.', 'arvuta', 56),
]

# ---------------------------------------------------------------- 8. tund: pildid ja heli

pildid = [
    p('Pildid ja heli arvudena', title),
    subtitle('8. tund', 'konspekt'),

    p('Kuidas foto arvutisse mahub?', h2),
    p('Teed telefoniga pildi koolisööklast. Sekundi pärast on see saadetud sõbrale teise linna. Aga mööda kaablit ei '
      'saa saata supitaldrikut ega isegi värve. Mööda kaablit liiguvad ainult bitid, nullid ja ühed. Kuidas siis pilt '
      'arvudeks muutub? Teksti puhul (3. tund) leppisime kokku, et iga täht on üks arv. Piltide ja heliga tehakse '
      'täpselt sama trikki, ainult arve on palju rohkem.'),

    p('Pilt on ruudustik', h2),
    p('Suumi mõnda pilti telefonis nii palju kui saad. Ühel hetkel muutub pilt ruuduliseks. Iga ruut on ühte värvi '
      'ja seda ruutu nimetatakse <b>piksliks</b> (ingl <i>picture element</i>). Pilt ongi ainult pikslite ruudustik. '
      'Mida rohkem piksleid, seda väiksemad on ruudud ja seda teravam on pilt.'),
    p('Kõige lihtsam pilt on mustvalge. Siis on igal pikslil kaks võimalust ja selleks piisab ühest bitist: 1 on must, '
      '0 on valge. Kaheksa korda kaheksa pikslit, 64 bitti ehk 8 baiti:'),
    figure(pixel_drawing(), 'Naerunägu: igal pikslil üks bitt. Arvuti hoiab ainult paremal olevaid arve.'),
    p('Pane tähele, et arvuti ei tea, et see on naerunägu. Tal on 8 baiti. Pildiks muutuvad need alles siis, kui '
      'keegi kokkuleppe järgi ruudustiku joonistab.'),

    p('Värvid: punane, roheline, sinine', h2),
    p('Värvipildis ei piisa ühest bitist. 2. tunnis nägid veebivärve nagu ' + c('#FF8800') + '. Iga piksel ongi '
      'kolm arvu: kui palju on punast (R), rohelist (G) ja sinist (B) valgust. Igaüks on üks bait ehk 0 kuni 255. '
      'Sinu ekraanil on iga piksli sees päriselt kolm pisikest lampi: punane, roheline ja sinine. Võta suurendusklaas '
      'ja vaata!'),
    table(['Värv', 'R', 'G', 'B', '16-süsteemis'], [
        ['must', '0', '0', '0', c('#000000')],
        ['valge', '255', '255', '255', c('#FFFFFF')],
        ['punane', '255', '0', '0', c('#FF0000')],
        ['kollane', '255', '255', '0', c('#FFFF00')],
        ['oranž', '255', '136', '0', c('#FF8800')],
    ], [WIDTH * 0.32, WIDTH * 0.12, WIDTH * 0.12, WIDTH * 0.12, WIDTH * 0.32]),
    Spacer(1, 6),
    p('Kolm baiti pikslis annab 256 × 256 × 256 ehk umbes 16,7 miljonit värvi. See on rohkem, kui inimsilm eristada '
      'suudab.'),

    p('Kui suur on üks pilt?', h2),
    p('Nüüd saame arvutada. Täis-HD ekraan on 1920 pikslit lai ja 1080 kõrge:'),
    code('''
1920 × 1080 = 2 073 600 pikslit
2 073 600 × 3 baiti = 6 220 800 baiti ≈ 6,2 MB
'''),
    p('Telefoni kaamera teeb 12-megapikslise pildi. 12 miljonit pikslit korda kolm baiti on 36 MB. Aga vaata oma '
      'galeriis: üks foto on umbes 3 MB. Kus ülejäänu on?'),

    p('Pakkimine: kuidas 36 MB-st saab 3 MB', h2),
    p('Mõtle pildile, kus on sinine taevas. Tuhanded pikslid järjest on täpselt sama värvi. Selle asemel, et kirjutada '
      '„sinine, sinine, sinine…“ tuhat korda, võib kirjutada „1000 korda sinine“. See on <b>pakkimine</b>: sama '
      'info kirjutatakse lühemalt. Midagi ei lähe kaotsi. Nii töötab PNG ja selliseid vorminguid nimetatakse '
      '<b>kadudeta</b> pakkimiseks.'),
    p('JPEG läheb kavalamaks. Ta viskab ära detailid, mida silm niikuinii ei märka: pisikesed värvierinevused, '
      'teravad üleminekud. Pilt jääb samasugune, aga fail on kümme korda väiksem. See on <b>kadudega</b> pakkimine. '
      'Kui JPEG-i mitu korda salvestad ja jälle saadad, kaob iga kord natuke ja lõpuks on pilt plekiline. Kõik on '
      'näinud mõnda meemi, mis on nii palju ringelnud, et pole enam loetav.'),
    table(['Vorming', 'Pakkimine', 'Sobib'], [
        ['BMP', 'üldse ei paki', 'peaaegu millekski, liiga suur'],
        ['PNG', 'kadudeta', 'ekraanipildid, logod, tekst pildil'],
        ['JPEG', 'kadudega', 'fotod'],
        ['WebP, AVIF', 'mõlemat moodi', 'veebilehed: uuemad ja väiksemad'],
    ], [WIDTH * 0.2, WIDTH * 0.3, WIDTH * 0.5]),

    p('Heli: õhu värisemine', h2),
    p('Heli on õhu värisemine. Kui kitarrikeel võngub, lükkab see õhku edasi-tagasi ja see liikumine jõuab sinu '
      'kõrva. Mikrofon teeb sama asja vastupidi: õhk liigutab tema sees pisikest membraani ja sellest tekib '
      'elektrivool, mis tõuseb ja langeb täpselt nagu heli. Joonisel on hall joon see laine.'),
    p('Laine on sujuv, aga arvuti oskab hoida ainult arve. Seepärast mõõdab ta laine kõrgust kindlate vahedega ja '
      'kirjutab iga mõõtmise arvuna üles. Iga sinine täpp on üks mõõtmine. Seda nimetatakse <b>diskreetimiseks</b> '
      '(ingl <i>sampling</i>).'),
    figure(wave_drawing(), 'Hall: päris helilaine. Sinised: mõõtmised, mida arvuti hoiab.'),
    p('Muusika jaoks mõõdetakse <b>44 100 korda sekundis</b>. Miks nii palju? Inimene kuuleb kuni umbes 20 000 '
      'võnget sekundis ja ühe võnke kirjeldamiseks on vaja vähemalt kahte mõõtmist. Iga mõõtmine on 16 bitti ehk 2 '
      'baiti. Ja stereos on kaks kanalit, vasak ja parem kõrv.'),
    code('''
44 100 × 2 baiti × 2 kanalit = 176 400 baiti sekundis
176 400 × 60 sekundit ≈ 10,6 MB minutis
'''),
    p('Kolmeminutiline laul oleks seega üle 30 MB. MP3 ja Spotify kasutavad jälle kadudega pakkimist. Ära visatakse '
      'helid, mida kõrv ei kuule, näiteks vaikne heli kohe valju heli kõrval. Tulemus on umbes 1 MB minutis.'),

    p('Video: palju pilte järjest', h2),
    p('Video on lihtsalt pildid, mida näidatakse nii kiiresti, et silm ei jõua neid eristada. Tavaliselt 30 kaadrit '
      'sekundis. Arvutame ilma pakkimiseta:'),
    code('''
6,2 MB (üks täis-HD kaader) × 30 kaadrit = 186 MB sekundis
'''),
    p('Kahetunnine film oleks üle 1,3 terabaidi. Netflix saadab sama filmi umbes 3 GB-ga. Videopakkimine on veel '
      'kavalam: kaks järjestikust kaadrit on peaaegu samad, nii et saadetakse ainult see, mis muutus. Kui uudiste '
      'saates liigub ainult diktori suu, siis saadetaksegi peamiselt suud.'),

    p('Sõnastik', h2),
    table(['Sõna', 'Tähendus'], [
        ['<b>piksel</b>', 'pildi väikseim ruut, ühte värvi'],
        ['<b>resolutsioon</b>', 'mitu pikslit on pildil laiuses ja kõrguses, näiteks 1920 × 1080'],
        ['<b>RGB</b>', 'värv kolme arvuna: punane, roheline, sinine'],
        ['<b>pakkimine</b>', 'sama info kirjutamine vähemate baitidega'],
        ['<b>kadudeta</b>', 'pakkimine, kus midagi ei lähe kaotsi (PNG, ZIP)'],
        ['<b>kadudega</b>', 'pakkimine, mis viskab ära detailid, mida ei märka (JPEG, MP3)'],
        ['<b>diskreetimine</b>', 'helilaine mõõtmine kindlate vahedega'],
        ['<b>kaader</b>', 'üks pilt videost'],
    ], [WIDTH * 0.22, WIDTH * 0.78]),
]

# ---------------------------------------------------------------- 10.–11. tund: internet

internet = [
    p('Kuidas internet töötab', title),
    subtitle('10. ja 11. tund', 'konspekt'),

    p('Kust see video tuleb?', h2),
    p('Klõpsad YouTube’is videol ja sekundi pärast see mängib. Video ei olnud sinu telefonis. See oli kuskil teises '
      'riigis, serveris, mille asukohta sa ei tea. Selle sekundi jooksul läks sinu küsimus sinna ja video tuli tagasi, '
      'läbides tõenäoliselt kümmekond arvutit ja võib-olla ka merepõhjas oleva kaabli.'),
    p('Internetti nimetatakse tihti pilveks, nagu oleks see miski õhus. Päriselt on internet kaablid, raadiolained ja '
      'arvutid, mis neid omavahel ühendavad. Eestist Soome viivad näiteks mitu kaablit mööda Soome lahe põhja.'),

    p('Võrk ja võrkude võrk', h2),
    p('Kui ühendad kaks arvutit omavahel, on sul <b>võrk</b>. Sinu kodus on väike võrk: telefon, sülearvuti ja '
      'teler on ühendatud WiFi kaudu kodusesse <b>ruuterisse</b>. Koolis on suurem võrk. Ruuter on võrgu '
      'liikluspolitseinik: ta teab, mis tema taga on, ja saadab kõik muu edasi internetiteenuse pakkujale, näiteks '
      'Telia või Elisa.'),
    p('Internet on kõigi nende võrkude ühendus. Sõna ise ütleb seda: <i>inter-net</i>, võrkude vaheline. Ükski '
      'firma ega riik ei oma tervet internetti. On tuhanded võrgud, kes on kokku leppinud, et nad edastavad üksteise '
      'andmeid.'),

    p('IP-aadress', h2),
    p('Et kiri kohale jõuaks, on vaja aadressi. Internetis on igal seadmel <b>IP-aadress</b>. Vanem kuju, IPv4, '
      'näeb välja nii:'),
    code('193.40.250.10'),
    p('Neli arvu, igaüks 0 kuni 255. Kas tuleb tuttav ette? Iga arv on üks bait, kokku 4 baiti ehk 32 bitti. 32 '
      'bitiga saab teha 2³² ehk umbes 4,3 miljardit erinevat aadressi. Kui internet leiutati, tundus see lõputu. '
      'Täna on Maal rohkem nutiseadmeid kui inimesi ja aadressid said otsa. Seepärast on uus IPv6, kus aadress on '
      '128 bitti. Neid jätkub igale liivaterale Maal.'),
    note('<b>Proovi:</b> ava terminal ja kirjuta ' + c('ipconfig') + ' (Macis ' + c('ifconfig') + '). Leia rida '
         + c('IPv4 Address') + '. See on sinu arvuti aadress koolivõrgus. Kas pinginaabril on sama?'),

    p('Paketid', h2),
    p('Kujuta ette, et pead saatma terve raamatu, aga postkontor võtab ainult postkaarte. Mida teed? Kirjutad raamatu '
      'postkaartidele, igale kaardile lehekülje numbri ja saaja aadressi. Kaardid võivad minna eri teid ja jõuda '
      'kohale suvalises järjekorras. Saaja paneb need numbrite järgi kokku. Kui mõni kaduma läheb, palub ta selle '
      'uuesti saata.'),
    p('Internet töötab täpselt nii. Iga fail, pilt ja video tükeldatakse <b>pakettideks</b>, igaüks umbes 1500 '
      'baiti. Igal paketil on saatja ja saaja IP-aadress ning järjekorranumber.'),
    figure(network_drawing(), 'Teel serverini läbib pakett mitu ruuterit (R). Paketid 1, 2 ja 3 võivad minna eri '
                              'teid, server paneb need numbrite järgi kokku.'),
    p('Ükski ruuter ei tea kogu teed. Iga ruuter vaatab paketi saaja aadressi ja otsustab ainult: „see läheb sinna '
      'naabrile“. Täpselt nagu linnas teed küsides: iga inimene näitab ainult järgmise ristmikuni.'),
    note('<b>Proovi:</b> terminalis ' + c('tracert google.com') + ' (Macis ' + c('traceroute google.com')
         + '). Iga rida on üks ruuter teel Google’i serverini. Mitu sammu tuli? Kas mõnes nimes on näha linna või '
         'riiki?'),

    p('DNS: internetisõnastik', h2),
    p('IP-aadresse on raske meeles pidada. Keegi ei taha kirjutada ' + c('142.250.74.46') + ', kui tahab Google’isse '
      'minna. Seepärast on olemas <b>DNS</b> (<i>Domain Name System</i>). See on nagu telefoniraamat: annad nime, '
      'saad numbri.'),
    p('Kui kirjutad aadressiribale ' + c('youtube.com') + ', küsib arvuti kõigepealt DNS-serverilt: „mis on '
      'youtube.com-i IP-aadress?“ Alles siis, kui vastus käes, saab ta päris päringu teele saata.'),
    note('<b>Proovi:</b> ' + c('nslookup tahvel.edu.ee') + '. Mis IP-aadressi DNS andis?'),

    p('Mis juhtub, kui avad veebilehe?', h2),
    p('Paneme kõik kokku. Kirjutad ' + c('tahvel.edu.ee') + ' ja vajutad Enterit:'),
    table(['Samm', 'Mis toimub'], [
        ['1. DNS', 'Arvuti küsib DNS-ilt: mis on tahvel.edu.ee IP-aadress? Saab vastuseks neli arvu.'],
        ['2. Ühendus', 'Arvuti võtab selle IP-aadressiga ühendust. Paketid lähevad läbi ruuterite.'],
        ['3. Päring', 'Brauser saadab <b>HTTP</b> päringu: „anna mulle avaleht“.'],
        ['4. Vastus', 'Server saadab HTML-i, pildid ja muu. Kõik pakettidena, tükkhaaval.'],
        ['5. Joonistamine', 'Brauser paneb paketid kokku ja joonistab lehe ekraanile.'],
    ], [WIDTH * 0.2, WIDTH * 0.8]),
    Spacer(1, 6),
    p('Kogu see teekond võtab tavaliselt alla sekundi.'),

    p('HTTPS ja lukk', h2),
    p('Pakett läbib teel kümmet võõrast arvutit. Kas nad saavad sisse vaadata? Tavalise HTTP puhul saavad, nagu '
      'postiljon saab lugeda postkaarti. Seepärast kasutab peaaegu iga leht täna <b>HTTPS</b>-i. S tähendab '
      '<i>secure</i>. Kõik paketid krüpteeritakse: postkaart pannakse lukustatud karpi ja võtme on ainult sinul ja '
      'serveril. Lukuikoon aadressiribal tähendab, et ühendus on krüpteeritud.'),
    note('<b>Tähtis:</b> lukk tähendab, et keegi ei saa teel pealt kuulata. See <b>ei</b> tähenda, et leht on aus. '
         'Ka petulehel võib olla lukk. Kontrolli alati, kas aadress on õige: ' + c('swedbank.ee') + ', mitte '
         + c('swedbank-ee.info') + '.'),

    p('Kiirus: megabitid ja millisekundid', h2),
    p('Internetipakkuja lubab „100 megabitti“. Allalaadimine näitab aga 12 MB/s. Kas petavad? Ei. Pakkuja loeb '
      '<b>bitte</b>, allalaadimine baite. Bait on 8 bitti: 100 ÷ 8 = 12,5. Pane tähele, et väike b on bitt ja suur '
      'B on bait.'),
    p('Kiirusel on ka teine pool: <b>viivitus</b> (ingl <i>latency</i>, mängurid ütlevad <i>ping</i>). See on aeg, '
      'mis kulub paketil kohale jõudmiseks ja tagasi. Valgus liigub klaaskiukaablis umbes 200 000 km sekundis. '
      'Tallinnast New Yorki on umbes 7000 km, nii et ainuüksi tee võtab 35 ms ühte ja 70 ms edasi-tagasi. Kiiremaks '
      'seda ei tee ükski pakkuja, sest valguse kiirust ei saa muuta. Seepärast on mänguserverid igas maailmajaos '
      'eraldi.'),
    note('<b>Proovi:</b> ' + c('ping google.com') + ' ja ' + c('ping google.co.jp') + '. Kumb vastab kiiremini? '
         'Miks?'),

    p('Sõnastik', h2),
    table(['Sõna', 'Tähendus'], [
        ['<b>võrk</b>', 'omavahel ühendatud arvutid'],
        ['<b>internet</b>', 'võrkude võrk, mis katab kogu maailma'],
        ['<b>ruuter</b>', 'seade, mis saadab pakette õiges suunas edasi'],
        ['<b>IP-aadress</b>', 'seadme number internetis, nt 193.40.250.10'],
        ['<b>pakett</b>', 'väike andmetükk koos saatja ja saaja aadressiga'],
        ['<b>DNS</b>', 'teenus, mis teeb nimest (youtube.com) IP-aadressi'],
        ['<b>HTTP / HTTPS</b>', 'veebilehtede päringute keel. S tähendab krüpteeritud'],
        ['<b>viivitus</b>', 'aeg, mis kulub paketil kohale ja tagasi, millisekundites'],
    ], [WIDTH * 0.22, WIDTH * 0.78]),
]


if __name__ == '__main__':
    build('public/files/protsessor-konspekt.pdf', 'Kuidas protsessor programmi täidab',
          f'{SUBJECT} · Kuidas protsessor programmi täidab', protsessor, SUBJECT)
    build('public/files/kodutoo-protsessor.pdf', 'Kodutöö: protsessor', f'{SUBJECT} · Kodutöö: protsessor', kodutoo,
          SUBJECT)
    build('public/files/pildid-heli-konspekt.pdf', 'Pildid ja heli arvudena', f'{SUBJECT} · Pildid ja heli arvudena',
          pildid, SUBJECT)
    build('public/files/internet-konspekt.pdf', 'Kuidas internet töötab', f'{SUBJECT} · Kuidas internet töötab',
          internet, SUBJECT)
