# Builds the 10IT PDFs for lessons 7-11 in public/files/:
#   protsessor-konspekt.pdf, kodutoo-protsessor.pdf (fillable),
#   pildid-heli-konspekt.pdf, kodutoo-pildid.pdf (fillable),
#   pakkimine-konspekt.pdf, kodutoo-pakkimine.pdf (fillable) and internet-konspekt.pdf.
# Needs ReportLab (pip install reportlab) and the macOS system fonts Arial and Menlo.
# Run from the project root: python scripts/tund_10it.py
# To build only some of them: python scripts/tund_10it.py pildid-heli-konspekt kodutoo-pildid
import math
import sys

from reportlab.graphics.shapes import Circle, Drawing, Line, PolyLine, Polygon, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import CondPageBreak, KeepTogether, Paragraph, Spacer

from pdf_common import (BLUE, LINE, NAVY, PALE, WIDTH, Field, build, bullet, bullets, c, code, h2, intro, label,
                        label_b, note, p, question, row, sub, title)
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


def proovi(number, text_):
    return note(f'<b>Proovi ise {number}.</b> {text_}')


def intro_box(text_):
    return note(text_)


def numbered(items):
    return [Paragraph(i, bullet, bulletText=f'{n}.') for n, i in enumerate(items, 1)]


ARROW = ['00011000', '00111100', '01111110', '11111111', '00011000', '00011000', '00011000', '00011000']


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


def bit_grid(d, rows, x0, top, s, on=NAVY):
    for r, line in enumerate(rows):
        for col, bit in enumerate(line):
            d.add(Rect(x0 + col * s, top - (r + 1) * s, s, s, fillColor=on if bit == '1' else white,
                       strokeColor=LINE, strokeWidth=0.5))


def arrow_picture():
    d = Drawing(WIDTH, 136)
    bit_grid(d, ARROW, (WIDTH - 128) / 2, 132, 16)
    return d


def subpixel_drawing():
    d = Drawing(WIDTH, 112)
    x0 = 30
    for r in range(4):
        for col in range(6):
            d.add(Rect(x0 + col * 16, 96 - (r + 1) * 16, 16, 16, fillColor=HexColor('#FF8800'), strokeColor=white,
                       strokeWidth=0.6))
    d.add(Rect(x0 + 32, 96 - 32, 16, 16, fillColor=None, strokeColor=NAVY, strokeWidth=1.4))
    text(d, x0 + 48, 16, 'oranž ala ekraanil', 8.5, BLUE)
    arrow(d, x0 + 106, 56, x0 + 150, 56)
    lamps = [('R = 255', HexColor('#FF0000')), ('G = 136', HexColor('#008800')), ('B = 0', HexColor('#D6DEEA'))]
    for i, (name, colour) in enumerate(lamps):
        x = x0 + 165 + i * 72
        d.add(Rect(x, 30, 56, 64, fillColor=colour, strokeColor=LINE))
        text(d, x + 28, 16, name, 9, NAVY, 'Mono')
    return d


def resolution_drawing():
    d = Drawing(WIDTH, 128)
    for i, n in enumerate([8, 16, 48]):
        size = 96
        x0 = 30 + i * (size + 52)
        s = size / n
        for r in range(n):
            for col in range(n):
                dx, dy = (col + 0.5) / n - 0.5, (r + 0.5) / n - 0.5
                if dx * dx + dy * dy < 0.2:
                    d.add(Rect(x0 + col * s, 120 - (r + 1) * s, s, s, fillColor=BLUE, strokeColor=None))
        d.add(Rect(x0, 24, size, size, fillColor=None, strokeColor=LINE))
        text(d, x0 + size / 2, 8, f'{n} × {n}', 9, NAVY, 'Mono')
    return d


def sampling_compare():
    def wave(i):
        return 0.7 * math.sin(i * 4 * math.pi) + 0.3 * math.sin(i * 11 * math.pi)

    d = Drawing(WIDTH, 112)
    for k, (samples, name) in enumerate([(9, 'vähe mõõtmisi'), (49, 'palju mõõtmisi')]):
        width = WIDTH / 2 - 16
        x0, mid, amp = 4 + k * (width + 24), 58, 40
        d.add(PolyLine([v for i in range(201) for v in (x0 + width * i / 200, mid + amp * wave(i / 200))],
                       strokeColor=MUTED, strokeWidth=1))
        steps = []
        for j in range(samples):
            y = mid + amp * wave(j / (samples - 1))
            x = x0 + width * j / (samples - 1)
            steps += [x, y, min(x + width / (samples - 1), x0 + width), y]
        d.add(PolyLine(steps, strokeColor=BLUE, strokeWidth=1.5))
        text(d, x0 + width / 2, 4, name, 9, NAVY)
    return d


def rle_row(d, row, x0, y, s):
    for i, ch in enumerate(row):
        d.add(Rect(x0 + i * s, y, s, s, fillColor=NAVY if ch == 'M' else white, strokeColor=LINE, strokeWidth=0.7))


def rle_drawing(rows):
    d = Drawing(WIDTH, 28 * len(rows))
    for n, (row, packed) in enumerate(rows):
        y = (len(rows) - n - 1) * 28 + 4
        rle_row(d, row, 4, y, 20)
        arrow(d, 4 + len(row) * 20 + 10, y + 10, 4 + len(row) * 20 + 40, y + 10)
        text(d, 4 + len(row) * 20 + 50, y + 6, packed, 10, NAVY, 'Mono', anchor='start')
    return d


def flag_drawing():
    d = Drawing(WIDTH, 80)
    s = 12
    x0 = (WIDTH - 12 * s) / 2
    colours = [HexColor('#0072CE')] * 2 + [HexColor('#000000')] * 2 + [white] * 2
    for r, colour in enumerate(colours):
        for col in range(12):
            d.add(Rect(x0 + col * s, 76 - (r + 1) * s, s, s, fillColor=colour, strokeColor=LINE, strokeWidth=0.4))
    return d


