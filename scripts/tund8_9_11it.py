# Builds the 11IT lesson 8 and 9 PDFs in public/files/:
#   react-server-konspekt.pdf, tunnijuhend-react-server.pdf, kodutoo-react-server.pdf (fillable),
#   lisamine-kustutamine-konspekt.pdf, tunnijuhend-lisamine.pdf and kodutoo-lisamine.pdf (fillable).
# Needs ReportLab (pip install reportlab) and the macOS system fonts Arial and Menlo.
# Run from the project root: python scripts/tund8_9_11it.py
# To build only some of them: python scripts/tund8_9_11it.py react-server-konspekt
import math
import sys

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import CondPageBreak, KeepTogether, Paragraph, Preformatted, Spacer, Table, TableStyle

from pdf_common import (BLUE, NAVY, PALE, WIDTH, Field, build, bullet, bullets, c, caption, code, code_parts, explain,
                        h2, intro, label, label_b, note, p, question, row, sub, table, title)

SUBJECT = '11IT · Veebirakendused'
MUTED = HexColor('#7A8BA3')
GREEN = HexColor('#2E8B57')
figcap = ParagraphStyle('figcap', fontName='Sans', fontSize=8.5, leading=11, textColor=BLUE, alignment=1,
                        spaceBefore=2, spaceAfter=4)
small_code = ParagraphStyle('small_code', fontName='Mono', fontSize=7.4, leading=10, textColor=NAVY)


def subtitle(lesson, kind):
    return p(f'{SUBJECT} · {lesson} · {kind}', sub)


def proovi(number, text_):
    return note(f'<b>Proovi ise {number}.</b> {text_}')


def numbered(items):
    return [Paragraph(i, bullet, bulletText=f'{n}.') for n, i in enumerate(items, 1)]


def figure(drawing, text_):
    return KeepTogether([drawing, p(text_, figcap), Spacer(1, 6)])


def see(text_):
    """What the student should now see on screen."""
    return p('<b>Nüüd peaksid nägema:</b> ' + text_)


def stuck(text_):
    """What to do when the screen shows something else."""
    return p('<b>Kui näed midagi muud:</b> ' + text_)


def code_file(text_, filename):
    """A whole file in smaller letters, so that the longest lines still fit in the box."""
    lines = text_.strip('\n').split('\n')
    # One table cell can't split across pages, so a long file becomes several boxes.
    chunks = []
    while lines:
        end = len(lines)
        if end > 55:
            end = next(i for i in range(55, 0, -1) if lines[i] == '')
        chunks.append(lines[:end])
        lines = lines[end:]
        if lines and lines[0] == '':
            lines = lines[1:]
    boxes = []
    for chunk in chunks:
        t = Table([[Preformatted('\n'.join(chunk), small_code)]], colWidths=[WIDTH])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), PALE),
            ('LINEBEFORE', (0, 0), (0, -1), 3, BLUE),
            ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        t.hAlign = 'LEFT'
        boxes.append(t)
    return [KeepTogether([Paragraph(filename, caption), boxes[0]]), *boxes[1:], Spacer(1, 8)]


# ---------------------------------------------------------------- joonised

def text(d, x, y, s, size=9, color=NAVY, font='Sans', anchor='middle'):
    d.add(String(x, y, s, fontName=font, fontSize=size, fillColor=color, textAnchor=anchor))


def arrow(d, x1, y1, x2, y2, color=BLUE):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.4))
    ang = math.atan2(y2 - y1, x2 - x1)
    s = 6
    d.add(Polygon([x2, y2, x2 - s * math.cos(ang - 0.4), y2 - s * math.sin(ang - 0.4),
                   x2 - s * math.cos(ang + 0.4), y2 - s * math.sin(ang + 0.4)], fillColor=color, strokeColor=color))


def box(d, x, y, w, h, name, detail, fill=PALE):
    d.add(Rect(x, y, w, h, fillColor=fill, strokeColor=BLUE, strokeWidth=1, rx=5, ry=5))
    text(d, x + w / 2, y + h / 2 + 3, name, 10, NAVY, 'Sans-Bold')
    text(d, x + w / 2, y + h / 2 - 11, detail, 8, BLUE)


def proxy_drawing():
    d = Drawing(WIDTH, 112)
    w, h, y = 110, 52, 36
    xs = [4, (WIDTH - w) / 2, WIDTH - w - 4]
    box(d, xs[0], y, w, h, 'Brauser', 'sinu lehekülg')
    box(d, xs[1], y, w, h, 'Vite', 'port 5173')
    box(d, xs[2], y, w, h, 'Express', 'port 3000')
    for a, b in [(0, 1), (1, 2)]:
        arrow(d, xs[a] + w + 4, y + 36, xs[b] - 4, y + 36)
        arrow(d, xs[b] - 4, y + 14, xs[a] + w + 4, y + 14, GREEN)
    text(d, (xs[0] + w + xs[1]) / 2, y + 42, '1. päring', 8)
    text(d, (xs[1] + w + xs[2]) / 2, y + 42, '2. edasi', 8)
    text(d, (xs[1] + w + xs[2]) / 2, y + 2, '3. vastus', 8, GREEN)
    text(d, (xs[0] + w + xs[1]) / 2, y + 2, '4. vastus', 8, GREEN)
    text(d, WIDTH / 2, 100, 'kumbki server töötab oma terminalis', 8.5, MUTED)
    text(d, WIDTH / 2, 14, 'brauser räägib ainult Vite’iga, Vite räägib serveriga', 8.5, MUTED)
    return d


def methods_drawing():
    d = Drawing(WIDTH, 92)
    rows = [('GET', '/api/arvustused', 'anna kõik arvustused', '200 ja nimekiri', 70),
            ('POST', '/api/arvustused', 'lisa see uus arvustus', '201 ja uus arvustus', 42),
            ('DELETE', '/api/arvustused/2', 'kustuta arvustus number 2', '200 ja kustutatud', 14)]
    for method, path, meaning, answer, y in rows:
        d.add(Rect(2, y - 5, 50, 18, fillColor=BLUE, strokeColor=None, rx=3, ry=3))
        text(d, 27, y, method, 8.5, white, 'Sans-Bold')
        text(d, 60, y, path, 8.5, NAVY, 'Mono', 'start')
        text(d, 170, y, meaning, 8.5, NAVY, 'Sans', 'start')
        arrow(d, 300, y + 3, 330, y + 3, GREEN)
        text(d, 338, y, answer, 8.5, GREEN, 'Sans', 'start')
    return d


# ---------------------------------------------------------------- koodid, täpselt nagu proovitud projektis

VITE_CONFIG = '''
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:3000',
    },
  },
})
'''

APP_8 = '''
import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import type { Arvustus } from './types';
import ArvustuseKaart from './ArvustuseKaart';
import './App.css';

export default function App() {
  const [arvustused, setArvustused] = useState<Arvustus[]>([]);
  const [laeb, setLaeb] = useState(true);
  const [viga, setViga] = useState('');
  const [toit, setToit] = useState('');
  const [hinne, setHinne] = useState(5);
  const [kommentaar, setKommentaar] = useState('');

  async function laeArvustused() {
    try {
      const vastus = await fetch('/api/arvustused');
      if (!vastus.ok) {
        throw new Error('Server vastas veaga');
      }
      const andmed: Arvustus[] = await vastus.json();
      setArvustused(andmed);
    } catch {
      setViga('Arvustusi ei saanud kätte. Kas server töötab?');
    }
    setLaeb(false);
  }

  useEffect(() => {
    laeArvustused();
  }, []);

  function lisa(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const uus: Arvustus = { id: Date.now(), toit, hinne, kommentaar };
    setArvustused([uus, ...arvustused]);
    setToit('');
    setHinne(5);
    setKommentaar('');
  }

  return (
    <main>
      <h1>Söökla arvustused</h1>

      <form onSubmit={lisa}>
        <input value={toit} onChange={(e) => setToit(e.target.value)} placeholder="Mis toit?" />
        <select value={hinne} onChange={(e) => setHinne(Number(e.target.value))}>
          <option value={5}>5 ★</option>
          <option value={4}>4 ★</option>
          <option value={3}>3 ★</option>
          <option value={2}>2 ★</option>
          <option value={1}>1 ★</option>
        </select>
        <input
          value={kommentaar}
          onChange={(e) => setKommentaar(e.target.value)}
          placeholder="Kommentaar"
        />
        <button type="submit">Lisa</button>
      </form>

      {laeb && <p className="kokku">Laen arvustusi…</p>}
      {viga && <p className="kokku">{viga}</p>}

      <ul>
        {arvustused.map((a) => (
          <ArvustuseKaart key={a.id} arvustus={a} />
        ))}
      </ul>
    </main>
  );
}
'''

SERVER_9 = '''
const express = require('express');

const app = express();

app.use(express.json());

let arvustused = [
  { id: 1, toit: 'Kanakaste riisiga', hinne: 5, kommentaar: 'Parim toit sel nädalal!' },
  { id: 2, toit: 'Hernesupp', hinne: 3, kommentaar: 'Natuke liiga paks.' },
  { id: 3, toit: 'Makaronid hakklihaga', hinne: 4, kommentaar: 'Klassika, alati hea.' },
];
let jargmineId = 4;

app.get('/', (req, res) => {
  res.send('Tere! Söökla server töötab.');
});

app.get('/api/arvustused', (req, res) => {
  res.json(arvustused);
});

app.post('/api/arvustused', (req, res) => {
  const { toit, hinne, kommentaar } = req.body;

  const toitOnKorras = typeof toit === 'string' && toit.trim() !== '';
  const kommentaarOnKorras = typeof kommentaar === 'string' && kommentaar.trim() !== '';
  const hinneOnKorras = Number.isInteger(hinne) && hinne >= 1 && hinne <= 5;

  if (!toitOnKorras || !kommentaarOnKorras || !hinneOnKorras) {
    res.status(400).json({ viga: 'Täida kõik lahtrid, hinne on 1 kuni 5.' });
    return;
  }

  const uus = { id: jargmineId, toit: toit.trim(), hinne, kommentaar: kommentaar.trim() };
  jargmineId = jargmineId + 1;
  arvustused = [uus, ...arvustused];
  res.status(201).json(uus);
});

app.delete('/api/arvustused/:id', (req, res) => {
  const id = Number(req.params.id);
  const leitud = arvustused.find((a) => a.id === id);

  if (!leitud) {
    res.status(404).json({ viga: 'Sellist arvustust pole.' });
    return;
  }

  arvustused = arvustused.filter((a) => a.id !== id);
  res.json(leitud);
});

app.get('/api/menyy', (req, res) => {
  res.json(['Hernesupp', 'Kanakaste riisiga', 'Pannkoogid']);
});

app.listen(3000, () => {
  console.log('Server töötab: http://localhost:3000');
});
'''

KAART_9 = '''
import type { Arvustus } from './types';

type Props = {
  arvustus: Arvustus;
  kustuta: (id: number) => void;
};

export default function ArvustuseKaart({ arvustus, kustuta }: Props) {
  const tahed = '★'.repeat(arvustus.hinne) + '☆'.repeat(5 - arvustus.hinne);
  return (
    <li className="kaart">
      <div className="kaart-pea">
        <strong>{arvustus.toit}</strong>
        <span className="tahed">{tahed}</span>
      </div>
      <p>{arvustus.kommentaar}</p>
      <button type="button" onClick={() => kustuta(arvustus.id)}>Kustuta</button>
    </li>
  );
}
'''

