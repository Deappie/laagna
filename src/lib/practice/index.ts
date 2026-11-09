// Data for the interactive practice sheets (PracticeSheet.astro).
// kt1 is written by hand; kt2 is generated together with the paper test by teacher/kontrolltoo2_10it.py.
import kt2json from './kt2.json';

// num: decimal number (spaces, units and "0,5" allowed) · bin/hex: leading zeros ignored
// text: exact (case matters) · codes: list of numbers · word: one of several words, any case
// compact: exact after removing spaces, any case (RLE, truth table columns) · list: words in this order, any case
export type Kind = 'num' | 'bin' | 'hex' | 'text' | 'codes' | 'word' | 'compact' | 'list';
export interface Field {
  label: string;
  kind: Kind;
  answer: string | string[];
}
export interface Question {
  text: string;
  fields: Field[];
  hint: string;
  solution: string;
  open?: boolean; // no automatic check, only a model answer
}
export interface Section {
  title: string;
  questions: Question[];
}

export const kt1: Section[] = [
  {
    title: 'A. Teisendused',
    questions: [
      {
        text: 'Teisenda 37 kahend- ja 16-süsteemi.',
        fields: [{ label: 'Kahendsüsteemis', kind: 'bin', answer: '100101' }, { label: '16-süsteemis', kind: 'hex', answer: '25' }],
        hint: 'Kahendsüsteemi jaoks otsi astmereast suurimad sobivad: 32 + 4 + 1. 16-süsteemi jaoks jaga kahendarv paremalt neljaks.',
        solution: '37 = 32 + 4 + 1 = 100101. Neljaks jagatult 0010 0101, ehk 25.',
      },
      {
        text: 'Teisenda 11001100 kümnend- ja 16-süsteemi.',
        fields: [{ label: 'Kümnendsüsteemis', kind: 'num', answer: '204' }, { label: '16-süsteemis', kind: 'hex', answer: 'CC' }],
        hint: 'Liida nende bittide väärtused, kus on 1: 128 + 64 + ... 16-süsteemis jaga neljaks: 1100 1100.',
        solution: '128 + 64 + 8 + 4 = 204. 1100 on 12 ehk C, seega CC.',
      },
      {
        text: 'Teisenda 7E kümnend- ja kahendsüsteemi.',
        fields: [{ label: 'Kümnendsüsteemis', kind: 'num', answer: '126' }, { label: 'Kahendsüsteemis', kind: 'bin', answer: '1111110' }],
        hint: '7E = 7 · 16 + E, kus E on 14. Kahendsüsteemis kirjuta iga sümbol nelja bitina: 7 = 0111, E = 1110.',
        solution: '7 · 16 + 14 = 126. 0111 1110 ehk 1111110.',
      },
      {
        text: 'Teisenda 250 16-süsteemi.',
        fields: [{ label: '16-süsteemis', kind: 'hex', answer: 'FA' }],
        hint: 'Mitu korda mahub 16 arvu 250 sisse ja mis jääb üle? 10 on A, 15 on F.',
        solution: '250 = 15 · 16 + 10. 15 on F ja 10 on A, seega FA.',
      },
    ],
  },
  {
    title: 'B. Bitid ja väärtused',
    questions: [
      {
        text: 'Mitu erinevat väärtust mahub 5 bitti?',
        fields: [{ label: 'Väärtusi', kind: 'num', answer: '32' }],
        hint: 'Kahekordista viis korda: 2, 4, 8, ...',
        solution: '2 · 2 · 2 · 2 · 2 = 32.',
      },
      {
        text: 'Mitu bitti on vähemalt vaja, et kirjutada kõik arvud 0 kuni 200?',
        fields: [{ label: 'Bitte', kind: 'num', answer: '8' }],
        hint: 'Väärtusi on 201. Kahekordista, kuni jõuad vähemalt 201-ni, ja loe sammud kokku.',
        solution: '7 bitti annab ainult 128 väärtust, 8 bitti annab 256. Vaja on 8 bitti.',
      },
      {
        text: 'Miks on ASCII-tabelis just 128 kohta? Kirjuta vastus ja võrdle siis näidisvastusega.',
        fields: [],
        open: true,
        hint: 'Mitu bitti kasutab ASCII?',
        solution: 'ASCII kasutab 7 bitti ja 7 bitiga saab kirja panna 2 · 2 · 2 · 2 · 2 · 2 · 2 = 128 eri väärtust.',
      },
    ],
  },
  {
    title: 'C. Failimahud',
    questions: [
      {
        text: 'Raamatus on 200 lehekülge, igal umbes 2500 märki. Mitu baiti see võtab? Mitu MB?',
        fields: [{ label: 'Baite', kind: 'num', answer: '500000' }, { label: 'MB', kind: 'num', answer: '0.5' }],
        hint: 'Korruta lehekülgede arv märkide arvuga. Iga märk on üks bait ja miljon baiti on 1 MB.',
        solution: '200 · 2500 = 500 000 baiti ehk 0,5 MB.',
      },
      {
        text: 'Kui suur on 8-megapiksline foto pakkimata, kui iga piksel võtab 3 baiti? Vasta megabaitides.',
        fields: [{ label: 'MB', kind: 'num', answer: '24' }],
        hint: 'Megapikslite arv korda 3 baiti.',
        solution: '8 miljonit pikslit · 3 baiti = 24 MB.',
      },
      {
        text: 'Mitu 4 MB fotot mahub 128 GB telefoni? (1 GB = 1000 MB)',
        fields: [{ label: 'Fotosid', kind: 'num', answer: '32000' }],
        hint: 'Tee gigabaidid enne megabaitideks: 128 GB = 128 000 MB. Siis jaga foto suurusega.',
        solution: '128 000 MB : 4 MB = 32 000 fotot.',
      },
    ],
  },
  {
    title: 'D. Tekst',
    questions: [
      {
        text: 'Mis sõna on 73 84?',
        fields: [{ label: 'Sõna', kind: 'text', answer: 'IT' }],
        hint: 'Otsi arvud ASCII-tabelist (konspektis või Tekstilaboris). Suur ja väike täht on erinevad.',
        solution: '73 on I ja 84 on T: IT.',
      },
      {
        text: 'Kirjuta sõna „Tere“ ASCII-koodidena.',
        fields: [{ label: 'Koodid', kind: 'codes', answer: '84 101 114 101' }],
        hint: 'T on 84. Väiketähed on alati 32 võrra suuremad kui samad suurtähed (E on 69).',
        solution: 'T = 84, e = 101, r = 114, e = 101.',
      },
      {
        text: 'Mitu märki ja mitu baiti (UTF-8) on sõnas „süda“?',
        fields: [{ label: 'Märke', kind: 'num', answer: '4' }, { label: 'Baite', kind: 'num', answer: '5' }],
        hint: 'Kõigepealt loe märgid kokku. Siis pea meeles, et täpitäht võtab UTF-8-s kaks baiti.',
        solution: 'Märke on 4: s, ü, d, a. ü võtab kaks baiti, ülejäänud ühe: 1 + 2 + 1 + 1 = 5 baiti.',
      },
    ],
  },
  {
    title: 'E. Värvikood',
    questions: [
      {
        text: 'Värvikood on #FFA500. Kirjuta punane, roheline ja sinine kümnendsüsteemis. Mis värv see on?',
        fields: [
          { label: 'Punane (R)', kind: 'num', answer: '255' },
          { label: 'Roheline (G)', kind: 'num', answer: '165' },
          { label: 'Sinine (B)', kind: 'num', answer: '0' },
          { label: 'Värv', kind: 'word', answer: ['oranž', 'oranz', 'orange', 'oranzh', 'kollakasoranž'] },
        ],
        hint: 'Iga kaks sümbolit on üks värv: FF, A5 ja 00. A5 = 10 · 16 + 5.',
        solution: 'FF = 255, A5 = 165, 00 = 0. Täis punane, üle poole rohelist, sinist pole: oranž.',
      },
    ],
  },
];

export const sheets: Record<string, Section[]> = { kt1, kt2: kt2json as Section[] };