def jpeg_block_drawing():
    values = [[182, 184, 183, 186], [181, 185, 184, 183], [186, 182, 185, 184], [183, 184, 182, 185]]
    mean = round(sum(map(sum, values)) / 16)
    d = Drawing(WIDTH, 112)
    s = 24
    for k, x0 in enumerate([40, 280]):
        for r in range(4):
            for col in range(4):
                v = values[r][col] if k == 0 else mean
                d.add(Rect(x0 + col * s, 104 - (r + 1) * s, s, s, fillColor=HexColor(f'#{v:02X}{v:02X}{v:02X}'),
                           strokeColor=white, strokeWidth=0.5))
                text(d, x0 + col * s + s / 2, 104 - (r + 1) * s + 8, str(v), 8, NAVY, 'Mono')
    arrow(d, 150, 56, 270, 56)
    text(d, 210, 62, 'väikesed erinevused kaovad', 8.5, BLUE)
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
      'alla“. Saada täidetud fail aadressile <b>mtsopo@taltech.ee</b> enne 03.11. Abiks on konspekt ja veebilehe '
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

    intro_box('Selle konspekti lugemiseks ei pea sa midagi ette teadma. Kõik sõnad selgitan ära siis, kui neid esimest '
              'korda vaja läheb, ja arvutused teeme samm-sammult läbi. Lahenda „Proovi ise“ kastid ja võrdle vastust '
              'konspekti lõpus olevatega. Mängi samal ajal veebilehel <b>Pildilaborit</b>.<br/><br/>'
              '<b>Pärast seda tundi oskad:</b><br/>'
              '• kirjutada mustvalge piksli rea arvudena ja RGB-värvi koodina;<br/>'
              '• arvutada pakkimata pildi andmemahu;<br/>'
              '• arvutada pakkimata heli andmemahu.<br/><br/>'
              'Need kolm ongi kõige tähtsamad. Video osa on lisateema.'),

    p('Kuidas foto arvutisse mahub?', h2),
    p('Teed telefoniga pildi koolisööklast. Sekundi pärast on see sõbra telefonis teises linnas. Kaablit mööda ei saa '
      'aga saata supitaldrikut. Isegi mitte värve.'),
    p('Arvuti teab ainult arve. Nii et kuskil peab pilt arvudeks muutuma, ja sama juhtub laulu ning videoga. Just seda '
      'trikki me täna lahti võtamegi. Pärast seda oskad ise välja arvutada, kui palju ruumi üks pakkimata pilt võtab.'),

    p('Neli sõna, mida läheb vaja', h2),
    p('Kui oled neid varem kuulnud, on see kiire meeldetuletus. Kui mitte, siis siit saad kõik vajaliku.'),
    table(['Sõna', 'Mis see on'], [
        ['<b>bitt</b>', 'Väikseim infokogus arvutis. Üks lüliti, mis on kas väljas (0) või sees (1).'],
        ['<b>bait</b>', '8 bitti koos. Ühe baidiga saab kirjutada arve 0 kuni 255, kokku 256 eri väärtust.'],
        ['<b>KB, MB, GB, TB</b>', 'Nendes materjalides kasutame kümnendühikuid: 1 KB = 1000 baiti, 1 MB = 1 000 000 '
                                  'baiti, 1 GB = 1000 MB ja 1 TB = 1000 GB.'],
        ['<b>kuueteist-<br/>kümnendsüsteem</b>', 'Lühidalt 16-süsteem. Arvude kirjutamise viis, kus numbreid on kuusteist: '
                                            '0–9 ja siis A, B, C, D, E, F. A tähendab 10 ja F tähendab 15. Ühe baidi '
                                            'saab kirjutada kahe sellise märgiga.'],
    ], [WIDTH * 0.24, WIDTH * 0.76]),

    p('Pilt on ruudustik', h2),
    p('Suurenda telefonis mõnda pilti nii palju, kui saad. Mingil hetkel muutub see ruuduliseks, nagu matemaatikavihik, '
      'kus iga ruut on ühte värvi värvitud. Sellist ruutu nimetatakse <b>piksliks</b>. Sõna tuleb inglise keelest: '
      '<i>picture element</i>, pildi osake.'),
    p('Rohkem pole seal midagi. Ükskõik milline foto on lihtsalt väga palju väikseid ühevärvilisi ruute.'),
    p('Võtame kõige lihtsama juhtumi. Siin tähendab mustvalge pilt pilti, mille piksel on kas täiesti must või täiesti '
      'valge. Halltoone selles näites ei ole. Igal pikslil on seega kaks võimalust ja selleks piisab ühest bitist. '
      'Lepime kokku, et 1 on must ja 0 on valge. Siin on 8 pikslit lai ja 8 pikslit kõrge pilt:'),
    figure(pixel_drawing(), 'Vasakul see, mida sina näed. Paremal see, mida arvuti tegelikult hoiab.'),
    p('Vaata ülemist rida: ' + c('0 0 1 1 1 1 0 0') + '. Kaks valget, neli musta, kaks valget. Võrdle joonisega ja leia '
      'need ruudud üles. Kui saad sellest reast aru, oled pildifaili põhiidee juba kätte saanud.'),
    p('Ja pane tähele üht veidrat asja: arvuti ei tea, et see on naerunägu. Tal on lihtsalt arvud. Pilt tekib alles '
      'siis, kui keegi need kokkuleppe järgi ruudustikuks joonistab.'),
    p('Kui palju ruumi see pilt võtab? Arvutame:'),
    code('''
1. samm: pikslite arv     8 × 8 = 64 pikslit
2. samm: bittide arv      64 pikslit × 1 bitt = 64 bitti
3. samm: baitide arv      64 : 8 = 8 baiti       (sest 1 bait = 8 bitti)
'''),
    proovi('1', 'Mustvalge pilt on 16 pikslit lai ja 8 pikslit kõrge. Mitu pikslit, mitu bitti ja mitu baiti see on? '
                'Ava siis Pildilaboris vaheleht <b>Bitipilt</b> ja klõpsa ruutudel: näed, kuidas read arvudeks muutuvad.'),

    p('Kuidas rida 16-süsteemi kirjutada', h2),
    p('Kaheksat nulli ja ühte on tülikas välja kirjutada. Seepärast kirjutavad programmeerijad baidi tavaliselt kahe '
      '16-süsteemi märgina. See käib nii: jaga 8 bitti pooleks ja vaata kumbki pool allolevast tabelist järele.'),
    table(['Bitid', 'Märk', 'Bitid', 'Märk', 'Bitid', 'Märk', 'Bitid', 'Märk'], [
        ['0000', '0', '0100', '4', '1000', '8', '1100', 'C'],
        ['0001', '1', '0101', '5', '1001', '9', '1101', 'D'],
        ['0010', '2', '0110', '6', '1010', 'A', '1110', 'E'],
        ['0011', '3', '0111', '7', '1011', 'B', '1111', 'F'],
    ], [WIDTH / 8] * 8),
    Spacer(1, 6),
    p('Võtame naerunäo ülemise rea:'),
    code('''
00111100          kirjutame kaheks pooleks
0011 | 1100       vaatame tabelist: 0011 on 3 ja 1100 on C
3C                vastus
'''),
    proovi('2', 'Kirjuta 16-süsteemis read ' + c('01100110') + ' ja ' + c('11110000') + '.'),

    p('Värvid: punane, roheline, sinine', h2),
    p('Värvipildis ühest bitist ei piisa. Selles tunnis kasutame RGB-mudelit: RGB-värvipildis kirjeldame iga piksli '
      'värvi kolme arvuga, punase (R, ingl <i>red</i>), rohelise (G, <i>green</i>) ja sinise (B, <i>blue</i>) '
      'väärtusega.'),
    p('Lihtsustatult võib tüüpilist ekraani ette kujutada nii, et iga piksel koosneb kolmest pisikesest lambist: '
      'punasest, rohelisest ja sinisest. Kaugelt silm neid enam eraldi ei erista ja näeb segu. Iga lambi ereduse jaoks '
      'on üks bait, seega arv 0-st (lamp ei põle) kuni 255-ni (põleb täie jõuga).'),
    figure(subpixel_drawing(), 'Üks oranž piksel: punane lamp täiega, roheline umbes poole peal, sinine ei põle.'),
    table(['Värv', 'R', 'G', 'B', '16-süsteemis'], [
        ['must (kõik lambid kustus)', '0', '0', '0', c('#000000')],
        ['valge (kõik täiega)', '255', '255', '255', c('#FFFFFF')],
        ['punane', '255', '0', '0', c('#FF0000')],
        ['kollane (punane + roheline)', '255', '255', '0', c('#FFFF00')],
        ['oranž', '255', '136', '0', c('#FF8800')],
    ], [WIDTH * 0.40, WIDTH * 0.10, WIDTH * 0.10, WIDTH * 0.10, WIDTH * 0.30]),
    Spacer(1, 6),
    p('Veebilehtede värvikood, näiteks ' + c('#FF8800') + ', ongi need samad kolm baiti 16-süsteemis: ' + c('FF')
      + ' on punane, ' + c('88') + ' roheline, ' + c('00') + ' sinine. Kuidas tavalisest arvust selline kood saada? Jaga '
      '16-ga. Täisosa annab esimese märgi ja jääk teise:'),
    code('''
136 : 16 = 8, jääk 8     märgid on 8 ja 8    →  88
255 : 16 = 15, jääk 15   15 on F, seega      →  FF
 10 : 16 = 0, jääk 10    10 on A, seega      →  0A
'''),
    p('Vastupidi käib nii: korruta esimese märgi arvväärtus 16-ga ja liida teise märgi arvväärtus. ' + c('88')
      + ' on 8 × 16 + 8 = 136.'),
    p('Kui palju värve nii kokku saab? Punasel on 256 võimalust, rohelisel 256 ja sinisel 256, ja neid võib vabalt '
      'kombineerida: 256 × 256 × 256 = 16 777 216. Üle 16 miljoni värvi. Kahe naabervärvi vahet enamik inimesi ei '
      'näegi.'),
    proovi('3', 'Kirjuta värvikoodina RGB (0, 0, 255) ja RGB (32, 0, 255). Proovi see järele vahelehel '
                '<b>Värv ja resolutsioon</b>, kus saad liugureid liigutada ja lampe näha.'),

    p('Resolutsioon: mida rohkem ruute, seda teravam', h2),
    p('<b>Resolutsioon</b> ehk pikslimõõtmed ütleb, mitu pikslit on pildil laiuses ja kõrguses. Täis-HD ekraanil on '
      '1920 × 1080: 1920 pikslit laiuses ja 1080 kõrguses. Sama ring näeb eri resolutsioonis välja nii:'),
    figure(resolution_drawing(), 'Sama ring. Mida rohkem piksleid, seda vähem on trepiastmeid näha.'),
    p('Teravus maksab aga ruumi. Nendes ülesannetes kasutame pakkimata RGB-pilti, milles iga piksel võtab 3 baiti. '
      'Arvutame ainult pikslite andmemahtu; faili lisainfot ei arvesta.'),
    note('<b>Pakkimata pildiandmete maht = laius × kõrgus × baite ühes pikslis</b><br/>RGB-pildil on pikslis 3 baiti. '
         'Baitidest megabaitide saamiseks jaga 1 000 000-ga.'),
    p('Täis-HD pilt samm-sammult:'),
    code('''
1. samm: pikslite arv    1920 × 1080 = 2 073 600 pikslit
2. samm: baitide arv     2 073 600 × 3 = 6 220 800 baiti
3. samm: megabaidid      6 220 800 : 1 000 000 ≈ 6,2 MB
'''),
    proovi('4', 'RGB-pilt on 1000 pikslit lai ja 500 kõrge. Kui suur on selle pakkimata andmemaht baitides ja '
                'megabaitides?'),
    p('Nüüd mõistatus. Telefon teeb 12-megapikslise pildi. <i>Mega</i> tähendab miljonit: 12 000 000 × 3 baiti = '
      '36 000 000 baiti ehk 36 MB. Nii palju võtaksid selle pakkimata RGB-andmed. Pakitud fotofail võib olla näiteks '
      '3 MB. Kuhu ülejäänu kadus?'),

    p('Pakkimine: kuidas 36 MB-st võib saada 3 MB', h2),
    p('Oletame, et kirjutad poenimekirja. Sa ei kirjuta ju „õun, õun, õun, õun, õun“, vaid „5 õuna“. Info on sama, '
      'kirja läheb vähem. See ongi <b>pakkimine</b>: sama info kirjutatakse vähemate baitidega.'),
    p('Pildil võib see välja näha nii: sinine taevas on tuhat täpselt sama värvi pikslit järjest. Tuhande piksli asemel '
      'saab kirjutada „1000 korda sinine“ ja pildi saab pärast täpselt samasugusena tagasi. Sellist pakkimist, kus '
      'midagi ära ei kao, nimetatakse <b>kadudeta</b> pakkimiseks. See näide näitab kadudeta pakkimise põhiideed. Ka '
      'PNG kasutab kadudeta pakkimist, kuid selle tegelik pakkimisviis on keerukam.'),
    p('JPEG on julgem. Ta viskab päriselt infot minema, eelkõige pisikesi erinevusi, mida silm kergesti ei märka. Foto '
      'võib välja näha peaaegu samasugune, aga fail olla palju väiksem. See on <b>kadudega</b> pakkimine. Äravisatut '
      'enam tagasi ei saa.'),
    p('JPEG-pildi kvaliteet võib halveneda, kui pilti muudetakse ja seejärel uuesti JPEG-vormingus salvestatakse. Faili '
      'muutmata kopeerimine või saatmine selle kvaliteeti ei vähenda.'),
    table(['Failivorming', 'Pakkimine', 'Sobib'], [
        ['BMP', 'tavaliselt ei paki', 'tänapäeval harva, fail on suur'],
        ['PNG', 'kadudeta', 'ekraanipildid, logod, tekst pildil: seal, kus on teravad servad'],
        ['JPEG', 'kadudega', 'fotod'],
        ['WebP, AVIF', 'mõlemat moodi', 'veebilehed: uuemad vormingud, failid sageli väiksemad'],
    ], [WIDTH * 0.2, WIDTH * 0.25, WIDTH * 0.55]),
    Spacer(1, 6),
    p('Järgmises tunnis teeme pakkimist töötoas ise, nii et praegu piisab sellest põhiideest.'),

    p('Heli: õhu värisemine', h2),
    p('Löö kitarrikeelt. Keel võngub ehk väriseb kiiresti edasi-tagasi, tõukab õhku ja see liikumine jõuab su kõrva '
      'sisse. Heli ongi õhu värisemine. Mikrofon teeb sama asja vastupidi: õhk liigutab tema sees pisikest plaati ja '
      'sellest tekib elektrivool, mis tõuseb ja langeb koos heliga.'),
    p('Kui selle tõusmise ja langemise joonistad, saad laine. Laine on sujuv, aga arvuti oskab hoida ainult üksikuid '
      'arve. Mida teha?'),
    p('Mõtle ilmajaamale. Õhutemperatuur muutub kogu aeg, aga jaam kirjutab selle üles iga tunni tagant. Nende arvude '
      'järgi saab päeva graafiku uuesti joonistada. Arvuti teeb helilainega sama, ainult et mitte kord tunnis, vaid '
      'kümneid tuhandeid kordi sekundis. Seda mõõtmist nimetatakse <b>diskreetimiseks</b> (ingl <i>sampling</i>).'),
    figure(wave_drawing(), 'Hall joon on päris helilaine. Iga sinine täpp on üks mõõtmine: üks arv, mille arvuti salvestab.'),
    p('Mõõtma peab piisavalt tihti, et helis olevad kõige kõrgemad sagedused kirja saada. Kui mõõdad liiga harva, kaovad '
      'kiired võnked ära ja heli muutub tuhmiks, nagu vana telefonikõne.'),
    figure(sampling_compare(), 'Hall on päris laine. Sinine astmeline joon aitab mõõtmistulemusi näha. Tegelik heli '
                               'taastamine on keerukam.'),
    p('Järgmises näites kasutame CD-heli parameetreid: 44 100 mõõtmist sekundis kanali kohta, 2 baiti mõõtmise kohta ja '
      '2 kanalit. Igal arvul on oma põhjus:'),
    table(['Arv', 'Mida tähendab', 'Miks just nii'], [
        ['<b>44 100</b>', 'mõõtmist sekundis kanali kohta', 'Inimene kuuleb kuni umbes 20 000 võnget sekundis ja ühe '
                                                            'võnke kirjeldamiseks on vaja vähemalt kaht mõõtmist.'],
        ['<b>2 baiti</b>', 'ühe mõõtmise kohta', 'See on 16 bitti, millega saab eristada 65 536 erinevat signaalitaset.'],
        ['<b>2 kanalit</b>', 'stereo', 'Eraldi vasaku ja parema kanali helisignaal. Üks kanal oleks mono.'],
    ], [WIDTH * 0.16, WIDTH * 0.26, WIDTH * 0.58]),
    Spacer(1, 6),
    note('<b>Pakkimata heli andmemaht = mõõtmisi sekundis × baite mõõtmises × kanaleid × sekundeid</b>'),
    CondPageBreak(90),
    p('Üks minut CD-heli samm-sammult:'),
    code('''
1. samm: üks sekund, üks kanal   44 100 × 2 = 88 200 baiti
2. samm: üks sekund, stereo      88 200 × 2 = 176 400 baiti
3. samm: üks minut               176 400 × 60 = 10 584 000 baiti ≈ 10,6 MB
'''),
    p('Pakkimata kolmeminutiline laul võtaks seega üle 30 MB. MP3 ja teised sarnased vormingud kasutavad jälle kadudega '
      'pakkimist ja viskavad ära helid, mida kõrv kergesti ei kuule, näiteks vaikse heli kohe valju heli kõrval. '
      'Tulemus võib olla näiteks umbes 1 MB minutis.'),
    proovi('5', 'Kui suur on 10 sekundit pakkimata CD-heli stereos? Vaata siis vahelehel <b>Heli</b>, mis lainega '
                'juhtub, kui mõõtmiste arvu liuguriga vähendad.'),

    p('Lisateema. Video: palju pilte järjest', h2),
    p('Video on nagu lehenurga-multikas: palju pilte, mida näidatakse nii kiiresti, et silm näeb liikumist. Ühte pilti '
      'videos nimetatakse <b>kaadriks</b>. Sageli on sekundis 30 kaadrit. Arvutame pakkimata täis-HD video pildiandmete '
      'mahu. Heli siin ei arvesta. Täpne baitide arv jääb arvutuse lõpuni alles ja ümardame ainult lõppvastuse:'),
    code('''
1. samm: üks kaader (vaata arvutust eespool)   6 220 800 baiti
2. samm: üks sekund    6 220 800 × 30 = 186 624 000 baiti
3. samm: kaks tundi    2 tundi on 7200 sekundit
                       186 624 000 × 7200 = 1 343 692 800 000 baiti ≈ 1,3 TB
'''),
    p('Pakitud kahetunnine film võib olla näiteks umbes 6 GB. Kuidas? Video pakkimine on väga kaval: kaks järjestikust '
      'kaadrit on sageli peaaegu samad, nii et salvestatakse enamasti ainult see, mis muutus. Kui uudistes liigub vaid '
      'diktori suu, siis on muutusi vähe.'),
    proovi('6', 'Kui palju ruumi võtaksid 10 sekundi pakkimata täis-HD video pildiandmed?'),

    p('Sõnastik', h2),
    table(['Sõna', 'Tähendus'], [
        ['<b>piksel</b>', 'pildi väikseim ruut, mis on ühte värvi'],
        ['<b>resolutsioon</b>', 'pikslimõõtmed: mitu pikslit on pildil laiuses ja kõrguses, näiteks 1920 × 1080'],
        ['<b>RGB</b>', 'värvimudel, mis kirjeldab värvi punase, rohelise ja sinise väärtusega'],
        ['<b>andmemaht</b>', 'mitu baiti andmed võtavad'],
        ['<b>failivorming</b>', 'kokkulepe, kuidas andmed failis on kirjas, näiteks PNG või JPEG'],
        ['<b>pakkimine</b>', 'sama info kirjutamine vähemate baitidega'],
        ['<b>kadudeta</b>', 'pakkimine, kus midagi ei lähe kaotsi (PNG, ZIP)'],
        ['<b>kadudega</b>', 'pakkimine, mis viskab osa infot jäädavalt ära (JPEG, MP3)'],
        ['<b>diskreetimine</b>', 'helilaine mõõtmine kindlate vahedega'],
        ['<b>mono, stereo</b>', 'üks helikanal; eraldi vasak ja parem helikanal'],
        ['<b>kaader</b>', 'üks pilt videost'],
    ], [WIDTH * 0.22, WIDTH * 0.78]),

    CondPageBreak(190),
    p('„Proovi ise“ vastused', h2),
    *numbered([
        '16 × 8 = 128 pikslit. Igaüks on 1 bitt, seega 128 bitti. 128 : 8 = 16 baiti.',
        c('0110') + ' on 6 ja ' + c('0110') + ' on 6, seega ' + c('66') + '. ' + c('1111') + ' on F ja ' + c('0000')
        + ' on 0, seega ' + c('F0') + '.',
        c('#0000FF') + ' ja ' + c('#2000FF') + '. 32 : 16 = 2, jääk 0, seega on punane ' + c('20') + '.',
        '1000 × 500 = 500 000 pikslit. 500 000 × 3 = 1 500 000 baiti ehk 1,5 MB.',
        'Üks sekund stereot on 176 400 baiti. 176 400 × 10 = 1 764 000 baiti ≈ 1,8 MB.',
        '186 624 000 × 10 = 1 866 240 000 baiti ≈ 1,9 GB.',
    ]),
]