LISA_9 = '''
  async function lisa(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setViga('');

    try {
      const vastus = await fetch('/api/arvustused', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ toit, hinne, kommentaar }),
      });
      const andmed = await vastus.json();

      if (!vastus.ok) {
        setViga(andmed.viga);
        return;
      }

      setArvustused((praegused) => [andmed, ...praegused]);
      setToit('');
      setHinne(5);
      setKommentaar('');
    } catch {
      setViga('Serveriga ei saanud ühendust. Kas server töötab?');
    }
  }
'''

KUSTUTA_9 = '''
  async function kustuta(id: number) {
    setViga('');

    try {
      const vastus = await fetch(`/api/arvustused/${id}`, { method: 'DELETE' });
      const andmed = await vastus.json();

      if (!vastus.ok) {
        setViga(andmed.viga);
        return;
      }

      setArvustused((praegused) => praegused.filter((a) => a.id !== id));
    } catch {
      setViga('Serveriga ei saanud ühendust. Kas server töötab?');
    }
  }
'''

LAE_8 = APP_8[APP_8.index('  async function laeArvustused'):APP_8.index('  function lisa(e')].rstrip() + '\n'
APP_9 = APP_8[:APP_8.index('  function lisa(e')] + LISA_9.lstrip('\n') + '\n' + KUSTUTA_9.lstrip('\n') + '\n' \
    + APP_8[APP_8.index('  return (\n    <main>'):].replace('arvustus={a} />', 'arvustus={a} kustuta={kustuta} />')


CHECK_9 = SERVER_9[SERVER_9.index('  const toitOnKorras'):SERVER_9.index('  const uus =')].rstrip()
NEW_9 = SERVER_9[SERVER_9.index('  const uus ='):SERVER_9.index("app.delete(")].rstrip().removesuffix('});').rstrip()
DELETE_9 = SERVER_9[SERVER_9.index("app.delete("):SERVER_9.index("app.get('/api/menyy'")].rstrip()


# ---------------------------------------------------------------- 8. tund: konspekt

