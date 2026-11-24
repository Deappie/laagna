# Builds the 11IT lesson 11 PDFs in public/files/:
#   andmebaasid-konspekt.pdf (theory: why a database, tables, keys, SQL, NoSQL) and
#   tunnitoo-andmebaasid.pdf (team presentations about one popular database each).
# Needs ReportLab (pip install reportlab) and the macOS system fonts Arial and Menlo.
# Run from the project root: python scripts/tund11_11it.py
# To build only some of them: python scripts/tund11_11it.py andmebaasid-konspekt
import math
import sys

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import CondPageBreak, KeepTogether, Paragraph, Spacer

from pdf_common import (BLUE, LINE, NAVY, PALE, WIDTH, build, bullet, bullets, c, code, code_parts, h2, intro, note, p,
                        sub, title)
from pdf_common import table as plain_table

SUBJECT = '11IT · Veebirakendused'
MUTED = HexColor('#7A8BA3')
figcap = ParagraphStyle('figcap', fontName='Sans', fontSize=8.5, leading=11, textColor=BLUE, alignment=1,
                        spaceBefore=2, spaceAfter=4)


def table(*args, **kwargs):
    return KeepTogether([plain_table(*args, **kwargs), Spacer(1, 6)])


def subtitle(lesson, kind):
    return p(f'{SUBJECT} · {lesson} · {kind}', sub)


def proovi(number, text_):
    return note(f'<b>Proovi ise {number}.</b> {text_}')


def numbered(items):
    return [Paragraph(i, bullet, bulletText=f'{n}.') for n, i in enumerate(items, 1)]


def figure(drawing, text_):
    return KeepTogether([drawing, p(text_, figcap), Spacer(1, 6)])


def text(d, x, y, s, size=9, color=NAVY, font='Sans', anchor='middle'):
    d.add(String(x, y, s, fontName=font, fontSize=size, fillColor=color, textAnchor=anchor))


def arrow(d, x1, y1, x2, y2, color=BLUE):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.4))
    ang = math.atan2(y2 - y1, x2 - x1)
    s = 6
    d.add(Polygon([x2, y2, x2 - s * math.cos(ang - 0.4), y2 - s * math.sin(ang - 0.4),
                   x2 - s * math.cos(ang + 0.4), y2 - s * math.sin(ang + 0.4)], fillColor=color, strokeColor=color))


def memory_drawing():
    d = Drawing(WIDTH, 120)
    w, h = 190, 84
    left, right = 10, WIDTH - 10 - w
    for x, name, line1, line2, fill in [
        (left, 'SERVER: MÄLU (RAM)', 'let arvustused = [ … ]', 'kaob, kui server peatub', PALE),
        (right, 'ANDMEBAAS: KETAS', 'sookla.db', 'jääb alles ka pärast taaskäivitust', white),
    ]:
        d.add(Rect(x, 22, w, h, rx=8, fillColor=fill, strokeColor=BLUE, strokeWidth=1.3))
        text(d, x + w / 2, 22 + h - 18, name, 8.5, BLUE, 'Sans-Bold')
        text(d, x + w / 2, 22 + h / 2 - 6, line1, 10, NAVY, 'Mono')
        text(d, x + w / 2, 32, line2, 8, MUTED)
    arrow(d, left + w + 12, 70, right - 12, 70)
    arrow(d, right - 12, 52, left + w + 12, 52)
    text(d, WIDTH / 2, 76, 'SQL-päring', 8, BLUE)
    text(d, WIDTH / 2, 40, 'vastus', 8, BLUE)
    text(d, WIDTH / 2, 6, 'Täna hoiab söökla server arvustusi vasakul. Järgmisel korral liigub kõik paremale.', 8, MUTED)
    return d


ARVUSTUSED = [
    ['1', 'Kanakaste riisiga', '5', 'Parim toit sel nädalal!'],
    ['2', 'Hernesupp', '3', 'Natuke liiga paks.'],
    ['3', 'Makaronid hakklihaga', '4', 'Klassika, alati hea.'],
]


def arvustused_table():
    return table(['id', 'toit', 'hinne', 'kommentaar'], ARVUSTUSED,
                 [WIDTH * 0.08, WIDTH * 0.32, WIDTH * 0.12, WIDTH * 0.48])