kodutoo_pildid = [
    p('Kodutöö: pildid ja heli', title),
    subtitle('8. tund', 'kodutöö'),
    row([p('Nimi', label_b), Field('nimi', 220), '', p('Kuupäev', label_b), Field('kuupaev', 110), ''],
        [51, 220, 18, 51, 110, WIDTH + 12 - 450], PALE),
    Spacer(1, 8),
    p('Täida lahtrid otse kursuse veebilehel: ava fail nupuga „Vaata“, kirjuta vastused ja vajuta „Laadi täidetud PDF '
      'alla“. Saada täidetud fail aadressile <b>mtsopo@taltech.ee</b> hiljemalt 09.11 kell 23.59. Kõik siinne on konspektis '
      'samm-sammult läbi tehtud, nii et hätta jäädes otsi sealt sarnane näide üles.', intro),

    p('1. Pildist arvudeks', h2),
    p('See pilt on 8 × 8 pikslit, must on 1 ja valge on 0. Loe ridu ülevalt alla ja iga rea piksleid vasakult paremale. '
      'Kirjuta iga vastus täpselt kahe kuueteistkümnendsüsteemi numbriga, vajaduse korral koos algusnulliga. Näide: '
      + c('00111100') + ' on ' + c('3C') + '.'),
    arrow_picture(),
    Spacer(1, 6),
]
for i in range(8):
    kodutoo_pildid.append(row([p(f'{i + 1}. rida', label), Field(f'rida_{i}', 60)], [70, 60]))