konspekt_8 = [
    p('React küsib andmed serverilt', title),
    subtitle('8. tund', 'konspekt'),
    note('Selles konspektis selgitan kõik mõisted uuesti läbi, ka need, mida oleme varem kasutanud. See on meelega: mida '
         'rohkem kordi sama mõtet kuuled, seda kindlamalt see pähe jääb. Koodi käivitamiseks on vaja Node.js-i, npm-i, '
         'VS Code’i ja söökla projekti, mille saad ka kursuse lehelt alla laadida. Lahenda „Proovi ise“ kastid, vastused '
         'on lõpus.<br/><br/>'
         '<b>Pärast seda tundi oskad:</b><br/>'
         '• panna Reacti lehe ja serveri korraga tööle ning selgitada, kes kellega räägib;<br/>'
         '• tuua lehe avanemisel andmed serverist ja panna need ekraanile;<br/>'
         '• näidata kasutajale laadimisteadet ja veateadet.<br/><br/>'
         'Kõige tähtsam on teine punkt. Läbivalt võrdleme kõike restoraniga.'),

    p('Mis täna muutub?', h2),
    p('Meie söökla rakenduse lehel on arvustused. Kust need tulevad? Praegu failist ' + c('andmed.ts') + ', mis asub '
      'lehe enda koodi sees. Need on näidisandmed. Justkui toidupilt menüüs: näeb välja nagu päris, aga köögist pole '
      'keegi midagi toonud.'),
    p('Samal ajal on sul olemas ka päris köök ehk server, mis oskab samad arvustused välja anda. Need kaks ei tea '
      'teineteisest midagi. Täna ühendame nad. Fail ' + c('andmed.ts') + ' läheb prügikasti ja leht küsib andmed '
      'serverilt.'),

    p('Klient, server, päring, vastus', h2),
    p('Kõigepealt neli sõna, millel kogu tänane tund seisab.'),
    table(['Restoranis', 'Veebis', 'Mis see on'], [
        ['Sina laua taga', '<b>klient</b>', 'Programm, mis saadab päringuid. Meil on selleks brauser ja selles töötav '
                                            'Reacti leht.'],
        ['Tellimus: „üks hernesupp“', '<b>päring</b>', 'Küsimus, mille klient saadab.'],
        ['Köök', '<b>server</b>', 'Programm, mis ootab päringuid ja vastab neile.'],
        ['Taldrik, mis lauale tuuakse', '<b>vastus</b>', 'See, mille server tagasi saadab.'],
    ], [WIDTH * 0.32, WIDTH * 0.14, WIDTH * 0.54]),
    Spacer(1, 6),
    p('Köök ei tee midagi enne, kui keegi tellib. Server samuti: ta käivitub ja jääb ootama. Seepärast ei tule terminali '
      'pärast serveri käivitamist uut käsurida. Terminal pole kinni jooksnud, server lihtsalt töötab.'),

    p('JSON: mis kujul arvustused liiguvad', h2),
    p('Interneti kaudu saab saata teksti, pilte, heli ja muid andmeid. Meie rakendus kasutab arvustuste saatmiseks '
      'JSON-vormingus teksti. <b>JSON</b> (loe „džeison“) on kokkulepe, kuidas andmed tekstina kirja panna, et teine pool '
      'neist aru saaks. Üks arvustus näeb JSON-ina välja nii:'),
    code('''
{ "id": 2, "toit": "Hernesupp", "hinne": 3, "kommentaar": "Natuke liiga paks." }
'''),
    p('Loogelised sulud tähendavad <b>objekti</b>: üks asi, millel on nimega väljad. Mitu asja järjest on <b>massiiv</b>, '
      'selle ümber on nurksulud:'),
    code('''
[ { "id": 1, "toit": "Kanakaste riisiga" }, { "id": 2, "toit": "Hernesupp" } ]
'''),
    proovi('1', 'Kas ' + c('[ { "id": 1 }, { "id": 2 }, { "id": 3 } ]') + ' on objekt või massiiv? Mitu elementi selles '
                'on?'),

    p('Terminal ja port', h2),
    p('<b>Terminal</b> on aken, kuhu kirjutad arvutile käske. Meil on täna neid vaja kaks tükki, sest korraga töötab kaks '
      'programmi ja kumbki hõivab oma terminali. Selles projektis on pordid sellised:'),
    table(['Programm', 'Mida teeb', 'Käsk', 'Port'], [
        ['<b>Vite</b>', 'annab brauserile sinu Reacti lehe', c('npm run dev'), '5173'],
        ['<b>Express</b>', 'annab välja arvustused', c('node index.js') + ' kaustas server', '3000'],
    ], [WIDTH * 0.15, WIDTH * 0.40, WIDTH * 0.33, WIDTH * 0.12]),
    Spacer(1, 6),
    p('Mis on <b>port</b>? Mõtle toidusaalile: üks maja, mitu letti, igal letil oma number. Sinu arvuti on maja ja selle '
      'aadress on ' + c('localhost') + ', mis tähendab „seesama arvuti“. Port on leti number: selle järgi teatakse, '
      'millisele programmile päring läheb. ' + c('localhost:3000') + ' tähendab „selles arvutis lett number 3000“. '
      'Vite’i vaikimisi port on 5173, aga kui see on juba kinni, võib ta võtta teise. Seepärast ava alati aadress, mille '
      'Vite terminali kirjutab.'),
    p('Kumbki programm jääb tööle, kuni paned ta kinni. Selleks on ' + c('Ctrl+C') + ' selles terminalis, kus ta töötab.'),
    proovi('2', 'Sul on lahti ' + c('http://localhost:3000/api/arvustused') + '. Kumb programm sellele vastab: Vite või '
                'Express?'),

    p('Miks brauser ei lase otse küsida?', h2),
    p('Võiks ju arvata, et leht kirjutab lihtsalt ' + c("fetch('http://localhost:3000/api/arvustused')") + ' ja kõik. '
      'Proovisin. Ei tööta! Brauseri konsoolis on punane veateade sõnaga <b>CORS</b>.'),
    p('Brauser võrdleb lehe ja päringu päritolu: protokolli, hostinime ja porti. Pordid 5173 ja 3000 on erinevad, seega '
      'vajab brauser vastuse lugemiseks serveri luba. Meie arendusprojektis kasutame päringu vahendamiseks Vite’i.'),
    p('Selleks on <b>proxy</b> (loe „proksi“) ehk vahendusserver. Restoranis on see teenindaja: sina räägid temaga ja tema '
      'viib tellimuse kööki. Brauser küsib Vite’ilt ' + c('/api/arvustused') + ', mis on lehega sama päritoluga. Vite '
      'saadab küsimuse serverile edasi ja toob vastuse tagasi.'),
    figure(proxy_drawing(), 'Päring käib läbi Vite’i, seepärast näeb brauser ainult ühte päritolu.'),
    p('Pane tähele, et ' + c('/api/arvustused') + ' algab kaldkriipsuga ja selles pole serveri nime ega porti. Selline '
      'aadress tähendab „sama koht, kust see leht tuli“. Vahendusserveri seadistus läheb faili ' + c('vite.config.ts')
      + ':'),
    code("""
server: {
  proxy: {
    '/api': 'http://localhost:3000',
  },
},
"""),
    p('Inimkeeles: kui aadress algab ' + c('/api') + '-ga, saada päring edasi aadressile ' + c('localhost:3000')
      + '. Kõik muu annab Vite ise. See seadistus kehtib Vite’i <b>arendusserveris</b>. Kui rakendus kunagi päriselt '
      'internetti panna, tuleb see lahendada teisiti.'),
    proovi('3', 'Brauser küsib ' + c('/api/menyy') + '. Kes vastab lõpuks? Aga kui brauser küsib ' + c('/favicon.svg')
                + '?'),

    p('React: komponent ja JSX', h2),
    p('React on teek, millega ehitatakse veebilehti tükkidest. Üks tükk on <b>komponent</b>. Komponent on funktsioon, '
      'mille nimi algab suure tähega ja mis tagastab selle, mida ekraanil näidata:'),
    code("""
export default function App() {
  return <h1>Söökla arvustused</h1>;
}
"""),
    p('See HTML-i moodi kirjutis on <b>JSX</b>. Loogelised sulud JSX-is tähendavad „siin on JavaScript“: ' + c('{toit}')
      + ' näitab muutuja ' + c('toit') + ' väärtust.'),

    p('useState: Reacti mälu', h2),
    p('Mõtle restorani seinal olevale tahvlile. Kui kirjutad tahvlile uue asja, näevad kõik seda kohe. Reactis on selline '
      'tahvel <b>olek</b> (ingl <i>state</i>) ja see tehakse käsuga ' + c('useState') + ':'),
    code("""
const [arvustused, setArvustused] = useState<Arvustus[]>([]);
"""),
    table(['Tükk', 'Tähendus'], [
        [c('arvustused'), 'mis tahvlil praegu kirjas on'],
        [c('setArvustused'), 'funktsioon, millega tahvlile uus asi kirjutada. Pärast seda joonistab React lehe uuesti.'],
        [c('<Arvustus[]>'), 'TypeScriptile: siin on massiiv, mille iga element on Arvustus'],
        [c('([])'), 'mis on alguses tahvlil: tühi massiiv'],
    ], [WIDTH * 0.28, WIDTH * 0.72]),
    Spacer(1, 6),
    p('Miks mitte tavaline muutuja? Tavalist muutujat muutes React ei tea, et midagi juhtus, ja ekraan jääb samaks.'),
    p('<b>TypeScript</b> on JavaScript, kuhu saab kirja panna andmete tüübi, näiteks et hinne on arv. Tüüp ' + c('Arvustus')
      + ' asub failis ' + c('src/types.ts') + ' ja see jääb alles, kuigi ' + c('andmed.ts') + ' kaob.'),

    p('fetch, async ja await: tellimuse esitamine', h2),
    p('Andmeid küsitakse käsuga ' + c('fetch') + '. Päring võtab aega, nagu toit köögist. ' + c('fetch()') + ' tagastab kohe '
      'Promise’i ehk lubaduse tulevase tulemuse kohta. Nagu teenindaja, kes ütleb „supp on tulemas“: supp ise pole veel '
      'laual. ' + c('await') + ' võimaldab kasutada tulemust pärast seda, kui see on kohale jõudnud.'),
    p('Meie näites peab ' + c('await') + '-i kasutava funktsiooni ees olema ' + c('async') + '. Funktsioon võib olla '
      + c('async') + ' ka siis, kui selles pole ' + c('await') + '-i. ' + c('await') + ' peatab ainult selle funktsiooni '
      'jätkamise, kogu leht ei jää seisma.'),
    code("""
async function laeArvustused() {
  const vastus = await fetch('/api/arvustused');
  const andmed: Arvustus[] = await vastus.json();
  setArvustused(andmed);
}
"""),
    explain([
        ['async function laeArvustused() {', 'Teeme funktsiooni. async lubab selles kasutada sõna await.'],
        ["const vastus = await fetch(\n  '/api/arvustused');", 'Saadab päringu ja ootab. vastus on nagu kaanega kaetud '
         'taldrik: seal on staatus ja sisu, aga kaas on veel peal.'],
        ['const andmed: Arvustus[] =\n  await vastus.json();', 'Võtab kaane pealt: vastus.json() loeb JSON-vastuse '
         'JavaScripti väärtuseks. Ka see võtab aega, sellepärast teine await.'],
        ['setArvustused(andmed);', 'Kirjutab andmed tahvlile. React joonistab lehe uuesti ja arvustused on ekraanil.'],
    ]),
    Spacer(1, 6),
    p('Kirje ' + c(': Arvustus[]') + ' aitab TypeScriptil koodi kontrollida, kuid ei kontrolli serveri vastuse tegelikku '
      'sisu.'),
    proovi('4', 'Mis juhtub, kui kirjutad ' + c("const vastus = fetch('/api/arvustused');") + ' ilma sõnata await? Kas '
                + c('vastus') + ' on siis päris vastus?'),

    p('useEffect: tee see, kui leht avaneb', h2),
    p('Funktsioon on olemas, aga keegi pole seda veel välja kutsunud. Millal seda teha? Kohe, kui leht avaneb. Selleks on '
      + c('useEffect') + ':'),
    code("""
useEffect(() => {
  laeArvustused();
}, []);
"""),
    p('Vaatame seda koodi osade kaupa. ' + c('() => { … }') + ' on <b>noolefunktsioon</b>, lühidalt kirjutatud funktsioon '
      'ilma nimeta. Selle anname Reactile ja ütleme: „käivita see pärast seda, kui leht on ekraanile joonistatud.“'),
    p('Lõpus olev ' + c('[]') + ' on <b>sõltuvuste massiiv</b>: nimekiri asjadest, mille muutumisel tuleb funktsioon '
      'uuesti käivitada. Tühja sõltuvuste massiiviga ' + c('[]') + ' käivitub efekt komponendi lisamisel lehele, mitte '
      'iga joonistamise järel.'),
    p('Miks ei võiks ' + c('laeArvustused()') + ' lihtsalt komponenti kirjutada, ilma ' + c('useEffect') + '-ita? Sest iga '
      'kord, kui olek muutub, käivitab React kogu komponendi funktsiooni uuesti. Tekiks ring: lae andmed, kirjuta '
      'tahvlile, joonista uuesti, lae andmed… Serverile läheks päringuid lõputult.'),
    note('<b>Ära ehmata:</b> meie projektis on failis ' + c('src/main.tsx') + ' sisse lülitatud <b>StrictMode</b>, Reacti '
         'arendusaegne kontrollrežiim. Selle tõttu toimub arenduse ajal alguses täiendav käivitus. Kui vaatad F12 all '
         'vahekaarti Network, näed kahte päringut. See on normaalne.'),

    p('Mis juhtub, kui midagi läheb valesti?', h2),
    p('Server võib olla kinni. Siis peab kasutaja nägema selget teadet, mitte tühja lehte. Vea püüdmiseks on '
      + c('try') + ' ja ' + c('catch') + ': „proovi seda; kui läks valesti, tee hoopis toda.“'),
    p('Üks meeldetuletus enne koodi: ' + c('true') + ' tähendab „tõene“ ja ' + c('false') + ' „väär“. Hüüumärk ' + c('!')
      + ' pöörab selle ümber, ' + c('!true') + ' on ' + c('false') + '.'),
    code(LAE_8[:LAE_8.index('  useEffect')].rstrip()),
    explain([
        ['try { … } catch { … }', 'Kui try sees tekib viga, hüppab programm kohe catch-i.'],
        ['if (!vastus.ok) {', 'vastus.ok on true, kui server vastas õnnestunult (staatus 200–299). !vastus.ok tähendab: '
                              'kui ei läinud hästi.'],
        ["throw new Error('Server vastas\n  veaga');", 'Tekitab ise vea, nii et programm hüppab catch-i. fetch ei pea '
         'veakoodiga vastust veaks, nii et peame ise kontrollima.'],
        ['setViga(...)', 'Paneb veateksti olekusse, et seda näidata.'],
        ['setLaeb(false);', 'Laadimine sai läbi, ükskõik kas õnnestus või mitte. Sellepärast on see rida väljaspool try-d.'],
    ]),
    Spacer(1, 6),
    p('Ekraanil näitame teateid nii:'),
    code("""
{laeb && <p className="kokku">Laen arvustusi…</p>}
{viga && <p className="kokku">{viga}</p>}
"""),
    p(c('&&') + ' tähendab JSX-is: kui vasak pool on tõene, näita paremat poolt. Tühi tekst ' + c("''") + ' loetakse '
      'vääraks, nii et kui viga pole, ei näidata midagi.'),
    proovi('5', 'Kui ' + c('laeb') + ' on ' + c('false') + ' ja ' + c('viga') + ' on ' + c("''") + ', mis teade ekraanil '
                'on?'),

    p('Kogu lugu järjest', h2),
    *numbered([
        'Avad lehe. Vite annab brauserile Reacti koodi.',
        'React käivitab App-i. ' + c('arvustused') + ' on tühi ja ' + c('laeb') + ' on tõene, ekraanil on „Laen '
        'arvustusi…“.',
        c('useEffect') + ' käivitab ' + c('laeArvustused') + '.',
        c('fetch') + ' saadab päringu Vite’ile, Vite saadab selle edasi pordile 3000.',
        'Express leiab marsruudi ja vastab JSON-iga. <b>Marsruut</b> on reegel „sellele aadressile vasta nii“.',
        c('setArvustused') + ' kirjutab andmed tahvlile ja ' + c('setLaeb(false)') + ' lõpetab laadimise.',
        'React joonistab uuesti. Arvustused on ekraanil.',
    ]),

    p('Kui midagi ei tööta', h2),
    table(['Mida näed', 'Võimalik põhjus', 'Mida kontrollida'], [
        ['„Arvustusi ei saanud kätte…“', 'Server ei tööta, aadress on vale või vahendusserver pole seadistatud.',
         'Serveri terminal, Vite’i terminal, F12 all Network: mis staatus päringul on. Fail ' + c('vite.config.ts') + '.'],
        ['Punane CORS-i viga konsoolis', 'fetch-is on täielik aadress koos pordiga.', 'Kas fetch-is on ainult '
         + c('/api/arvustused') + '.'],
        ['Konsoolis tuhandeid päringuid', c('[]') + ' on puudu või ' + c('laeArvustused()') + ' on väljaspool '
         + c('useEffect') + '-i.', c('useEffect') + '-i viimane rida.'],
        [c('map is not a function'), 'Olekus ei ole massiiv, näiteks puudub ' + c('await vastus.json()') + ' või server '
         'saatis muud andmed.', 'Teine ' + c('await') + ' ja F12 all Network → Response.'],
        [c('Cannot find module ... andmed'), 'Fail on kustutatud, aga import on alles.', 'Kas App-is on veel rida '
         + c("import { naidisArvustused } ...") + '.'],
    ], [WIDTH * 0.30, WIDTH * 0.36, WIDTH * 0.34]),

    p('Sõnastik', h2),
    table(['Sõna', 'Tähendus'], [
        ['<b>klient</b>', 'programm, mis saadab päringuid; meil brauser ja Reacti leht'],
        ['<b>server</b>', 'programm, mis ootab päringuid ja vastab neile'],
        ['<b>päring, vastus</b>', 'küsimus ja see, mis selle peale tagasi tuleb'],
        ['<b>marsruut</b>', 'serveri reegel: sellele aadressile vasta nii'],
        ['<b>JSON</b>', 'kokkulepe, kuidas andmeid tekstina kirjutada'],
        ['<b>port</b>', 'number, mis ütleb, millisele programmile arvutis päring läheb'],
        ['<b>localhost</b>', 'seesama arvuti'],
        ['<b>päritolu</b>', 'protokoll, hostinimi ja port kokku'],
        ['<b>CORS</b>', 'reeglid, millega server saab lubada brauseril lugeda teise päritoluga vastuseid'],
        ['<b>proxy, vahendusserver</b>', 'programm, mis saadab päringud edasi; meil Vite'],
        ['<b>olek</b> (state)', 'Reacti mälu; selle muutmisel joonistatakse leht uuesti'],
        ['<b>useEffect</b>', 'Reacti käsk: tee see pärast joonistamist'],
        ['<b>Promise</b>', 'lubadus tulevase tulemuse kohta'],
        ['<b>await, async</b>', '„kasuta tulemust, kui see on kohal“; ja funktsioon, kus nii tohib teha'],
        ['<b>try, catch</b>', 'proovi; kui läks valesti, tee hoopis nii'],
    ], [WIDTH * 0.25, WIDTH * 0.75]),

    CondPageBreak(170),
    p('„Proovi ise“ vastused', h2),
    *numbered([
        'Massiiv, sest ümber on nurksulud. Selles on kolm elementi.',
        'Express, sest port on 3000.',
        c('/api/menyy') + ' peale vastab Express, sest aadress algab ' + c('/api') + '-ga. ' + c('/favicon.svg')
        + ' peale vastab Vite ise.',
        'Ei. Ilma await-ita on ' + c('vastus') + ' alles Promise ehk lubadus, et vastus kunagi tuleb.',
        'Ei ühtegi. Mõlemad on väärad.',
    ]),
]

# ---------------------------------------------------------------- 8. tund: tunnijuhend