# ---------------------------------------------------------------- konspekt

konspekt = [
    p('Andmebaasid', title),
    subtitle('11. tund', 'konspekt'),

    note('Selles tunnis on teooria ja esitlused, järgmisel korral paneme söökla serveri päriselt andmebaasi kasutama. '
         'Konspekti saab lugeda ka tunnist puududes. „Proovi ise“ kastid lahendad paberil, vastused on lõpus.<br/><br/>'
         '<b>Pärast seda tundi oskad:</b><br/>'
         '• selgitada, miks serveri massiiv ei sobi andmete hoidmiseks;<br/>'
         '• lugeda andmebaasi tabelit: rida, veerg, primaarvõti ja võõrvõti;<br/>'
         '• kirjutada lihtsaid SQL-päringuid SELECT, INSERT, UPDATE ja DELETE;<br/>'
         '• eristada relatsioonilist andmebaasi NoSQL-andmebaasidest.'),

    p('Kuhu arvustused kadusid?', h2),
    p('Lisa söökla lehel arvustus, peata server klahvidega Ctrl + C ja käivita see uuesti. Värskenda lehte. Sinu arvustus '
      'on kadunud, alles on ainult kolm algset.'),
    p('Põhjus on ühes reas: ' + c('let arvustused = [ … ]') + '. See massiiv elab serveri mälus ehk RAM-is. RAM on kiire, '
      'aga unustab kõik, kui programm lõpetab. Iga taaskäivitus alustab nendest kolmest arvustusest, mis on koodis kirjas. '
      'Päris rakendus nii töötada ei saa. Kujuta ette, et Instagram kaotaks kõik pildid iga kord, kui serverisse '
      'uuendus paigaldatakse.'),
    figure(memory_drawing(), 'Mälu unustab, ketas mäletab. Andmebaas hoiab andmeid kettal ja server küsib neid sealt.'),

    p('Miks mitte lihtsalt fail?', h2),
    p('Esimene mõte oleks kirjutada massiiv faili, näiteks ' + c('arvustused.json') + ', ja lugeda see käivitamisel '
      'sisse. Väikeses kooliprojektis see isegi töötab. Mured tulevad siis, kui rakendus kasvab:'),
    *bullets(
        '<b>Kaks kasutajat korraga.</b> Mari ja Jaan saadavad arvustuse samal sekundil. Mõlema päring loeb faili, lisab '
        'oma arvustuse ja kirjutab faili tagasi. Kes kirjutab viimasena, kirjutab teise töö üle, ja üks arvustus kaob.',
        '<b>Otsimine.</b> Et leida miljoni arvustuse seast kõik hernesupi omad, peab programm läbi lugema terve faili.',
        '<b>Pooleli jäänud fail.</b> Kui server kukub keset kirjutamist, võib fail jääda pooleli ja ükski arvustus pole '
        'enam loetav.',
    ),
    p('Just nende murede lahendamiseks ongi andmebaasid tehtud.'),

    p('Andmebaas ja andmebaasisüsteem', h2),
    p('<b>Andmebaas</b> on korrastatud andmete kogum. <b>Andmebaasisüsteem</b> (ingl <i>database management system</i>, '
      'DBMS) on programm, mis neid andmeid hoiab. See salvestab andmed kettale, leiab need kiiresti üles ja hoolitseb, et '
      'kaks samaaegset kirjutajat üksteist ei segaks. Igapäevakõnes öeldakse mõlema kohta lihtsalt „andmebaas“. MySQL, '
      'PostgreSQL ja SQLite on andmebaasisüsteemid.'),
    p('Meie server ei hakka ise faile kirjutama. Ta ütleb andmebaasile: „anna kõik arvustused“ või „lisa see arvustus“, '
      'ja andmebaas teeb ülejäänu.'),

    p('Tabel: read ja veerud', h2),
    p('Kõige levinum andmebaasi liik on <b>relatsiooniline andmebaas</b>. Seal on andmed tabelites, natuke nagu Excelis. '
      'Söökla arvustused näeksid välja nii:'),
    arvustused_table(),
    *bullets(
        '<b>Veerg</b> on üks omadus, näiteks hinne. Igal veerul on kindel andmetüüp: ' + c('hinne') + ' on täisarv, '
        + c('toit') + ' on tekst. Enamik andmebaase ei lase täisarvu veergu teksti kirjutada. SQLite, mida kasutame '
        'järgmisel korral, on leebem ja võtab vaikimisi vastu ka sobimatu väärtuse, nii et sisendit kontrollib ikka '
        'meie server, nagu kontrolltöös.',
        '<b>Rida</b> ehk kirje on üks arvustus.',
        '<b>Primaarvõti</b> on veerg, mis eristab iga rida teistest. Meil on see ' + c('id') + ': kahel real ei tohi '
        'olla sama id.',
    ),
    p('Võrdle seda serveri massiiviga. Massiivi üks objekt on tabeli üks rida ja objekti võtmed on veerud:'),
    code("{ id: 2, toit: 'Hernesupp', hinne: 3, kommentaar: 'Natuke liiga paks.' }"),
    p('Tabelit olete seega juba kasutanud. See lihtsalt elas mälus.'),

    p('Mitu tabelit ja võõrvõti', h2),
    p('Mis siis, kui tahame hoida ka toidu hinda? Võiksime lisada igale arvustusele veeru ' + c('hind') + ', aga siis '
      'kordub hernesupi hind igas hernesupi arvustuses. Kui hind muutub, tuleb see parandada kümnes kohas ja mõni jääb '
      'kindlasti parandamata.'),
    p('Parem on teha kaks tabelit. Toidud on eraldi ja arvustus viitab toidule selle id kaudu. Sellist viitavat veergu '
      'nimetatakse <b>võõrvõtmeks</b>.'),
    table(['id', 'nimi', 'hind'], [['1', 'Kanakaste riisiga', '2,10'], ['2', 'Hernesupp', '1,80'],
                                   ['3', 'Makaronid hakklihaga', '2,00']],
          [WIDTH * 0.1, WIDTH * 0.5, WIDTH * 0.2]),
    KeepTogether([
        p('Ülal tabel <b>toidud</b>, all tabel <b>arvustused</b>. Veerg ' + c('toidu_id') + ' on võõrvõti: see viitab '
          'tabeli toidud ühele reale.'),
        plain_table(['id', 'toidu_id', 'hinne', 'kommentaar'], [['1', '1', '5', 'Parim toit sel nädalal!'],
                                                          ['2', '2', '3', 'Natuke liiga paks.'],
                                                          ['3', '2', '4', 'Täna oli parem.']],
              [WIDTH * 0.1, WIDTH * 0.16, WIDTH * 0.12, WIDTH * 0.52]),
    ]),
    p('Nüüd on hernesupi hind kirjas ainult ühes kohas. Nimi „relatsiooniline“ tuleb matemaatikast, kus sellist tabelit '
      'nimetatakse relatsiooniks. Tabeleid võtmete kaudu omavahel siduda ongi relatsioonilise andmebaasi suur tugevus.'),
    proovi('1', 'Vaata kahte ülemist tabelit. Arvustusel number 3 on ' + c('toidu_id = 2') + '. Mis toitu see arvustab '
                'ja kui palju see toit maksab?'),

    p('SQL: keel, millega andmebaasiga räägitakse', h2),
    p('Relatsioonilise andmebaasiga suheldakse keeles <b>SQL</b> (<i>Structured Query Language</i>). SQL-is ei kirjuta '
      'sa, kuidas andmeid otsida, vaid ütled, mida tahad saada. Kuidas see kõige kiiremini leida, otsustab andmebaas ise.'),
    p('Vaatame nelja käsku. Need peaksid tuttavad tunduma, sest neid saab võrrelda meetoditega, mida kontrolltöös '
      'kasutasite. Vastavus on ligikaudne: HTTP ja SQL töötavad eri kohtades ja üks GET-päring võib serveris teha ka mitu '
      'andmebaasipäringut. Meelde jätmiseks sobib see tabel aga hästi:'),
    table(['HTTP-meetod', 'SQL-käsk', 'Mida teeb'], [
        [c('GET'), c('SELECT'), 'loeb andmeid'],
        [c('POST'), c('INSERT'), 'lisab uue rea'],
        [c('PUT') + ' või ' + c('PATCH'), c('UPDATE'), 'muudab olemasolevat rida'],
        [c('DELETE'), c('DELETE'), 'kustutab rea'],
    ], [WIDTH * 0.25, WIDTH * 0.2, WIDTH * 0.55]),
    p('Kõik näited käivad esimese tabeli <b>arvustused</b> kohta, kus on veerud ' + c('id') + ', ' + c('toit') + ', '
      + c('hinne') + ' ja ' + c('kommentaar') + '.'),

    p('<b>SELECT</b> loeb. Tärn tähendab kõiki veerge, nii et see annab kogu tabeli:'),
    code('SELECT * FROM arvustused;'),
    p('Tavaliselt tahame aga ainult osa. ' + c('WHERE') + ' valib read, ' + c('ORDER BY') + ' järjestab need, ' + c('DESC')
      + ' tähendab suuremast väiksemani:'),
    code('''
SELECT toit, hinne FROM arvustused
WHERE hinne >= 4
ORDER BY hinne DESC;
'''),
    p('Tulemus on kaks rida: Kanakaste riisiga 5 ja Makaronid hakklihaga 4. Hernesupp jääb välja, sest 3 on alla 4.'),

    p('<b>INSERT</b> lisab uue rea. Kõigepealt veergude nimed, siis samas järjekorras väärtused:'),
    code('''
INSERT INTO arvustused (toit, hinne, kommentaar)
VALUES ('Seljanka', 4, 'Hea ja vürtsikas.');
'''),
    p('Veeru ' + c('id') + ' jätame ära. Kui tabel on nii seadistatud, annab andmebaas uuele reale ise järgmise numbri, '
      'ja just nii me selle järgmisel korral teemegi. Tekst käib ülakomade vahele, arvud ilma.'),

    KeepTogether([p('<b>UPDATE</b> muudab olemasolevat rida. ' + c('SET') + ' ütleb, mida muuta, ' + c('WHERE')
                    + ' ütleb, millist rida:'),
                  *code_parts('''
UPDATE arvustused
SET hinne = 4
WHERE id = 2;
''')]),
    p('<b>DELETE</b> kustutab:'),
    code('''
DELETE FROM arvustused
WHERE id = 3;
'''),
    note('<b>Ettevaatust:</b> ' + c('UPDATE') + ' ja ' + c('DELETE') + ' ilma ' + c('WHERE') + '-ta muudavad või '
         'kustutavad tabeli kõik read. Käsk ' + c('DELETE FROM arvustused;') + ' tühjendab terve tabeli ja '
         'andmebaas ei küsi üle. Kirjuta ' + c('WHERE') + ' alati enne, kui käsu käivitad.'),
    p('SQL-i käsusõnad kirjutatakse tavaliselt suurtähtedega, et neid tabelite ja veergude nimedest eristada. Andmebaas '
      'saaks aru ka väiketähtedest. Käsu lõpus on semikoolon.'),
    proovi('2', 'Tabelis <b>arvustused</b> on veerud ' + c('id') + ', ' + c('toit') + ', ' + c('hinne') + ' ja '
                + c('kommentaar') + '. Kirjuta SQL-is: <b>a)</b> kõik arvustused, mille hinne on 3 või vähem; <b>b)</b> lisa arvustus toidule '
                '„Kartulipuder“, hinne 5, kommentaar „Nagu kodus.“; <b>c)</b> kustuta arvustus, mille id on 1.'),
    proovi('3', 'Mida annab see päring tabeli <b>arvustused</b> peal (sama, mis eespool)? ' + c("SELECT kommentaar FROM arvustused WHERE toit = "
                                                                 "'Hernesupp';")),

    p('Üks oht: SQL-i süstimine', h2),
    p('Järgmisel korral paneme serveri SQL-i saatma ja seal on üks lõks. Kui panna kasutaja kirjutatud tekst otse SQL-i '
      'sisse, võib pahatahtlik kasutaja kirjutada kommentaari asemel hoopis SQL-i käsu ja andmebaas täidab selle. Seda '
      'nimetatakse <b>SQL-i süstimiseks</b> (ingl <i>SQL injection</i>) ja see on üks levinumaid turvavigu veebis.'),
    p('Kaitse on lihtne: kasutaja andmed antakse andmebaasile eraldi, neid ei liimita SQL-i teksti sisse. Kuidas see käib, '
      'näeme järgmisel korral.'),

    p('Kõik andmebaasid pole tabelid: NoSQL', h2),
    p('Relatsiooniline andmebaas sobib enamikule rakendustele. Mõnikord on andmed aga teistsugused: neid on tohutult '
      'palju, need muutuvad väga kiiresti või neil pole kindlat kuju. Selleks on loodud andmebaasid, mida kutsutakse '
      'ühise nimega <b>NoSQL</b>. Nimi on eksitav: see ei tähenda „SQL on keelatud“, vaid pigem „mitte ainult SQL“. '
      'Mõnel neist on isegi SQL-i moodi päringukeel.'),
    table(['Liik', 'Kuidas andmed välja näevad', 'Näide', 'Sobib'], [
        ['relatsiooniline', 'tabelid ridade ja veergudega, päringud SQL-is', 'MySQL, PostgreSQL, MariaDB, SQLite',
         'enamik rakendusi: poed, koolid, pangad'],
        ['dokumendiandmebaas', 'JSON-i moodi dokumendid, igaühel võib olla oma kuju', 'MongoDB',
         'andmed, mille kuju muutub tihti'],
        ['võti-väärtus', 'võti ja selle väärtus nagu JavaScripti objektis, sageli mälus', 'Redis',
         'vahemälu, sisselogimised, edetabelid'],
        ['laia veeruga', 'hiiglaslikud tabelid, mis on jagatud paljude serverite vahel', 'Cassandra',
         'väga suured andmehulgad, palju kirjutamist'],
    ], [WIDTH * 0.24, WIDTH * 0.3, WIDTH * 0.2, WIDTH * 0.26]),
    KeepTogether([p('Nii võiks hernesupi arvustus välja näha dokumendiandmebaasis:'),
                  *code_parts('{ "toit": "Hernesupp", "hinne": 3, "kommentaar": "Natuke liiga paks.", "sildid": ["supp", "soe"] }')]),
    p('Pane tähele, et dokumendi sees võib olla ka nimekiri. Relatsioonilises andmebaasis tehakse siltide jaoks '
      'tavaliselt eraldi tabel.'),

    p('Kus andmebaas elab?', h2),
    p('<b>SQLite</b> on lihtsalt üks fail, näiteks ' + c('sookla.db') + ', ja andmebaas töötab sinu programmi sees. '
      'Eraldi midagi käivitama ei pea. Seepärast kasutame meie just seda.'),
    p('<b>MySQL</b>, <b>PostgreSQL</b> ja enamik teisi on eraldi serverid. Need on programmid, mis kuulavad oma pordil, '
      'PostgreSQL vaikimisi 5432 ja MySQL 3306, täpselt nagu sinu Express kuulab porti 3000. Sinu server saadab neile '
      'päringu ja saab vastuse.'),
    p('Suures rakenduses on seega kolm osa, nagu 5. tunnis joonistasime. Brauser räägib serveriga HTTP kaudu, server '
      'räägib andmebaasiga SQL-is. Meie rakenduses, nagu enamikus veebirakendustes, ei räägi brauser andmebaasiga '
      'otse.'),

    CondPageBreak(200),
    p('Mida tunnis teeme', h2),
    *numbered([
        '<b>Teooria.</b> Läbime selle konspekti peamised mõtted.',
        '<b>Meeskonnad.</b> Jaguneme 4–5 meeskonda ja iga meeskond valib ühe populaarse andmebaasi. Nimekiri ja küsimused, '
        'millele esitlus vastab, on rühmatöö lehel.',
        '<b>Esitluse tegemine.</b> Uurite oma andmebaasi internetist ja teete kuni 6 slaidi. Saatke esitlus enne esitluste '
        'algust aadressile <b>mtsopo@taltech.ee</b>.',
        '<b>Esitlused.</b> Iga meeskond esitab kuni 5 minutit ja küsib lõpus klassilt ühe küsimuse.',
    ]),

    p('Järgmisel korral', h2),
    p('Söökla server saab SQLite’i andmebaasi. Massiiv ' + c('arvustused') + ' kaob koodist ja GET, POST ning DELETE '
      'loevad ja kirjutavad andmebaasi. Kui server siis taaskäivitub, on kõik arvustused alles.'),

    CondPageBreak(330),
    p('Sõnastik', h2),
    table(['Sõna', 'Tähendus'], [
        ['<b>andmebaas</b>', 'korrastatud andmete kogum'],
        ['<b>andmebaasisüsteem (DBMS)</b>', 'programm, mis andmeid hoiab ja otsib, näiteks PostgreSQL või SQLite'],
        ['<b>relatsiooniline andmebaas</b>', 'andmebaas, kus andmed on tabelites ja päringud kirjutatakse SQL-is'],
        ['<b>tabel, rida, veerg</b>', 'andmete kogum; üks kirje; üks omadus kindla andmetüübiga'],
        ['<b>primaarvõti</b>', 'veerg, mille väärtus on igal real erinev, tavaliselt id'],
        ['<b>võõrvõti</b>', 'veerg, mis viitab teise tabeli reale selle primaarvõtme kaudu'],
        ['<b>SQL</b>', 'keel, millega relatsioonilise andmebaasiga suheldakse'],
        ['<b>SELECT, INSERT, UPDATE, DELETE</b>', 'loe, lisa, muuda, kustuta'],
        ['<b>SQL-i süstimine</b>', 'turvaviga: kasutaja tekst satub SQL-i sisse ja andmebaas täidab selle käsuna'],
        ['<b>NoSQL</b>', 'andmebaasid, mis ei hoia andmeid relatsioonilistes tabelites, näiteks MongoDB ja Redis'],
    ], [WIDTH * 0.34, WIDTH * 0.66]),

    CondPageBreak(200),
    p('„Proovi ise“ vastused', h2),
    *numbered([
        'Hernesuppi, see maksab 1,80 €.',
        '<b>a)</b> ' + c('SELECT * FROM arvustused WHERE hinne <= 3;') + '<br/><b>b)</b> '
        + c("INSERT INTO arvustused (toit, hinne, kommentaar) VALUES ('Kartulipuder', 5, 'Nagu kodus.');")
        + '<br/><b>c)</b> ' + c('DELETE FROM arvustused WHERE id = 1;'),
        'Ühe rea, kus on ainult kommentaar „Natuke liiga paks.“',
    ]),
]