kodutoo_pildid += [
    question('Mitu baiti võtavad selle pildi pikslid kokku, kui ühes pikslis on 1 bitt?', 'rida_baite'),

    p('2. Värvikoodid', h2),
    p('Kirjuta RGB-värv koodina, näiteks RGB (255, 136, 0) on ' + c('#FF8800') + '.'),
]
for i, rgb in enumerate(['0, 255, 0', '255, 0, 255', '128, 128, 128', '16, 32, 64']):
    kodutoo_pildid.append(row([p(f'RGB ({rgb})', label), Field(f'hex_{i}', 100)], [130, 100]))
kodutoo_pildid += [
    CondPageBreak(110),
    Spacer(1, 4),
    p('Nüüd vastupidi: kirjuta kood kolme arvuna R, G, B. Näiteks ' + c('#FF8800') + ' on 255, 136, 0.'),
]
for i, code_ in enumerate(['#FFFF00', '#00FFFF', '#0A0A0A']):
    kodutoo_pildid.append(row([p(c(code_), label), Field(f'rgb_{i}', 130)], [130, 130]))
kodutoo_pildid += [
    CondPageBreak(200),
    p('3. Kui suur on pakkimata pilt?', h2),
    p('Arvutusi tehes mõtle läbi: <b>antud → valem → arvutus → vastus koos ühikuga</b>. Lahtrisse kirjuta ainult vastus. '
      'Arvuta pakkimata RGB-pildi andmemaht, kus iga piksel võtab 3 baiti. Faili lisainfot ära arvesta. Megabaidi '
      'saamiseks jaga 1 000 000-ga ja kirjuta vastus kahe komakohaga.'),
    row([p('<b>Pilt</b>', label), p('<b>Baite</b>', label), p('<b>MB</b>', label)], [230, 120, 80]),
]
for i, name in enumerate(['RGB-pilt 800 × 600', '4K-ekraani pilt 3840 × 2160', '20-megapiksline foto']):
    kodutoo_pildid.append(row([p(name, label), Field(f'pilt_b_{i}', 110), '', Field(f'pilt_mb_{i}', 80)],
                              [230, 110, 10, 80]))