juhend_8 = [
    p('Tunnijuhend: React räägib serveriga', title),
    subtitle('8. tund', 'tunnis'),
    p('Täna võtad söökla rakendusest näidisandmed ära ja leht hakkab arvustusi serverilt küsima.'),
    note('<b>Vaja läheb:</b> Node.js, npm, VS Code ja söökla projekt või kursuse lehelt algfailid.<br/><br/>'
         '<b>Kuidas töötada:</b> ennusta, mis juhtub → kirjuta kood → käivita → selgita, mis muutus. Kirjuta kood ise, nii '
         'märkad, mis mida teeb. Vigade otsimiseks on kaks kohta: brauseri vead on konsoolis (' + c('F12')
         + '), serveri vead on selle terminalis.<br/><br/>'
         '<b>Miinimum:</b> sammud 0–4, leht näitab serverist tulnud arvustusi. Sammud 5–8 teevad rakenduse töökindlaks.'),

    p('Samm 0: projekt lahti', h2),
    p('Ava söökla projekt VS Code’is: File → Open Folder ja vali kaust, kus on failid ' + c('package.json') + ' ja '
      + c('vite.config.ts') + '. Seda kausta nimetame edaspidi <b>projekti peakaustaks</b>. <b>Kui sul projekti pole</b> '
      'või see ei tööta, laadi kursuse lehelt alla algfailid ' + c('tunnitoo-react-server.zip') + ', paki lahti, ava kaust '
      + c('sookla') + ' ja tee terminalis:'),
    code("""
npm install
cd server
npm install
cd ..
"""),
    p(c('npm install') + ' paigaldab paketid, mida projekt vajab. Seda on vaja teha kaks korda, sest lehel ja serveril on '
      'kummalgi oma ' + c('package.json') + '. ' + c('cd') + ' tähendab „mine kausta“ ja ' + c('cd ..') + ' „mine üks '
      'kaust ülespoole“.'),

    p('Samm 1: pane server tööle', h2),
    p('Ava terminal (Terminal → New Terminal). Käsk ' + c('pwd') + ' näitab, mis kaustas oled: see peab olema projekti '
      'peakaust. Siis kirjuta:'),
    code("""
cd server
node index.js
"""),
    see('terminalis ' + c('Server töötab: http://localhost:3000') + ' ja uut käsurida ei tule. See on õige, server ootab. '
        'Ava brauseris ' + c('http://localhost:3000/api/arvustused') + ': seal on kolm arvustust JSON-ina.'),
    stuck(c('Cannot find module') + ' tähendab, et sa pole kaustas ' + c('server') + ', fail ' + c('index.js')
          + ' puudub või paketid on paigaldamata. Kontrolli ' + c('pwd') + '-ga kausta ja ' + c('ls')
          + '-iga faile. ' + c('EADDRINUSE') + ' tähendab, et port 3000 on juba mõne teise programmi käes. See võib olla '
          'sama server teises terminalis.'),

    p('Samm 2: pane leht tööle teises terminalis', h2),
    p('Server hõivab oma terminali, nii et vaja on teist. Vajuta terminali paneelis nuppu <b>+</b>. Kontrolli ' + c('pwd')
      + '-ga, et oled projekti peakaustas. Kui ei ole, mine sinna ' + c('cd') + '-ga. Kirjuta:'),
    code("""
npm run dev
"""),
    see('terminalis aadress, tavaliselt ' + c('http://localhost:5173/') + '. Ava see aadress, mille Vite <b>kirjutas</b>: '
        'seal on sinu söökla leht, nagu enne. Nüüd töötab korraga kaks programmi. Terminalide vahel saad paneeli paremas '
        'servas liikuda.'),
    stuck('kui ' + c('npm run dev') + ' annab vea ' + c('Missing script') + ', oled kaustas ' + c('server')
          + '. Mine ' + c('cd ..') + '-ga tagasi.'),

    p('Samm 3: vahendusserver', h2),
    p('Nüüd õpetame Vite’ile, et kõik ' + c('/api') + '-ga algavad päringud lähevad edasi serverile. Ava projekti '
      'peakaustas fail ' + c('vite.config.ts') + '. Lisa seadistusobjektis omaduse ' + c('plugins') + ' järele omadus '
      + c('server') + ', nagu järgmises näites.'),
    code(VITE_CONFIG.strip('\n'), 'vite.config.ts'),
    explain([
        ['server: {', 'Vite’i arendusserveri seaded.'],
        ['proxy: {', 'Vahendusserveri seaded: millised päringud edasi saata.'],
        ["'/api': 'http://localhost:3000',", 'Kui aadress algab /api-ga, saada edasi Expressile pordil 3000.'],
    ]),
    Spacer(1, 6),
    p('<b>Mis sinu arvates juhtub</b>, kui avad pärast salvestamist Vite’i pordil aadressi ' + c('/api/arvustused')
      + '? Salvesta. Vite märkab muutust ja käivitub ise uuesti.'),
    see('ava ' + c('http://localhost:5173/api/arvustused') + '. Ometi on see Vite’i port ja näed serveri arvustusi! '
        'Vahendusserver töötab.'),
    stuck('lehekülg on tühi või näed Reacti lehte: kontrolli sulge ja koma failis ' + c('vite.config.ts')
          + ' ning käivita Vite uuesti (' + c('Ctrl+C') + ', siis ' + c('npm run dev') + '). Veateate korral vaata, kas '
          'server töötab ja mida Vite’i terminal ütleb.'),

    p('Samm 4: küsi arvustused serverilt', h2),
    p('Ava ' + c('src/App.tsx') + '. Teeme kolm muudatust.'),
    p('<b>Esiteks</b> muuda faili ülaosas importe: lisa ' + c('useEffect') + ' ja kustuta impordirida, millega tuuakse '
      'sisse ' + c('naidisArvustused') + '.'),
    code("""
import { useEffect, useState } from 'react';
"""),
    p('<b>Teiseks</b> muuda esimest ' + c('useState') + '-rida, nii et alguses oleks nimekiri tühi:'),
    code("""
const [arvustused, setArvustused] = useState<Arvustus[]>([]);
"""),
    p('<b>Kolmandaks</b> lisa kohe viimase ' + c('useState') + '-rea järele see kood:'),
    code("""
  async function laeArvustused() {
    const vastus = await fetch('/api/arvustused');
    const andmed: Arvustus[] = await vastus.json();
    setArvustused(andmed);
  }

  useEffect(() => {
    laeArvustused();
  }, []);
"""),
    explain([
        ['async function laeArvustused() {', 'Funktsioon, mis toob andmed. async lubab kasutada await-i.'],
        ["await fetch('/api/arvustused')", 'Saadab päringu ja kasutab tulemust, kui see on kohal. Aadress algab /api-ga, '
                                            'nii et Vite saadab selle serverile.'],
        ['await vastus.json()', 'Loeb JSON-vastuse JavaScripti massiiviks.'],
        ['setArvustused(andmed);', 'Kirjutab massiivi olekusse. React joonistab lehe uuesti.'],
        ['useEffect(() => {', 'Käivita see funktsioon pärast seda, kui leht on joonistatud.'],
        ['}, []);', 'Tühi sõltuvuste massiiv: mitte iga joonistamise järel.'],
    ]),
    Spacer(1, 6),
    p('Salvesta ja kustuta fail ' + c('src/andmed.ts') + ' (paremklõps failil → Delete). Seda pole enam vaja.'),
    see('lehel on endiselt kolm arvustust, aga nüüd tulevad need serverist. Kontrolli: muuda failis '
        + c('server/index.js') + ' ühe arvustuse kommentaari, salvesta, pane server ' + c('Ctrl+C') + '-ga kinni, '
        'käivita uuesti ' + c('node index.js') + ' ja värskenda lehte (' + c('F5') + '). Uus tekst on lehel. '
        '<b>Miks?</b> Selgita pinginaabrile.'),
    stuck('tühi leht: vaata konsooli (' + c('F12') + '). Tabel levinud vigadega on konspekti lõpus.'),
    note('<b>Vaata ise, kuidas päring käib.</b> Vajuta ' + c('F12') + ', vali vahekaart <b>Network</b> ja värskenda lehte. '
         'Otsi rida ' + c('arvustused') + ' ja klõpsa sellel. Vahekaardil <b>Response</b> on täpselt see, mille server '
         'saatis. Ridu on kaks, sest projektis on sisse lülitatud StrictMode, mis arenduse ajal käivitab efekti alguses '
         'kaks korda.'),

    p('Samm 5: laadimine ja vead', h2),
    p('Nüüd tuleb kasutajale öelda, mis toimub. Lisa teiste ' + c('useState') + '-ridade juurde kaks uut:'),
    code("""
const [laeb, setLaeb] = useState(true);
const [viga, setViga] = useState('');
"""),
    p(c('laeb') + ' on ' + c('true') + ' ehk tõene, kuni andmed pole veel kohal. ' + c('viga') + ' on alguses tühi tekst. '
      'Muuda funktsioon ' + c('laeArvustused') + ' selliseks:'),
    code(LAE_8[:LAE_8.index('  useEffect')].rstrip()),
    explain([
        ['try {', 'Proovi teha seda, mis on järgnevates sulgudes.'],
        ['if (!vastus.ok) {', 'Kui server ei vastanud õnnestunult. ! tähendab „ei“.'],
        ["throw new Error('Server vastas\n  veaga');", 'Tekita viga: programm hüppab kohe catch-i.'],
        ['} catch {', 'Siia jõuab programm, kui try sees läks midagi valesti.'],
        ["setViga('Arvustusi ei saanud...');", 'Kirjutab veateksti olekusse.'],
        ['setLaeb(false);', 'Laadimine on läbi, hoolimata tulemusest.'],
    ]),
    Spacer(1, 6),
    p('Lõpuks näita teateid. Pane need JSX-is kohe rea ' + c('</form>') + ' järele:'),
    code("""
{laeb && <p className="kokku">Laen arvustusi…</p>}
{viga && <p className="kokku">{viga}</p>}
"""),
    see('leht töötab nagu enne. „Laen arvustusi…“ on nii lühidalt, et sa ei pruugi seda märgatagi.'),

    p('Samm 6: tee meelega katki', h2),
    p('<b>Mis sinu arvates juhtub</b>, kui server on kinni ja värskendad lehte? Mine serveri terminali, vajuta '
      + c('Ctrl+C') + ' ja värskenda lehte (' + c('F5') + ').'),
    see('arvustusi pole ja lehel on teade „Arvustusi ei saanud kätte. Kas server töötab?“. Täpselt nii peabki olema! Vaata '
        'ka Vite’i terminali ja F12 all vahekaarti Network: mis veateade ja staatus seal on? <b>Miks see juhtus?</b>'),
    p('Käivita server uuesti (' + c('node index.js') + ') ja värskenda lehte. Arvustused on tagasi.'),

    p('Samm 7: mida server veel ei oska', h2),
    p('Lisa lehel vormiga uus arvustus. See ilmub nimekirja. <b>Mis sinu arvates juhtub</b>, kui vajutad ' + c('F5')
      + '? Vajuta.'),
    see('sinu arvustus on kadunud, algsed kolm on alles. Vormi kood lisab arvustuse ainult sinu brauseri mällu ja server '
        'ei kuulnud sellest midagi. Järgmises tunnis õpetame serveri arvustusi vastu võtma.'),

    p('Samm 8: salvesta Gitti', h2),
    p('Git on programm, mis hoiab alles koodi ajalugu. Mine terminali, kus ükski server ei tööta. Vajadusel vajuta '
      'jälle <b>+</b>. Kontrolli, et oled projekti peakaustas, ja tee:'),
    code("""
git add .
git commit -m "React küsib arvustused serverilt"
"""),
    p(c('git add .') + ' valib kõik muudatused ja ' + c('git commit') + ' salvestab need koos sõnumiga. Kaks võimalikku '
      'takistust: ZIP-failist võetud projektil pole Giti ajalugu, nii et kui Git ütleb ' + c('not a git repository')
      + ', tee enne seda üks kord ' + c('git init') + '. Kui Git küsib nime ja e-posti, täida need käskudega:'),
    code("""
git config --global user.name "Sinu Nimi"
git config --global user.email "sinu@naide.ee"
"""),

    p('Kogu fail', h2),
    p('Kui midagi ei tööta, võrdle oma faili sellega ja otsi, kus on erinevus.'),
    *code_file(APP_8, 'src/App.tsx'),

    CondPageBreak(120),
    p('Kui jõuad varem valmis', h2),
    p('Need on valikulised väljakutsed. Koodi pole, ainult vihjed.'),
    *bullets(
        '<b>Menüü lehel.</b> Küsi serverilt ka ' + c('/api/menyy') + ' ja näita toite nimekirjana. Vihje: uus '
        + c('useState') + ', teine funktsioon ja sama ' + c('useEffect') + '.',
        '<b>Mitu arvustust?</b> Näita nimekirja kohal, mitu arvustust on. Vihje: ' + c('arvustused.length')
        + ' ja klass ' + c('kokku') + '.',
        '<b>Värskenda-nupp.</b> Nupp, mis küsib andmed uuesti. Vihje: nupp vajab funktsiooni, mis enne küsimist teeb '
        + c("setViga('')") + ' ja ' + c('setLaeb(true)') + ', muidu jääb vana veateade alles.',
    ),
    Spacer(1, 6),
    note('<b>Hoia projekt alles!</b> Järgmises tunnis õpib server arvustusi lisama ja kustutama.'),
]