# ---------------------------------------------------------------- rühmatöö

def db_row(n, name, site, hint):
    return [f'<b>{n}</b>', f'<b>{name}</b>', c(site), hint]


tunnitoo = [
    p('Rühmatöö: andmebaasid', title),
    subtitle('11. tund', 'rühmatöö'),
    p('Pärast teooriat jagunete 4–5 meeskonda. Iga meeskond valib ühe populaarse andmebaasi, uurib seda internetist ja '
      'tutvustab seda klassile. Kõik meeskonnad vastavad samadele küsimustele, nii et lõpuks saame andmebaase omavahel '
      'võrrelda.', intro),

    p('Reeglid', h2),
    *bullets(
        'Meeskonnas on 3–5 inimest. Esitluses räägib igaüks vähemalt korra.',
        'Igal meeskonnal on erinev andmebaas. Kes valib esimesena, see saab.',
        'Esitlus kestab <b>kõige rohkem 5 minutit</b>. Õpetaja hoiab aega ja viie minuti pärast esitlus lõpeb, ükskõik '
        'kus te parasjagu olete. Proovige korra läbi.',
        'Slaide on kuni 6, igal slaidil vähe teksti. Selgitus tuleb teie suust.',
        'Esitluses on <b>üks näide</b>: päring või andmed sellel kujul, nagu teie andmebaas neid hoiab.',
        'Lõpus esitate klassile <b>ühe küsimuse</b>, millele saab teie esitluse põhjal vastata. Ka küsimus ja vastus '
        'mahuvad nende viie minuti sisse.',
        'Viimasel slaidil on vähemalt kaks allikat: andmebaasi enda koduleht (aadress on tabelis) ja veel üks. '
        'Kontrollige, et fakt on värske, sest mõni firma on andmebaasi vahetanud ja vanad artiklid seda ei tea.',
        'Esitluse võite teha PowerPointis, Google Slidesis või Canvas.',
    ),

    p('Saatmine', h2),
    p('Saatke esitlus <b>enne esitluste algust</b> aadressile <b>mtsopo@taltech.ee</b>. Esitlusi näitame õpetaja '
      'arvutist, nii et ilma saatmata pole midagi näidata. Kirja pange:'),
    *bullets(
        'andmebaasi nimi ja kõigi meeskonnaliikmete nimed;',
        'fail (.pptx või .pdf) või Google Slidesi või Canva link, mille saab lingiga avada;',
        'faili nimi kujul ' + c('tund11-postgresql-Mari-Jaan-Kati.pptx') + '.',
    ),

    p('Tunni ajakava', h2),
    table(['Aeg', 'Mis toimub'], [
        ['0–20 min', 'Teooria: miks andmebaas, tabelid ja võtmed, SQL, NoSQL. Kõik on ka konspektis.'],
        ['20–25 min', 'Meeskonnad ja andmebaasi valik.'],
        ['25–60 min', 'Esitluse tegemine. Jagage töö kohe ära: kes uurib mida, kes teeb slaidid. Viimase viie minuti '
                      'jooksul harjutage esitlust, kontrollige selle kestust ja saatke fail ära.'],
        ['60–90 min', 'Esitlused, igaüks koos küsimusega klassile kuni 5 minutit.'],
    ], [WIDTH * 0.18, WIDTH * 0.82]),

    CondPageBreak(260),
    p('Andmebaasid, mille seast valida', h2),
    table(['', 'Andmebaas', 'Koduleht', 'Vihje alustamiseks'], [
        db_row(1, 'MySQL', 'mysql.com', 'üks maailma levinumaid; miks on nimes „My“?'),
        db_row(2, 'PostgreSQL', 'postgresql.org', 'sündis ülikoolis; mis seos on sellel Eesti tuntud firmaga Skype?'),
        db_row(3, 'MariaDB', 'mariadb.org', 'mis seos on sellel MySQL-iga ja miks see tehti?'),
        db_row(4, 'SQLite', 'sqlite.org', 'meie järgmise tunni andmebaas; miks on see sinu telefonis?'),
        db_row(5, 'MongoDB', 'mongodb.com', 'dokumendiandmebaas; kuidas andmed välja näevad?'),
        db_row(6, 'Cassandra', 'cassandra.apache.org', 'laia veeruga andmebaas; mis firma selle tegi ja milleks?'),
        db_row(7, 'Redis', 'redis.io', 'võti-väärtus mälus; miks see on nii kiire ja mis juhtub, kui server välja '
                                       'lülitub?'),
    ], [WIDTH * 0.05, WIDTH * 0.16, WIDTH * 0.29, WIDTH * 0.5]),

    p('Millele esitlus vastab', h2),
    p('Küsimused on igal meeskonnal samad. <b>Kohustuslikud on 1, 2, 5 ja 7.</b> Küsimused 3, 4 ja 6 lisage, kui '
      'aega jääb. Mitu küsimust võib panna ühele slaidile.'),
    *numbered([
        '<b>Liik.</b> Mis liiki andmebaas see on: relatsiooniline, dokumendiandmebaas, võti-väärtus või laia veeruga?',
        '<b>Ajalugu.</b> Kes selle tegi ja millal? Üks huvitav fakt.',
        '<b>Hind ja litsents.</b> Kas see on tasuta? Kas lähtekood on avatud? Kes selle eest täna hoolitseb?',
        '<b>Kasutajad.</b> Kaks-kolm tuntud firmat või rakendust, mis seda kasutavad.',
        '<b>Näide.</b> Üks päring või andmete näide sellel kujul, nagu teie andmebaas neid hoiab.',
        '<b>Tugevused ja nõrkused.</b> Milleks see sobib hästi ja milleks mitte?',
        '<b>Söökla.</b> Kas valiksite selle meie söökla rakendusele? Miks?',
    ]),
]


BUILDS = {
    'andmebaasid-konspekt': ('Andmebaasid', konspekt),
    'tunnitoo-andmebaasid': ('Rühmatöö: andmebaasid', tunnitoo),
}

if __name__ == '__main__':
    for name in sys.argv[1:] or BUILDS:
        doc_title, story = BUILDS[name]
        build(f'public/files/{name}.pdf', doc_title, f'{SUBJECT} · {doc_title}', story, SUBJECT)