kodutoo_pildid += [
    Spacer(1, 8),
    question('Mustvalge ikoon on 16 × 16 pikslit, igal pikslil 1 bitt. Mitu baiti see võtab?', 'ikoon'),

    p('4. Kui suur on pakkimata heli?', h2),
    p('CD-heli: 44 100 mõõtmist sekundis kanali kohta, 2 baiti mõõtmises. Mono on üks kanal, stereo kaks. Ülesannetes a '
      'ja b kirjuta vastus megabaitides ühe komakohaga. Ülesandes c kirjuta vastus baitides. Kõigis ülesannetes arvutame '
      'pakkimata heli andmemahtu.'),
    question('<b>a)</b> Üks minut monos.', 'heli_a'),
    question('<b>b)</b> Kolmeminutiline laul stereos.', 'heli_b'),
    question('<b>c)</b> Vanas telefonis mõõdeti häält 8000 korda sekundis, 1 bait mõõtmises, mono. Mitu baiti võttis '
             'üks minut kõnet?', 'heli_c'),

    CondPageBreak(150),
    p('5. PNG või JPEG?', h2),
    p('Kirjuta iga pildi juurde sobiv failivorming: PNG või JPEG.'),
]
for i, name in enumerate(['foto puhkusereisilt', 'ekraanipilt veateatest', 'kooli logo teravate servadega']):
    kodutoo_pildid.append(row([p(name, label), Field(f'vorming_{i}', 80)], [230, 80]))
kodutoo_pildid += [
    CondPageBreak(190),
    p('6. Selgita', h2),
    question('<b>a)</b> Sõber näitas meemi, mis on nii plekiline, et teksti on raske lugeda. Inimesed olid seda korduvalt '
             'muutnud ja uuesti salvestanud. Miks see nii läks? Kasuta sõna „kadudega“.', 'meem', 56),
    question('<b>b) Lisaülesanne.</b> Arvuta, mitu megabaiti võtaksid ühe sekundi pakkimata video pildiandmed, kui kaader '
             'on 1280 × 720 pikslit ja sekundis on 30 kaadrit. Kasuta RGB-pilti, milles iga piksel võtab 3 baiti. Heli ja '
             'faili lisainfot ära arvesta. Kirjuta ka arvutuskäik.', 'video', 56),
]

# ---------------------------------------------------------------- 9. tund: pakkimine