# ---------------------------------------------------------------- 8. tund: kodutöö

JRK_8 = ['A) ' + 'setArvustused kirjutab andmed olekusse', 'B) Express vastab JSON-iga',
         'C) React joonistab lehe esimest korda, nimekiri on tühi', 'D) Vite saadab päringu pordile 3000',
         'E) React joonistab lehe uuesti koos arvustustega', 'F) useEffect käivitab funktsiooni laeArvustused',
         'G) fetch saadab päringu Vite’ile']

kodutoo_8 = [
    p('Kodutöö: React ja server', title),
    subtitle('8. tund', 'kodutöö'),
    row([p('Nimi', label_b), Field('nimi', 220), '', p('Kuupäev', label_b), Field('kuupaev', 110), ''],
        [51, 220, 18, 51, 110, WIDTH + 12 - 450], PALE),
    Spacer(1, 8),
    p('Midagi paigaldama ei pea, piisab brauserist. Vastused leiad konspektist. Ava see fail kursuse lehel nupuga „Vaata“, '
      'täida lahtrid, vajuta „Laadi täidetud PDF alla“ ja saada fail aadressile <b>mtsopo@taltech.ee</b> hiljemalt 09.11 '
      'kell 23.59.', intro),

    p('1. Oma sõnadega', h2),
    p('Selgita ühe lausega.'),
]
for name, word in [('s_port', 'port'), ('s_proxy', 'vahendusserver'), ('s_state', 'olek'), ('s_await', 'await'),
                   ('s_effect', 'useEffect')]:
    kodutoo_8.append(row([p(word, label), Field(name, WIDTH - 90)], [90, WIDTH - 90]))
kodutoo_8 += [
    p('2. Milliseid porte kasutame selles projektis?', h2),
    row([p('Vite', label), Field('port_vite', 70), '', p('Express', label), Field('port_server', 70)],
        [50, 70, 30, 60, 70]),
    Spacer(1, 6),
    CondPageBreak(200),
    p('3. Pane järjekorda', h2),
    p('Avad lehe. Mis juhtub? Kirjuta lahtritesse tähed õiges järjekorras, igasse lahtrisse üks täht.'),
    *[p(item, label) for item in JRK_8],
    Spacer(1, 6),
    row([x for i in range(7) for x in (p(f'{i + 1}.', label), Field(f'jrk_{i}', 30), '')], [16, 30, 10] * 7),
    Spacer(1, 6),

    CondPageBreak(240),
    p('4. Loe koodi', h2),
    code("""
const [laeb, setLaeb] = useState(true);

async function laeArvustused() {
  try {
    const vastus = await fetch('/api/arvustused');
    if (!vastus.ok) {
      throw new Error('Viga');
    }
  } catch {
    setViga('Arvustusi ei saanud kätte.');
  }
}
"""),
    row([p('Mis väärtus on ' + c('laeb') + ' alguses?', label), Field('kood_laeb', 80)], [300, 80]),
    row([p('Server vastas staatusega 200. Mis on ' + c('vastus.ok') + ' (true või false)?', label), Field('kood_ok200', 80)],
        [300, 80]),
    row([p('Server vastas staatusega 404. Mis on ' + c('vastus.ok') + '?', label), Field('kood_ok404', 80)], [300, 80]),
    row([p('Kas 404 korral jõuab programm ' + c('catch') + '-i (jah või ei)?', label), Field('kood_catch', 80)], [300, 80]),
    Spacer(1, 6),

    CondPageBreak(150),
    p('5. Leia viga', h2),
    question('<b>a)</b> Serverile läheb lõputult päringuid. Mis on valesti ja kuidas parandada?', 'viga_a', 40, extra=code_parts("""
useEffect(() => {
  laeArvustused();
});
""")),
    question('<b>b)</b> Konsoolis on CORS-i veateade. Mis on valesti ja kuidas parandada?', 'viga_b', 40, extra=code_parts("""
const vastus = await fetch('http://localhost:3000/api/arvustused');
""")),
    question('<b>c)</b> VS Code joonib viimase rea punaseks, sest ' + c('vastus') + ' ei ole arvustuste massiiv. Mis ' + c('vastus')
             + ' tegelikult on ja mida tuleb enne teha, et arvustused kätte saada?', 'viga_c', 40, extra=code_parts("""
const vastus = await fetch('/api/arvustused');
setArvustused(vastus);
""")),

    CondPageBreak(160),
    p('6. Mõtle', h2),
    question('<b>a)</b> Lehel on teade „Arvustusi ei saanud kätte“. Mida sa kontrolliksid esimesena ja kus?', 'mote_a', 40),
    question('<b>b)</b> Pärast 8. tunni muudatusi lisad vormiga arvustuse ja vajutad ' + c('F5')
             + '. Arvustus on kadunud. Miks? Mida oleks vaja teha, et see alles jääks?', 'mote_b', 48),
    question('<b>c) Lisaülesanne.</b> Miks ei tohi kirjutada ' + c('laeArvustused()') + ' otse komponenti, ilma '
             + c('useEffect') + '-ita?', 'mote_c', 48),
]

# ---------------------------------------------------------------- 9. tund: konspekt