pakkimine = [
    p('Pakkimine', title),
    subtitle('9. tund', 'konspekt'),

    intro_box('See konspekt selgitab kõik algusest peale ja seda saab lugeda ka tunnist puududes. Lahenda „Proovi ise“ '
              'kastid, vastused on lõpus. Veebilehel on <b>Pakkimislabor</b>, kus saad kõike päris failidega järele '
              'proovida. Konspekti lõpus on kirjas, mida tunnis samm-sammult teeme.<br/><br/>'
              '<b>Pärast seda tundi oskad:</b><br/>'
              '• pakkida ja lahti pakkida RLE-ga;<br/>'
              '• arvutada, mitu korda andmemaht vähenes ja mitu protsenti säästsid;<br/>'
              '• selgitada, millal sobib kadudeta ja millal kadudega pakkimine.'),

    p('Poenimekiri', h2),
    p('Sul on vaja poest 12 õuna tuua. Sa ei kirjuta paberile kaksteist korda „õun“, vaid „12 õuna“. Selle pisikese '
      'trikiga oledki avastanud pakkimise.'),
    p('<b>Pakkimine</b> tähendab, et sama info kirjutatakse vähemate baitidega. Üks bait koosneb 8 bitist. Märgi '
      'salvestamiseks vajalik baitide arv sõltub kodeeringust: näiteks UTF-8 kodeeringus võtab a ühe baidi ja õ kaks '
      'baiti. 1 MB on 1 000 000 baiti.'),
    p('Eelmises tunnis arvutasime, et 12-megapikslise pildi pakkimata RGB-andmed võtaksid 36 MB, aga pakitud fotofail '
      'võib olla näiteks 3 MB. Ilma pakkimiseta mahuks telefoni palju vähem pilte ja video vaatamine netist oleks palju '
      'raskem. Täna saad teada, kuidas see käib, ja proovid järele.'),

    p('Pakkimisviis nr 1: loe järjest samad kokku', h2),
    p('Mõtle pildile, kus iga piksel (pildi väikseim ruut) on kas valge või must. Eelmises tunnis piisas kahevärvilise '
      'pildi ühe piksli jaoks ühest bitist. Siin kasutame RLE õppimiseks lihtsustatud esitust: iga piksel on kirjas '
      'ühebaidise märgina V (valge) või M (must). Üks rida kümnest pikslist:'),
    code('''
V V V V V M M M V V        10 pikslit = 10 baiti
'''),
    p('Selle asemel, et iga piksel eraldi üles kirjutada, loeme kokku, mitu ühesugust on järjest: viis valget, kolm '
      'musta, kaks valget. Kirjutame ' + c('5V 3M 2V') + '. Meie mudelis salvestatakse korduste arv ühe baidina ja '
      'värvitähis teise baidina. Paare on kolm, nii et kokku 6 baiti. Kümne asemel! Ka paar ' + c('12V') + ' võtab kaks '
      'baiti. Näidetes olevad tühikud on ainult lugemise hõlbustamiseks.'),
    figure(rle_drawing([('VVVVVMMMVV', '5V 3M 2V')]), 'Sama rida: pakkimata 10 baiti, pakituna 6 baiti.'),
    p('Seda viisi nimetatakse <b>RLE</b>-ks (ingl <i>run-length encoding</i>). Eesti keeles võiks öelda „järjendite '
      'pakkimine“, kus järjend on rida ühesuguseid asju.'),
    p('Lahtipakkimine on sama lihtne: kirjuta iga paari järgi pikslid uuesti välja. ' + c('2M 3V') + ' tähendab kaks '
      'musta ja kolm valget, ehk ' + c('MMVVV') + '. Tulemus on täpselt sama, mis enne pakkimist, midagi ei kadunud. See '
      'on <b>kadudeta</b> pakkimine.'),
    proovi('1', 'Paki rida ' + c('MMMMVVVVVV') + '. Mitu baiti see võtab? Paki lahti ' + c('2V 3M 1V') + '. Harjuta '
                'Pakkimislabori vahelehel <b>RLE</b>, seal kontrollib arvuti vastuse kohe ära.'),

    p('Kui hästi see töötas?', h2),
    p('Pakkimise tulemust mõõdetakse kahel viisil. Mõlemad arvutused põhinevad jagamisel.'),
    code('''
Mitu korda väiksem?       enne : pärast
                          10 baiti : 5 baiti = 2 korda

Mitu protsenti säästsid?  (enne - pärast) : enne × 100
                          (10 - 5) : 10 × 100 = 50 %
'''),
    p('Kui 36 MB-st saab 3 MB: 36 MB : 3 MB = 12 korda väiksem. Säästetud on (36 − 3) : 36 × 100 ≈ 92 %. Kui võrdled eri '
      'pikkusega faile, on protsent parem mõõt kui säästetud baitide arv.'),
    proovi('2', 'Fail oli 5 MB, pärast pakkimist 1 MB. Mitu korda väiksem ja mitu protsenti säästetud?'),

    p('Aga mis siis, kui järjest ühesuguseid pole?', h2),
    p('Proovi nüüd malelauda, kus värvid vahelduvad iga ruudu järel:'),
    figure(rle_drawing([('VMVMVMVM', '1V 1M 1V 1M 1V 1M 1V 1M')]), 'Kaheksa pikslit, kaheksa paari. Pakitud kuju on suurem kui algne!'),
    p('Kaheksast baidist sai kuusteist. Andmemaht <i>kasvas</i> kaks korda. See pole programmiviga. RLE elab kordustest '
      'ja kui korduseid pole, pole ka millestki kokku hoida.'),
    p('See on tähtis mõte, mis tuleb täna veel mitu korda tagasi: <b>ükski kadudeta pakkija ei suuda iga faili '
      'väiksemaks teha.</b>'),

    p('Pakkimisviis nr 2: sõnastik', h2),
    p('RLE aitab ainult siis, kui samad asjad on kohe üksteise kõrval. Tekstis on sageli teisiti. Vaata seda lauset. '
      'Selles näites loeme märke, sealhulgas tühikuid ja kirjavahemärke. See ei ole faili täpne baitide arv.'),
    code('''
kass istub, kass sööb, kass magab          33 märki
'''),
    p('Järjest ühesuguseid tähti siin pole, aga sõna „kass“ kordub. Teeme väikese sõnastiku: 1 tähendab sõna „kass“.'),
    code('''
sõnastik: 1=kass                            6 märki
tekst:    1 istub, 1 sööb, 1 magab         24 märki
kokku                                      30 märki
'''),
    p('Pane tähele, et sõnastik tuleb ka kaasa pakkida, muidu ei saa keegi teksti lahti pakkida. Seepärast võitsime siin '
      'ainult 3 märki. Pikas tekstis, kus sama sõna on sada korda, on võit palju suurem. Mõtle laulule, kus refrään '
      'kordub: piisab, kui refräänist on üks koopia ja mujale kirjutad „nüüd tuleb refrään“.'),
    p('Sarnast ideed kasutavad levinud kadudeta vormingud gzip ja ZIP. Natuke kavalamalt küll: eraldi sõnastiku asemel '
      'võib seal olla kirjas „mine 16 märki tagasi ja kopeeri sealt 4 märki“. Idee on sama: ära kirjuta kaks korda seda, '
      'mis on juba olemas. Programmis või tekstis ei tohi ükski täht kaotsi minna, seega sobib siia just kadudeta '
      'pakkimine.'),
    proovi('3', 'Paki sõnastikuga lause ' + c('tere tere tere Mari') + '. Mitu märki oli enne ja mitu pärast, kui ka '
                'sõnastik kokku lugeda?'),

    p('Miks juhuslikku asja on raske pakkida?', h2),
    p('Kujuta ette, et pead sõbrale telefonis ette lugema tähed ' + c('xqf7kP2z') + '. Lühemalt seda öelda ei saa, '
      'pead kõik ükshaaval ära ütlema. Mustrit pole, nii et pole ka midagi lühendada.'),
    p('Sarnane lugu on juba pakitud failiga. Juba pakitud failis on tavaliselt vähem lihtsalt ärakasutatavaid kordusi. '
      'Seepärast ei tee ZIP JPEG-pilti tavaliselt palju väiksemaks ja ZIP-i pakkimine teise ZIP-i sisse enamasti ei '
      'aita.'),
    p('Pakitud andmetele lisandub ka vormingu lisainfo. Seetõttu võib väga lühike tekst pakkimisel hoopis suureneda. '
      'Seda näed vahelehel <b>gzip-labor</b>. Selles laboris pakib brauser teksti gzip-vormingus ja näitab baitide arvu '
      'enne ja pärast. ZIP on teine levinud pakkimisvorming.'),

    p('Pakkimisviis nr 3: viska ära, mida silm kergesti ei näe', h2),
    p('Foto on keerulisem. Fotol võib olla palju väikeseid värvierinevusi, mistõttu lihtne RLE ei pruugi hästi töötada. '
      'JPEG lähenebki teisest otsast: kas inimesel on vaja iga väikest erinevust?'),
    p('Kujuta ette, et kirjeldad telefonis sõbrale pilti taevast. Sa ei hakka ütlema iga ruudu täpset värvi, vaid '
      'ütled: „see nurk on helesinine“. Sõber saab enam-vähem sama pildi. JPEG jagab pildi väikesteks ruutudeks '
      '(8 × 8 pikslit) ja lihtsustab igaühes väikeseid erinevusi.'),
    figure(jpeg_block_drawing(), 'Lihtsustatud näide väikeste heleduseerinevuste eemaldamisest; see ei näita JPEG-i '
                                 'täpset tööalgoritmi.'),
    p('See on <b>kadudega</b> pakkimine. Infot läheb päriselt kaotsi ja seda ei saa kuidagi tagasi. Salvestamisel saad '
      'valida kvaliteedi: kõrgem kvaliteet tähendab vähem ära visatud infot ja tavaliselt suuremat faili.'),
    p('Siit tuleb ka see, miks tekst JPEG-is võib halvasti välja näha. Teravate mustade tähtede ümber võib tekkida '
      'plekiline aura. Seepärast on ekraanipildi jaoks PNG sageli parem.'),
    p('JPEG-pildi kvaliteet võib halveneda, kui pilti muudetakse ja seejärel uuesti JPEG-vormingus salvestatakse. Faili '
      'muutmata kopeerimine või saatmine selle kvaliteeti ei vähenda. Vaata seda vahelehel <b>JPEG-labor</b> nupuga '
      '„Salvesta uuesti“, mis lõikab pildilt iga kord serva ära ja salvestab uuesti.'),

    p('Mida millal kasutada?', h2),
    table(['Asi', 'Vali', 'Miks'], [
        ['foto', 'JPEG', 'Väikesed kaod ei paista tavaliselt välja.'],
        ['ekraanipilt, logo, joonis', 'PNG', 'Palju ühesugust värvi pikslit, teravad servad ei tohi plekiliseks minna.'],
        ['tekst, kood, programmid', 'ZIP, gzip', 'Ükski märk ei tohi kaduda.'],
        ['muusika', 'MP3, AAC', 'Kadudega: väike kadu jääb tavaliselt kõrvale märkamatuks.'],
        ['juba pakitud fail', 'ära paki', 'Sellest ei tule tavaliselt palju kasu.'],
    ], [WIDTH * 0.32, WIDTH * 0.14, WIDTH * 0.54]),

    p('Mida tunnis teeme', h2),
    *numbered([
        '<b>RLE käsitsi.</b> Ava Pakkimislaboris vaheleht RLE ja tee ülesanded läbi. Täida töölehe 1. ja 2. osa.',
        '<b>Päris gzip.</b> Vahelehel gzip-labor on kolm nuppu: korduv tekst, tavaline tekst ja juhuslikud märgid. '
        'Vajuta kõiki, kirjuta tulemused töölehe 3. ossa ja kleebi kasti ka oma tekst.',
        '<b>Päris JPEG.</b> Vahelehel JPEG-labor vali foto moodi pilt, seejärel logo moodi pilt ja liiguta kvaliteeti. '
        'Kirjuta suurused töölehe 4. ossa. Soovi korral proovi oma pildiga, see ei lahku su arvutist.',
        '<b>Selgita.</b> Täida töölehe viimane osa, tee kodus lõpuni, mis jäi pooleli, ja saada tööleht ära. Ülesanne 5c '
        'on lisaülesanne.',
    ]),

    CondPageBreak(230),
    p('Sõnastik', h2),
    table(['Sõna', 'Tähendus'], [
        ['<b>andmemaht</b>', 'mitu baiti andmed võtavad'],
        ['<b>pakkimine</b>', 'sama info kirjutamine vähemate baitidega'],
        ['<b>kadudeta</b>', 'lahti pakkides saad täpselt sama faili tagasi (PNG, ZIP, gzip)'],
        ['<b>kadudega</b>', 'osa infot visatakse jäädavalt ära (JPEG, MP3)'],
        ['<b>RLE</b>', 'pakkimine, mis loeb kokku, mitu ühesugust asja on järjest: 5V 3M'],
        ['<b>sõnastik</b>', 'nimekiri korduvatest tükkidest, millele saab tekstis lühidalt viidata'],
        ['<b>ZIP, gzip</b>', 'levinud kadudeta pakkimisvormingud'],
        ['<b>kvaliteet</b>', 'JPEG-i seadistus: mida kõrgem, seda vähem infot visatakse ära'],
    ], [WIDTH * 0.22, WIDTH * 0.78]),

    CondPageBreak(170),
    p('„Proovi ise“ vastused', h2),
    *numbered([
        c('4M 6V') + ', kaks paari ehk 4 baiti. Lahti pakituna ' + c('VVMMMV') + '.',
        '5 : 1 = 5 korda väiksem. (5 − 1) : 5 × 100 = 80 % säästetud.',
        'Enne 19 märki. Sõnastik ' + c('1=tere') + ' on 6 märki ja tekst ' + c('1 1 1 Mari') + ' on 10 märki, kokku 16.',
    ]),
]

kodutoo_pakkimine = [
    p('Tunni- ja kodutöö: pakkimine', title),
    subtitle('9. tund', 'tööleht'),
    row([p('Nimi', label_b), Field('nimi', 220), '', p('Kuupäev', label_b), Field('kuupaev', 110), ''],
        [51, 220, 18, 51, 110, WIDTH + 12 - 450], PALE),
    Spacer(1, 8),
    p('Täida lahtrid otse kursuse veebilehel: ava fail nupuga „Vaata“, kirjuta vastused ja vajuta „Laadi täidetud PDF '
      'alla“. Tee tunnis nii palju, kui jõuad, ja lõpeta ülejäänud ülesanded kodus. Saada täidetud fail aadressile '
      '<b>mtsopo@taltech.ee</b> hiljemalt 16.11 kell 23.59. Abiks on konspekt ja veebilehe Pakkimislabor.', intro),

    p('1. RLE käsitsi', h2),
    p('V on valge, M on must. Pakkimata võtab iga piksel 1 baidi. Pakituna võtab iga paar 2 baiti: korduste arv on üks '
      'bait ja värvitähis teine, seega ka ' + c('10M') + ' võtab 2 baiti. Näide: ' + c('VVVVVMMMVV') + ' on '
      + c('5V3M2V') + ', 6 baiti.'),
    row([p('<b>Rida</b>', label), p('<b>Pakituna</b>', label), p('<b>Baite</b>', label)], [130, 200, 60]),
]
for i, line in enumerate(['VVVVVVMMMM', 'MMMMMMMMMM', 'VVMMVVMMVV', 'VMVMVMVM']):
    kodutoo_pakkimine.append(row([p(c(line), label), Field(f'rle_{i}', 190), '', Field(f'rle_b_{i}', 50)],
                                 [130, 190, 10, 50]))