konspekt_9 = [
    p('Arvustuste lisamine ja kustutamine', title),
    subtitle('9. tund', 'konspekt'),
    note('Ka siin selgitan kõik mõisted uuesti, kordamine on meelega. Koodi käivitamiseks on vaja Node.js-i, npm-i, VS Code’i '
         'ja söökla projekti, mille saad ka kursuse lehelt alla laadida. Lahenda „Proovi ise“ kastid, vastused on lõpus. '
         'Veebilehel on <b>Päringulabor</b>, serveri simulatsioon, mis töötab brauseris ja kus saad päringuid proovida '
         'ilma midagi paigaldamata.<br/><br/>'
         '<b>Pärast seda tundi oskad:</b><br/>'
         '• valida õige meetodi: GET, POST või DELETE;<br/>'
         '• kirjutada serverile marsruudid, mis lisavad ja kustutavad;<br/>'
         '• saata Reactist päringu koos andmetega ja lugeda staatusekoodi.<br/><br/>'
         'Kõige tähtsam on kontrollitud arvustuse lisamine. Kustutamine on järgmine etapp. Läbivalt võrdleme kõike '
         'restoraniga.'),

    p('Probleem', h2),
    p('Praegu saab meie rakendus andmeid ainult lugeda. Pärast lehe värskendamist kaovad brauseris lisatud arvustused. '
      'Serverist saadud algsed arvustused jäävad alles. Miks? Sest uus arvustus jõudis ainult sinu brauseri mällu ja '
      'server ei kuulnud sellest midagi.'),
    p('Täna paneme lehe serverile rääkima: „võta see arvustus vastu“ ja „kustuta see ära“.'),

    p('Kes on kes', h2),
    table(['Restoranis', 'Veebis', 'Mis see on'], [
        ['Sina laua taga', '<b>klient</b>', 'Programm, mis saadab päringuid: brauser ja Reacti leht.'],
        ['Tellimus', '<b>päring</b>', 'Mida klient serverilt tahab.'],
        ['Köök', '<b>server</b>', 'Programm, mis ootab päringuid ja vastab. Meil Express.'],
        ['See, mis lauale tuuakse', '<b>vastus</b>', 'Mille server tagasi saadab.'],
    ], [WIDTH * 0.32, WIDTH * 0.14, WIDTH * 0.54]),
    Spacer(1, 6),
    p('Meil töötab korraga kaks programmi, kumbki oma terminalis. <b>Vite</b> (' + c('npm run dev') + ', tavaliselt port '
      '5173) annab brauserile lehe. <b>Express</b> (' + c('node index.js') + ' kaustas ' + c('server') + ', port 3000) '
      'hoiab arvustusi. <b>Port</b> on number, mis ütleb, millisele programmile arvutis päring läheb. Leht küsib '
      'aadressilt ' + c('/api/...') + ' ja Vite saadab päringu serverile edasi nagu teenindaja, kes viib tellimuse kööki.'),

    p('Meetod: mida sa tahad teha?', h2),
    p('Restoranis võid menüüd vaadata, tellida või tellimuse tühistada. Päringul on samuti lisaks aadressile <b>meetod</b>, '
      'mis ütleb, mida teha. Sama aadress, eri meetod: eri tegevus.'),
    figure(methods_drawing(), 'Sinine on meetod, siis aadress, tähendus ja mida server vastab.'),
    table(['Meetod', 'Tähendus', 'Restoranis'], [
        [c('GET'), 'loe, ära muuda midagi', 'Vaatad menüüd'],
        [c('POST'), 'lisa midagi uut', 'Annad tellimuse'],
        [c('DELETE'), 'kustuta', 'Tühistad tellimuse'],
    ], [WIDTH * 0.18, WIDTH * 0.42, WIDTH * 0.40]),
    Spacer(1, 6),
    p('Aadressiribalt saad selles näites teha ' + c('GET') + '-päringu. ' + c('POST') + '-päringu proovimiseks kasutame '
      + c('fetch()') + '-i või Päringulaborit.'),
    proovi('1', 'Mis meetodit kasutaksid: (a) tahad näha kõiki arvustusi, (b) tahad arvustuse number 3 ära võtta, (c) '
                'tahad uue arvustuse lisada?'),

    p('Staatusekood: kuidas läks?', h2),
    p('Server vastab alati ka kolmekohalise numbriga, <b>staatusekoodiga</b>. Sa oled ühte juba näinud: 404 ehk „ei '
      'leitud“. Esimene number näitab vastuse üldist liiki:'),
    table(['Kood', 'Tähendus', 'Millal meie server seda kasutab'], [
        ['<b>200</b>', 'OK, kõik läks hästi', 'Arvustused anti välja või arvustus kustutati'],
        ['<b>201</b>', 'Loodud', 'Uus arvustus lisati'],
        ['<b>400</b>', 'Halb päring: päringus on midagi valesti', 'Toit on puudu või hinne on 9'],
        ['<b>404</b>', 'Ei leitud', 'Sellise numbriga arvustust pole'],
        ['<b>500</b>', 'Serveri ootamatu viga', 'Seda ei tee me meelega'],
    ], [WIDTH * 0.1, WIDTH * 0.45, WIDTH * 0.45]),
    Spacer(1, 6),
    p('Rusikareegel: 2-ga algavad tähendavad õnnestumist, 4-ga algavad probleemi päringuga ja 5-ga algavad ootamatut viga '
      'serveris.'),
    proovi('2', 'Saadad arvustuse, mille hinne on 9. Millise staatusekoodiga peaks server vastama? Miks?'),

    p('Serveri pool: express.json ja req.body', h2),
    p('Serveri failis ' + c('server/index.js') + ' on <b>marsruudid</b>. Marsruut on reegel: „kui tuleb selline päring, '
      'tee nii“. Seni oli meil ainult ' + c('app.get') + '. Lisamiseks on ' + c('app.post') + ':'),
    code("""
app.post('/api/arvustused', (req, res) => {
  // siia tuleb kood
});
"""),
    p('Funktsioon saab kaks asja. ' + c('req') + ' (ingl <i>request</i>) on päring: kõik, mida klient saatis. ' + c('res')
      + ' (<i>response</i>) on vastus: selle kaudu saadame midagi tagasi. Märk ' + c('=>') + ' teeb <b>noolefunktsiooni</b>, '
      'see on lühidalt kirjutatud funktsioon.'),
    p('Klient saadab uue arvustuse <b>päringu kehas</b> (ingl <i>body</i>), meil JSON-tekstina. Aadress ja meetod ütlevad, '
      'mida teha, keha on tellimuse sisu. JSON-keha parsimiseks ehk JavaScripti väärtuseks lugemiseks on see rida, mis '
      'peab olema pärast ' + c('app') + '-i loomist ja enne marsruute:'),
    code("""
app.use(express.json());
"""),
    p('Nüüd saad andmeid lugeda kujul ' + c('req.body') + '. Kui JSON-keha pole parsitud, võib ' + c('req.body') + ' olla '
      + c('undefined') + ' ehk väärtus puudub. Meie praegune kood annaks selle lahtivõtmisel vea.'),
    code("""
const { toit, hinne, kommentaar } = req.body;
"""),
    p('Seda kirjutusviisi nimetatakse lahtivõtmiseks. See on lihtsalt lühem kuju kolmest reast: ' + c('const toit = req.body.toit;')
      + ' ja sama teistega.'),

    p('Ära usalda kedagi: kontrolli andmeid', h2),
    p('Vormis on hinne valikmenüüs 1 kuni 5, kas pole siis kõik korras? Ei ole. Päringut saab saata ka ilma sinu vormita '
      'ja brauseris saab koodi muuta. Seepärast peab server ise kontrollima.'),
    p('Mõned märgid enne koodi: ' + c('===') + ' tähendab „on täpselt võrdne“, ' + c('!==') + ' „ei ole võrdne“, ' + c('&&')
      + ' „ja“, ' + c('||') + ' „või“ ning ' + c('!') + ' „ei“. ' + c('true') + ' on tõene ja ' + c('false') + ' väär.'),
    code(CHECK_9),
    explain([
        ["typeof toit === 'string'", 'toit peab olema tekst.'],
        ["toit.trim() !== ''", 'trim() eemaldab tühikud algusest ja lõpust. Alles peab jääma midagi.'],
        ['Number.isInteger(hinne)', 'hinne peab olema täisarv. Tekst "5" ei sobi.'],
        ['hinne >= 1 && hinne <= 5', 'hinne on lubatud vahemikus.'],
        ['if (!toitOnKorras || ...', 'Kui vähemalt üks tingimus pole täidetud.'],
        ['res.status(400)', 'Määrab staatusekoodi.'],
        [".json({ viga: '...' })", 'Saadab veateate JSON-ina.'],
        ['return;', 'Lõpetab funktsiooni kohe, nii et arvustust ei lisata. Ilma selleta läheks kood edasi.'],
    ]),

    p('Uue arvustuse tegemine', h2),
    code(NEW_9),
    explain([
        ['id: jargmineId', 'Igal arvustusel peab olema oma number. Numbri paneb server.'],
        ['toit: toit.trim()', 'Salvestame teksti ilma üleliigsete tühikuteta.'],
        ['jargmineId = jargmineId + 1;', 'Järgmine saab ühe võrra suurema numbri.'],
        ['[uus, ...arvustused]', 'Uus massiiv: ees on uus. Kolm punkti koodis laotavad vanad elemendid selle järele.'],
        ['res.status(201).json(uus);', 'Vastab koodiga 201 ja saadab uue arvustuse koos numbriga tagasi.'],
    ]),
    Spacer(1, 6),
    p('Selleks, et muutujatele ' + c('arvustused') + ' ja ' + c('jargmineId') + ' saaks anda uue väärtuse, peavad need '
      'olema kirjutatud sõnaga ' + c('let') + ', mitte ' + c('const') + '.'),

    p('Kustutamine ja aadressi sees olev number', h2),
    p('Kuidas öelda, millist arvustust kustutada? Number pannakse aadressi: ' + c('/api/arvustused/2') + '. Marsruudis '
      'tähistab seda koht, mis algab kooloniga. ' + c('.find()') + ' otsib massiivist esimese sobiva elemendi. '
      + c('.filter()') + ' teeb uue massiivi nendest, mis tingimusele vastavad.'),
    code(DELETE_9),
    explain([
        ["'/api/arvustused/:id'", ':id tähendab „siia võib tulla mis tahes väärtus, nimetame seda id“.'],
        ['req.params.id', 'See väärtus. Aadressil /api/arvustused/2 on see tekst "2", sest aadress on alati tekst.'],
        ['Number(...)', 'Teeb tekstist "2" arvu 2.'],
        ['.find((a) => a.id === id)', 'Kui ei leia, annab undefined.'],
        ['if (!leitud) {', 'Kui sellist polnud, vasta 404.'],
        ['.filter((a) => a.id !== id)', 'Jätab alles kõik, mille id ei ole see. Nii jääb kustutatav välja.'],
    ]),
    Spacer(1, 6),
    proovi('3', 'Massiivis on id-d 1, 2 ja 3. Saabub ' + c('DELETE /api/arvustused/7') + '. Millise staatusekoodi saad? Mis '
                'juhtub massiiviga?'),

    p('Kliendi pool: fetch koos meetodiga', h2),
    p('Seni kirjutasime ' + c("fetch('/api/arvustused')") + ' ja see tegi ' + c('GET') + '-päringu. Teistel meetoditel '
      'on vaja teist argumenti: objekt, kus on päringu seaded.'),
    code("""
const vastus = await fetch('/api/arvustused', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ toit, hinne, kommentaar }),
});
const andmed = await vastus.json();
"""),
    explain([
        ['await', 'Kasuta tulemust, kui see on kohal. Funktsiooni ette peab siis kirjutama async.'],
        ["method: 'POST',", 'Mis meetodiga saata.'],
        ["headers: { 'Content-Type':\n  'application/json' },", 'Päringu päised on lisainfo päringu kohta. See ütleb '
         'serverile: keha on JSON. Ilma selleta ei parsi express.json() keha.'],
        ['JSON.stringify({ ... })', 'Teeb objektist JSON-teksti, sest meie server ootab keha JSON-vormingus.'],
        ['vastus.json()', 'Loeb serveri JSON-vastuse JavaScripti väärtuseks.'],
    ]),
    Spacer(1, 6),
    p('Kontrollime ka tulemust. ' + c('vastus.ok') + ' on ' + c('true') + ', kui staatus on 200–299. Kui ei, näitame serveri '
      'veateadet, mis on kohas ' + c('andmed.viga') + ':'),
    code("""
if (!vastus.ok) {
  setViga(andmed.viga);
  return;
}
setArvustused((praegused) => [andmed, ...praegused]);
"""),
    p(c('useState') + ' on Reacti mälu ehk olek. Nüüd paneme nimekirja serveri vastuse, sest alles selles on õige ' + c('id')
      + '. Pane tähele, et ' + c('setArvustused') + ' saab nüüd funktsiooni. ' + c('praegused') + ' on oleku kõige värskem '
      'väärtus. See on vajalik, sest vastus võib tulla alles hiljem: kui vahepeal jõudis mõni teine päring nimekirja '
      'muuta, ei kirjutata seda muudatust üle.'),
    p('Server võib ka üldse mitte vastata. Selleks on kogu päring pandud ' + c('try') + '-plokki, nagu eelmises tunnis.'),
    p('Kustutamisel pole keha vaja, sest kõik on aadressis:'),
    code("""
const vastus = await fetch(`/api/arvustused/${id}`, { method: 'DELETE' });
"""),
    p('Langetusrõhumärgid ehk tagurpidi ülakomad ' + c('`') + ' teevad <b>malliteksti</b>: ' + c('${id}') + ' asemele '
      'pannakse muutuja väärtus.'),

    p('Kuidas nupp saab kustutada?', h2),
    p('Kustuta-nupp on komponendis ' + c('ArvustuseKaart') + ', aga nimekiri elab komponendis ' + c('App') + '. Lahendus: '
      + c('App') + ' annab kaardile funktsiooni ' + c('kustuta') + ' <b>propsina</b>. Prop on väärtus, mille komponent '
      'väljast saab, nagu funktsiooni argument. Kaart ütleb nupuvajutusel: „kutsu see välja minu numbriga“.'),
    code("""
<button type="button" onClick={() => kustuta(arvustus.id)}>Kustuta</button>
"""),
    p('Miks ' + c('() => kustuta(arvustus.id)') + ', mitte lihtsalt ' + c('kustuta(arvustus.id)') + '? Teisel juhul kutsutakse '
      'funktsioon välja juba joonistamise ajal, ilma nupuvajutuseta, ja see võib arvustusi kustutada. TypeScript võib selle '
      'vea juba enne käivitamist märgata.'),

    p('Aga miks server unustab?', h2),
    p('Pane server ' + c('Ctrl+C') + '-ga kinni ja käivita uuesti. Sinu lisatud arvustused on kadunud ja kustutatud on '
      'tagasi. Miks? Massiiv ' + c('arvustused') + ' elab programmi <b>mälus</b>, nagu tekst tahvlil. Programm kinni, tahvel '
      'puhas. Käivitamisel kirjutatakse failist uuesti need kolm esimest.'),
    p('Võrreldes varasemaga on palju paremaks läinud: arvustused jäävad alles lehe värskendamisel. Ühiseid arvustusi näevad '
      'kliendid, mis kasutavad sama serverit. Iga õpilase enda arvutis töötaval serveril on eraldi andmed.'),
    p('Andmete säilimiseks pärast serveri sulgemist tuleb need püsivalt salvestada, näiteks faili või andmebaasi. Edaspidi '
      'kasutame selleks andmebaasi.'),

    p('Kui midagi ei tööta', h2),
    table(['Mida näed', 'Võimalik põhjus', 'Mida kontrollida'], [
        ['Server ei reageeri koodimuudatusele', 'Serverit pole pärast koodi muutmist uuesti käivitatud.', c('Ctrl+C')
         + ' ja ' + c('node index.js') + '.'],
        ['Staatus 404, ' + c('Cannot POST'), 'Sellise meetodi ja aadressiga marsruuti pole.', 'Aadress ja meetod '
         'täht-tähelt.'],
        ['Staatus 500, ' + c('Cannot destructure'), c('req.body') + ' on ' + c('undefined') + '.', 'Kas '
         + c('app.use(express.json());') + ' on enne marsruute ja kas fetch-is on ' + c('headers') + '.'],
        ['Staatus 400, kuigi kõik on täidetud', 'Hinne läks tekstina või lahter on ainult tühikuid täis.', 'Vormi '
         + c('Number(e.target.value)') + ' ja F12 all Network → Payload.'],
        ['Arvustused kaovad ilma nupuvajutuseta', c('onClick={kustuta(arvustus.id)}'), 'Kas ees on ' + c('() =>') + '.'],
        ['„Serveriga ei saanud ühendust“', 'Server ei tööta või vastus pole JSON.', 'Serveri terminal ja Network.'],
    ], [WIDTH * 0.32, WIDTH * 0.35, WIDTH * 0.33]),

    p('Sõnastik', h2),
    table(['Sõna', 'Tähendus'], [
        ['<b>meetod</b>', 'mida päring teha tahab: GET, POST, DELETE'],
        ['<b>staatusekood</b>', 'kolmekohaline number vastuses, mis näitab vastuse liiki'],
        ['<b>marsruut</b>', 'serveri reegel: selle meetodi ja aadressi peale tee nii'],
        ['<b>päringu keha</b> (body)', 'päringuga kaasa saadetud andmed'],
        ['<b>päringu päis</b> (header)', 'lisainfo päringu kohta, näiteks mis kujul keha on'],
        ['<b>parsimine</b>', 'teksti lugemine andmeteks'],
        ['<b>req, res</b>', 'päring ja vastus serveri marsruudis'],
        ['<b>req.params</b>', 'aadressi muutuvad osad, näiteks :id'],
        ['<b>JSON.stringify</b>', 'teeb objektist JSON-teksti'],
        ['<b>prop</b>', 'väärtus, mille komponent väljast saab'],
        ['<b>andmebaas</b>', 'programm, mis hoiab andmeid püsivalt, nii et need jäävad alles'],
    ], [WIDTH * 0.25, WIDTH * 0.75]),

    CondPageBreak(130),
    p('„Proovi ise“ vastused', h2),
    *numbered([
        '(a) GET, (b) DELETE, (c) POST.',
        '400, sest päringus olev hinne ei ole lubatud.',
        '404. Massiiv ei muutu, sest ' + c('return') + ' lõpetab funktsiooni enne ' + c('filter') + '-it.',
    ]),
]