kodutoo_pakkimine += [
    Spacer(1, 6),
    p('Paki lahti:'),
]
for i, line in enumerate(['3M2V1M', '4V4M', '1M6V1M']):
    kodutoo_pakkimine.append(row([p(c(line), label), Field(f'lahti_{i}', 190)], [130, 190]))
kodutoo_pakkimine += [
    Spacer(1, 6),
    question('Vaata 1. osa pakkimistabelit. Millises reas jäi andmemaht samaks ja millises suurenes? Selgita mõlemat '
             'juhtumit.', 'rle_miks', 40),

    CondPageBreak(230),
    p('2. Eesti lipp', h2),
    p('Lipupilt on 12 pikslit lai ja 6 kõrge: kaks rida sinist (S), kaks musta (M) ja kaks valget (V). Iga piksel on '
      '1 bait. Iga rida alustab uut paari, ka siis, kui eelmine rida oli sama värvi. Esimesed kaks rida on seega '
      + c('12S') + ' ja ' + c('12S') + ', kumbki 2 baiti.'),
    flag_drawing(),
    Spacer(1, 4),
    row([p('Baite pakkimata', label), Field('lipp_enne', 60), '', p('Baite pakituna', label), Field('lipp_parast', 60), '',
         p('Mitu korda väiksem', label), Field('lipp_korda', 50)], [85, 60, 12, 80, 60, 12, 105, 50]),
    Spacer(1, 10),

    p('Arvuta veel: fail oli 1000 KB ja jäi pakituna 250 KB-ks.'),
    row([p('Mitu korda väiksem?', label), Field('suhe_korda', 80), '', p('Mitu % säästetud?', label),
         Field('suhe_pr', 80)], [130, 80, 20, 110, 80]),
    Spacer(1, 8),

    CondPageBreak(200),
    p('3. gzip-labor', h2),
    p('Vajuta Pakkimislabori vahelehel gzip-labor iga nuppu ja kirjuta tulemused. Viimases reas kasuta oma teksti, '
      'näiteks kopeeri mõni Vikipeedia artikkel.'),
    row([p('<b>Tekst</b>', label), p('<b>Baite enne</b>', label), p('<b>Baite pärast</b>', label),
         p('<b>Säästetud %</b>', label)], [150, 85, 85, 85]),
]
for i, name in enumerate(['korduv tekst', 'tavaline tekst', 'juhuslikud märgid', 'minu oma tekst']):
    kodutoo_pakkimine.append(row([p(name, label), Field(f'zip_e_{i}', 75), '', Field(f'zip_p_{i}', 75), '',
                                  Field(f'zip_s_{i}', 75)], [150, 75, 10, 75, 10, 75]))
kodutoo_pakkimine += [
    Spacer(1, 6),
    question('Millise teksti maht vähenes pakkimisel protsentides kõige rohkem ja millise oma kõige vähem? Miks?',
             'zip_miks', 56),

    CondPageBreak(230),
    p('4. JPEG-labor', h2),
    p('Vahelehel JPEG-labor vali pilt, liiguta kvaliteet õigele kohale ja kirjuta faili suurus kilobaitides. PNG suurus '
      'on seal kohe näha. 90, 50 ja 10 on liuguri seadistused, mitte protsendid algse pildi kvaliteedist.'),
    row([p('<b>Pilt</b>', label), p('<b>PNG</b>', label), p('<b>JPEG 90</b>', label), p('<b>JPEG 50</b>', label),
         p('<b>JPEG 10</b>', label)], [100, 80, 80, 80, 80]),
]
for i, name in enumerate(['foto moodi', 'logo moodi']):
    kodutoo_pakkimine.append(row([p(name, label), Field(f'jp_{i}_png', 70), '', Field(f'jp_{i}_90', 70), '',
                                  Field(f'jp_{i}_50', 70), '', Field(f'jp_{i}_10', 70)],
                                 [100, 70, 10, 70, 10, 70, 10, 70]))
kodutoo_pakkimine += [
    Spacer(1, 8),
    question('Kummale pildile sobib JPEG paremini ja kummale PNG? Mis JPEG 10 juures pildiga juhtus?', 'jp_miks', 56),

    CondPageBreak(180),
    p('5. Selgita oma sõnadega', h2),
    question('<b>a)</b> Miks ei tasu JPEG-pilti ZIP-i panna, kui eesmärk on fail väiksemaks saada?', 'sel_a', 48),
    question('<b>b)</b> Miks ei tohi programmifaili pakkida kadudega?', 'sel_b', 48),
    question('<b>c) Lisaülesanne.</b> Sõber väidab, et leiutas kadudeta pakkija, mis teeb iga faili poole väiksemaks. '
             'Miks ta eksib?', 'sel_c', 48),
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


BUILDS = {
    'protsessor-konspekt': ('Kuidas protsessor programmi täidab', protsessor),
    'kodutoo-protsessor': ('Kodutöö: protsessor', kodutoo),
    'pildid-heli-konspekt': ('Pildid ja heli arvudena', pildid),
    'kodutoo-pildid': ('Kodutöö: pildid ja heli', kodutoo_pildid),
    'pakkimine-konspekt': ('Pakkimine', pakkimine),
    'kodutoo-pakkimine': ('Tunni- ja kodutöö: pakkimine', kodutoo_pakkimine),
    'internet-konspekt': ('Kuidas internet töötab', internet),
}

if __name__ == '__main__':
    for name in sys.argv[1:] or BUILDS:
        doc_title, story = BUILDS[name]
        build(f'public/files/{name}.pdf', doc_title, f'{SUBJECT} · {doc_title}', story, SUBJECT)