# ---------------------------------------------------------------- 9. tund: tunnijuhend

juhend_9 = [
    p('Tunnijuhend: lisamine ja kustutamine', title),
    subtitle('9. tund', 'tunnis'),
    p('Täna õpetad serveri arvustusi vastu võtma ja kustutama ning ühendad need lehega.'),
    note('<b>Vaja läheb:</b> Node.js, npm, VS Code ja söökla projekt või kursuse lehelt algfailid.<br/><br/>'
         '<b>Kuidas töötada:</b> ennusta, mis juhtub → kirjuta kood → käivita → selgita, mis muutus.<br/><br/>'
         '<b>Kaks reeglit.</b> Iga kord, kui muudad faili ' + c('server/index.js') + ', pane server ' + c('Ctrl+C')
         + '-ga kinni ja käivita uuesti ' + c('node index.js') + ', sest Node ei loe faili ise uuesti. Serveri vead on '
         'serveri terminalis, lehe vead on konsoolis (' + c('F12') + ').<br/><br/>'
         '<b>Miinimum:</b> sammud 0–3, kontrollitud arvustuse lisamine. Sammud 4 ja 5 on kustutamine.'),

    p('Samm 0: mõlemad serverid tööle', h2),
    p('Ava söökla projekt. <b>Kui sul projekti pole</b>, laadi alla ' + c('tunnitoo-lisamine.zip') + ', paki lahti, ava kaust '
      + c('sookla') + ' ja tee terminalis ' + c('npm install') + ', siis ' + c('cd server') + ', ' + c('npm install') + ' ja '
      + c('cd ..') + '.'),
    p('Esimeses terminalis käivita server, teises leht. Uue terminali saad nupuga <b>+</b>. Mõlema terminali alguses '
      'kontrolli ' + c('pwd') + '-ga, et oled projekti peakaustas, kus on ' + c('vite.config.ts') + '.'),
    code("""
cd server
node index.js
""", 'esimene terminal'),
    code("""
npm run dev
""", 'teine terminal'),
    see('ava aadress, mille Vite terminali kirjutas, tavaliselt ' + c('http://localhost:5173') + ': lehel on kolm '
        'arvustust.'),
    stuck('kui lehel on „Arvustusi ei saanud kätte“, kontrolli esmalt, kas server töötab. Kui ' + c('npm run dev')
          + ' annab vea, oled tõenäoliselt vales kaustas: ' + c('cd ..') + ' viib tagasi.'),

    p('Samm 1: valmista server ette', h2),
    p('Ava ' + c('server/index.js') + '. Tee kaks väikest muudatust. Esiteks lisa kohe rea ' + c('const app = express();')
      + ' järele:'),
    code("""
app.use(express.json());
"""),
    p('See parsib päringu kehas tuleva JSON-i, nii et saame seda lugeda kujul ' + c('req.body') + '. Rida peab olema enne '
      'marsruute.'),
    p('Teiseks muuda ' + c('const arvustused') + ' sõnaks ' + c('let arvustused') + ' ja lisa massiivi lõpu järele uus rida:'),
    code("""
let jargmineId = 4;
"""),
    p(c('let') + ' lubab muutujale hiljem uue väärtuse anda. ' + c('jargmineId') + ' on number, mille saab järgmine uus '
      'arvustus. Neli, sest numbrid 1–3 on juba kasutusel.'),

    p('Samm 2: POST-marsruut', h2),
    p('Lisa see kood olemasoleva ' + c("app.get('/api/arvustused', ...") + ' marsruudi järele:'),
    code(SERVER_9[SERVER_9.index("app.post("):SERVER_9.index("app.delete(")].rstrip()),
    explain([
        ["app.post('/api/arvustused',", 'See reegel kehtib POST-päringutele sellel aadressil.'],
        ['(req, res) => {', 'Funktsioon saab päringu (req) ja vastuse (res).'],
        ['const { toit, hinne, kommentaar }\n  = req.body;', 'Võtab päringu kehast kolm välja.'],
        ["typeof toit === 'string' &&\n  toit.trim() !== ''", 'toit peab olema tekst ja selles peab olema muud kui '
                                                              'tühikud. && on „ja“.'],
        ['Number.isInteger(hinne) && ...', 'hinne peab olema täisarv 1 kuni 5.'],
        ['if (!toitOnKorras || ...', '! on „ei“, || on „või“. Kui midagi pole korras.'],
        ['res.status(400).json({ viga: ... });', 'Vastab koodiga 400 ja veateatega.'],
        ['return;', 'Lõpetab funktsiooni, nii et edasi ei minda.'],
        ['const uus = { id: jargmineId, ... };', 'Teeb uue arvustuse. Numbri annab server, trim() eemaldab tühikud.'],
        ['jargmineId = jargmineId + 1;', 'Järgmine saab ühe võrra suurema numbri.'],
        ['arvustused = [uus, ...arvustused];', 'Uus massiiv: ees uus arvustus, kolm punkti laotavad vanad järele.'],
        ['res.status(201).json(uus);', 'Vastab koodiga 201 ja saadab uue arvustuse tagasi.'],
    ]),
    Spacer(1, 6),
    p('Salvesta. Serveri terminalis: ' + c('Ctrl+C') + ', siis ' + c('node index.js') + '.'),
    p('Nüüd proovi päringut ilma Reactita. Ava oma leht, vajuta ' + c('F12') + ', vali vahekaart <b>Console</b> ja kirjuta '
      'sinna:'),
    code("""
const vastus = await fetch('/api/arvustused', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ toit: 'Test', hinne: 5, kommentaar: 'Hea' }),
});
await vastus.json();
"""),
    p('<b>Mis sinu arvates tagasi tuleb?</b> Vajuta Enter.'),
    see('konsoolis objekt koos ' + c('id') + '-ga. Kui lisasid esimese arvustuse pärast serveri käivitamist, on ' + c('id')
        + ' 4. Ava ' + c('http://localhost:3000/api/arvustused') + ': test-arvustus on nimekirja alguses. Kui konsool ütleb, '
        'et kleepimine pole lubatud, kirjuta käsk ' + c('allow pasting') + ' ja proovi uuesti.'),
    stuck('500 ja ' + c('Cannot destructure') + ' terminalis tähendab, et ' + c('req.body') + ' on ' + c('undefined')
          + ': kontrolli rida ' + c('app.use(express.json());') + '. 404 tähendab sageli, et serverit pole uuesti '
          'käivitatud.'),

    p('Samm 3: pane vorm serverile saatma', h2),
    p('Ava ' + c('src/App.tsx') + ' ja asenda kogu funktsioon ' + c('lisa') + ' selle koodiga:'),
    code(LISA_9.strip('\n')),
    explain([
        ['async function lisa(e: ...) {', 'Nüüd on see async, sest kasutame sees await-i.'],
        ['e.preventDefault();', 'Muidu teeks brauser vormi saatmisel lehele värskenduse.'],
        ["setViga('');", 'Kustutab eelmise veateate.'],
        ['try {', 'Kui server ei vasta üldse, hüppab programm catch-i.'],
        ["await fetch('/api/arvustused', {", 'Teine argument on objekt päringu seadetega.'],
        ["method: 'POST',", 'Meetod.'],
        ["headers: { 'Content-Type':\n  'application/json' },", 'Päringu päis ütleb serverile, et keha on JSON.'],
        ['body: JSON.stringify({ ... }),', 'Teeb objektist teksti. toit on lühend kirjutisest toit: toit.'],
        ['const andmed = await vastus.json();', 'Loeb vastuse: uus arvustus või { viga: ... }.'],
        ['if (!vastus.ok) {', 'Kui server vastas veakoodiga.'],
        ['setViga(andmed.viga);', 'Näitab serveri veateadet. Ekraanil näitab seda eelmises tunnis lisatud rida.'],
        ['setArvustused((praegused) =>\n  [andmed, ...praegused]);', 'Paneb serveri antud arvustuse nimekirja algusesse. '
         'praegused on oleku kõige värskem väärtus.'],
        ['} catch {', 'Siia jõuab programm, kui server ei vasta või vastus pole JSON.'],
    ]),
    Spacer(1, 6),
    p('<b>Mis sinu arvates juhtub</b>, kui lisad arvustuse ja vajutad siis ' + c('F5') + '? Proovi.'),
    see('arvustus ilmub nimekirja ja pärast ' + c('F5') + '-e <b>on see ikka alles!</b> Vajuta nüüd „Lisa“ tühja vormiga: '
        'lehel on teade „Täida kõik lahtrid, hinne on 1 kuni 5.“ See teade tuli serverist. <b>Miks</b> on hea, et kontroll '
        'on serveris?'),
    stuck('kui lehel on „Serveriga ei saanud ühendust“, kontrolli, kas server töötab ja kas fetch-i aadress on õige.'),

    p('Samm 4: DELETE-marsruut', h2),
    p('Lisa faili ' + c('server/index.js') + ' POST-marsruudi järele:'),
    code(SERVER_9[SERVER_9.index("app.delete("):SERVER_9.index("app.get('/api/menyy'")].rstrip()),
    explain([
        ["app.delete('/api/arvustused/:id',", ':id on muutuv osa aadressis.'],
        ['Number(req.params.id)', 'Aadressist saadud tekst "2" muutub arvuks 2.'],
        ['arvustused.find((a) => a.id === id)', '.find() otsib esimese sobiva. === on „täpselt võrdne“.'],
        ['if (!leitud) {', 'Ei leidnud: vastab 404 ja lõpetab.'],
        ['arvustused.filter((a) => a.id !== id)', '.filter() teeb uue massiivi. !== on „ei ole võrdne“.'],
        ['res.json(leitud);', 'Vastab kustutatud arvustusega. Staatus on vaikimisi 200.'],
    ]),
    Spacer(1, 6),
    p('Salvesta ja käivita server uuesti.'),

    p('Samm 5: kustuta-nupp', h2),
    p('Kõigepealt anname kaardile nupu. Muuda fail ' + c('src/ArvustuseKaart.tsx') + ' selliseks:'),
    code(KAART_9.strip('\n'), 'src/ArvustuseKaart.tsx'),
    explain([
        ['kustuta: (id: number) => void;', 'Uus prop: funktsioon, mis saab arvu ega tagasta midagi (void).'],
        ['({ arvustus, kustuta }: Props)', 'Võtame propsidest välja ka kustuta.'],
        ['onClick={() => kustuta(arvustus.id)}', 'Nupuvajutusel kutsu kustuta selle arvustuse numbriga. Noolefunktsioon '
                                                 'on vajalik, muidu kutsutaks see välja juba joonistamise ajal.'],
    ]),
    Spacer(1, 6),
    p('VS Code joonib nüüd App-is rea ' + c('<ArvustuseKaart') + ' punaseks. TypeScript annab märku, et vajalik omadus '
      + c('kustuta') + ' on puudu. Lisa ' + c('App.tsx') + '-i funktsiooni ' + c('lisa') + ' järele:'),
    code(KUSTUTA_9.strip('\n')),
    explain([
        ['fetch(`/api/arvustused/${id}`,', 'Langetusrõhumärgid ehk tagurpidi ülakomad: ${id} asemele tuleb number.'],
        ["{ method: 'DELETE' }", 'Keha pole vaja, kõik on aadressis.'],
        ['setArvustused((praegused) =>\n  praegused.filter(...));', 'Eemaldab ka lehelt, nii et ei pea kõike uuesti '
         'küsima.'],
    ]),
    Spacer(1, 6),
    p('Ja anna funktsioon kaardile:'),
    code("""
<ArvustuseKaart key={a.id} arvustus={a} kustuta={kustuta} />
"""),
    see('igal kaardil on punakas nupp „Kustuta“. Vajuta seda: kaart kaob. Vajuta ' + c('F5') + ': see on ikka kadunud.'),
    stuck('kui arvustused kaovad ilma nupuvajutuseta, on ' + c('onClick') + '-is puudu ' + c('() =>') + '.'),

    p('Samm 6: taaskäivita server', h2),
    p('Lisa arvustus ja kustuta üks vana. <b>Mis sinu arvates juhtub</b>, kui serveri taaskäivitad? Pane server ' + c('Ctrl+C')
      + '-ga kinni, käivita uuesti ja värskenda lehte.'),
    see('alles on jälle algsed kolm arvustust. Massiiv elab programmi mälus ja programmi sulgedes see kaob. <b>Miks see '
        'juhtus?</b> Andmete säilimiseks tuleb need püsivalt salvestada, edaspidi kasutame selleks andmebaasi.'),

    p('Samm 7: salvesta Gitti', h2),
    p('Ava terminal, kus ükski server ei tööta, kontrolli, et oled projekti peakaustas, ja tee:'),
    code("""
git add .
git commit -m "Arvustuste lisamine ja kustutamine"
"""),
    p('Kui Git ütleb ' + c('not a git repository') + ', on projekt ZIP-failist: tee enne seda üks kord ' + c('git init')
      + '. Kui Git küsib nime ja e-posti, täida need käskudega ' + c('git config --global user.name "Sinu Nimi"') + ' ja '
      + c('git config --global user.email "sinu@naide.ee"') + '.'),

    p('Kogu fail', h2),
    p('Kui midagi ei tööta, võrdle oma faile nendega.'),
    *code_file(SERVER_9, 'server/index.js'),
    *code_file(APP_9, 'src/App.tsx'),

    CondPageBreak(120),
    p('Kui jõuad varem valmis', h2),
    p('Valikulised väljakutsed. Koodi pole, ainult vihjed.'),
    *bullets(
        '<b>Muutmine.</b> Marsruut ' + c('app.put(\'/api/arvustused/:id\', ...)') + ', mis muudab olemasolevat arvustust. '
        'Vihje: ' + c('.map()') + ' ja sama kontroll, mis POST-is.',
        '<b>Üks arvustus.</b> ' + c('GET /api/arvustused/2') + ' annab ühe arvustuse või 404. Vihje: ' + c('.find()') + '.',
        '<b>Liiga pikk kommentaar.</b> Vasta 400, kui kommentaar on pikem kui 200 märki. Vihje: ' + c('kommentaar.length')
        + '.',
    ),
]

# ---------------------------------------------------------------- 9. tund: kodutöö

STAATUS_9 = [
    ('GET /api/arvustused', '200'),
    ('POST /api/arvustused, keha {"toit":"Supp","hinne":4,"kommentaar":"Hea"}', '201'),
    ('POST /api/arvustused, keha {"toit":"Supp","hinne":9,"kommentaar":"Hea"}', '400'),
    ('POST /api/arvustused, keha {"hinne":4,"kommentaar":"Hea"}', '400'),
    ('DELETE /api/arvustused/2', '200'),
    ('DELETE /api/arvustused/99', '404'),
    ('GET /api/toidud', '404'),
]

kodutoo_9 = [
    p('Kodutöö: lisamine ja kustutamine', title),
    subtitle('9. tund', 'kodutöö'),
    row([p('Nimi', label_b), Field('nimi', 220), '', p('Kuupäev', label_b), Field('kuupaev', 110), ''],
        [51, 220, 18, 51, 110, WIDTH + 12 - 450], PALE),
    Spacer(1, 8),
    p('Midagi paigaldama ei pea, piisab brauserist. Abiks on konspekt ja veebilehe Päringulabor. Ava see fail kursuse '
      'lehel nupuga „Vaata“, täida lahtrid, vajuta „Laadi täidetud PDF alla“ ja saada fail aadressile '
      '<b>mtsopo@taltech.ee</b> hiljemalt 16.11 kell 23.59.', intro),

    p('1. Mis meetod?', h2),
]
for i, line in enumerate(['Tahad näha kõiki arvustusi', 'Tahad uue arvustuse lisada', 'Tahad arvustuse ära võtta']):
    kodutoo_9.append(row([p(line, label), Field(f'meetod_{i}', 90)], [230, 90]))
kodutoo_9 += [
    p('2. Mis staatusekood tuleb?', h2),
    p('Ennusta esmalt peast. Server töötab nagu tunnis tehtud söökla server. Iga päring saadetakse äsja käivitatud '
      'serverile, kus on algsed arvustused numbritega 1, 2 ja 3. Päringulaboris saad seda kontrollida, kui vajutad enne '
      'igat päringut „Taaskäivita server“.'),
]
for i, (line, _) in enumerate(STAATUS_9):
    kodutoo_9.append(row([p(c(line), label), Field(f'staatus_{i}', 50)], [WIDTH - 60, 50]))
kodutoo_9 += [
    Spacer(1, 6),
    CondPageBreak(150),
    p('3. Päringulabor', h2),
    question('Tee Päringulaboris kõik ülesanded läbi. Viimase järel näitab labor koodsõna. Kirjuta see siia.', 'koodsona'),
    question('Vali üks staatusekood, mille laboris said. Kirjuta kood ja selgita, miks server nii vastas.', 'lab_kood', 40),

    CondPageBreak(190),
    p('4. Loe koodi', h2),
    code("""
app.delete('/api/raamatud/:id', (req, res) => {
  const id = Number(req.params.id);
  // siin on ülejäänud kood
});
"""),
    p('Tuleb päring ' + c('DELETE /api/raamatud/7') + '.'),
    row([p('Mis on ' + c('req.params.id') + '? Kirjuta täpselt, koos jutumärkidega.', label), Field('kood_params', 80)],
        [330, 80]),
    row([p('Mis on muutuja ' + c('id') + ' väärtus?', label), Field('kood_id', 80)], [330, 80]),
    row([p('Mis tüüpi on ' + c('id') + ' (arv või tekst)?', label), Field('kood_tyyp', 80)], [330, 80]),
    Spacer(1, 6),

    CondPageBreak(150),
    p('5. Leia viga', h2),
    question('<b>a)</b> Serveris on rida ' + c('app.use(express.json());') + ' olemas ja enne marsruute. Ometi vastab server '
             '500 ja terminalis on ' + c('Cannot destructure') + '. Mis fetch-ist puudub? Kirjuta puuduv rida.', 'viga_a', 40,
             extra=code_parts("""
fetch('/api/arvustused', {
  method: 'POST',
  body: JSON.stringify({ toit, hinne, kommentaar }),
});
""")),
    question('<b>b)</b> Arvustused kaovad ilma nupuvajutuseta. Mis on valesti? Kirjuta parandatud rida.', 'viga_b', 40,
             extra=code_parts("""
<button onClick={kustuta(arvustus.id)}>Kustuta</button>
""")),
    question('<b>c)</b> Hinne 9 lisatakse ikkagi nimekirja, kuigi server saatis 400. Mis on puudu?', 'viga_c', 40,
             extra=code_parts("""
if (hinne < 1 || hinne > 5) {
  res.status(400).json({ viga: 'Vale hinne' });
}
const uus = { id: jargmineId, toit, hinne, kommentaar };
arvustused = [uus, ...arvustused];
""")),

    CondPageBreak(170),
    p('6. Mõtle', h2),
    question('<b>a)</b> Miks peab server hinnet kontrollima, kui vormis saab niikuinii valida ainult 1 kuni 5?', 'mote_a',
             44),
    question('<b>b)</b> Lisad arvustuse ja taaskäivitad serveri. Arvustus on kadunud. Miks? Mis selle lahendaks?', 'mote_b',
             44),
    question('<b>c) Lisaülesanne.</b> Täida marsruut, mis annab ühe arvustuse või vastab 404.', 'mote_c', 96,
             extra=code_parts("""
app.get('/api/arvustused/:id', (req, res) => {
  const id = Number(req.params.id);
  // otsi arvustus, vasta 404, kui seda pole, muidu saada see
});
""")),
]

BUILDS = {
    'react-server-konspekt': ('React küsib andmed serverilt', konspekt_8),
    'tunnijuhend-react-server': ('Tunnijuhend: React räägib serveriga', juhend_8),
    'kodutoo-react-server': ('Kodutöö: React ja server', kodutoo_8),
    'lisamine-kustutamine-konspekt': ('Arvustuste lisamine ja kustutamine', konspekt_9),
    'tunnijuhend-lisamine': ('Tunnijuhend: lisamine ja kustutamine', juhend_9),
    'kodutoo-lisamine': ('Kodutöö: lisamine ja kustutamine', kodutoo_9),
}

if __name__ == '__main__':
    for name in sys.argv[1:] or BUILDS:
        doc_title, story = BUILDS[name]
        build(f'public/files/{name}.pdf', doc_title, f'{SUBJECT} · {doc_title}', story, SUBJECT)
