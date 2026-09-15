// All interface text in one place.
export const t = {
  courses: 'Klassid',
  usefulLinks: 'Kasulikud lingid',
  noPosts: 'Materjale veel pole.',
  back: '← Kõik klassid',
  openLink: 'Ava link',
  viewPdf: 'Vaata',
  download: 'Laadi alla',
  openForm: 'Täida vorm',
  openNewTab: 'Ava uues aknas',
  video: 'Video',
  pdfLoading: 'Laadin PDF-i…',
  pdfError: 'PDF-i avamine ebaõnnestus.',
  pdfNotFound: 'Faili ei leitud.',
  pdfFillHint: 'Selle PDF-i saad täita otse siin: klõpsa lahtril ja kirjuta. Kui oled valmis, vajuta „Laadi täidetud PDF alla“ ja saada fail õpetajale.',
  pdfDownloadFilled: 'Laadi täidetud PDF alla',
  pdfSaving: 'Salvestan…',
  types: {
    link: 'Link',
    video: 'Video',
    pdf: 'PDF',
    file: 'Fail',
    form: 'Vorm',
    game: 'Mäng',
  },
  codeGame: {
    title: {
      html: 'Harjutus: pane HTML kokku',
      css: 'Harjutus: pane CSS kokku',
    },
    hint: 'Klõpsa sõnal või lohista see lünka. Täidetud lüngal klõpsates saad sõna tagasi.',
    preview: 'Nii peaks tulemus välja nägema:',
    progress: (i: number, n: number) => `Ülesanne ${i}/${n}`,
    gap: 'Lünk',
    check: 'Kontrolli',
    next: 'Järgmine ülesanne',
    restart: 'Alusta otsast',
    correct: 'Õige! 🎉',
    allDone: 'Kõik ülesanded on tehtud! 🎉',
    fillAll: 'Täida enne kontrollimist kõik lüngad.',
    wrong: (n: number) =>
      `${n === 1 ? '1 lünk on' : `${n} lünka on`} valesti. Klõpsa punasel lüngal, et sõna tagasi võtta.`,
  },
  escapeGame: {
    rooms: {
      hex: {
        title: 'Põgenemistuba: serveriruum',
        story:
          'Jäid hilja õhtul kooli serveriruumi ja uks vajus lukku. Väljapääsuni on seitse lukku ning iga lukk tahab koodi, mis on peidetud kahend- või kuueteistkümnendsüsteemi. Kell hakkab tiksuma kohe, kui alustad. Kui kiiresti sa välja saad?',
        last: 'Ava uks',
        finishTitle: 'Oled vaba! 🎉',
        finishFact:
          'Ja veel üks fakt: ka selle veebilehe iga muudatus saab 16-süsteemis tunnuse, näiteks 3de79da. Programmeerijad kasutavad neid tunnuseid iga päev.',
      },
      web: {
        title: 'Põgenemistuba: lukus koduleht',
        story:
          'Homme on koolis lahtiste uste päev, aga keegi on kooli kodulehe seitsme lukuga kinni pannud. Iga lukk avaneb, kui leiad HTML-ist või CSS-ist vea või puuduva tüki. Kell hakkab tiksuma kohe, kui alustad. Kui kiiresti sa lehe päästad?',
        last: 'Päästa leht',
        finishTitle: 'Leht on päästetud! 🎉',
        finishFact:
          'Ja veel üks fakt: vajuta mistahes veebilehel F12 (Macis Cmd+Option+I) ja näed selle lehe HTML-i ja CSS-i. Nii on paljud veebiarendajad teiste lehtede pealt õppinud.',
      },
    },
    begin: 'Alusta',
    lock: (i: number, n: number) => `Lukk ${i}/${n}`,
    answer: 'Kood',
    open: 'Ava lukk',
    hint: 'Vihje (+30 s)',
    empty: 'Kirjuta kõigepealt kood.',
    wrong: 'Lukk ei avanenud. Kontrolli arvutust ja proovi uuesti.',
    correct: 'Klõps! Lukk avanes. 🔓',
    fact: 'Kas teadsid?',
    next: 'Järgmine lukk',
    finish: (time: string, hints: number) =>
      `Said hakkama ajaga ${time}${hints === 0 ? ' ja ühegi vihjeta' : hints === 1 ? ', kasutasid ühe vihje' : `, kasutasid ${hints} vihjet`}. Kas pinginaaber saab kiiremini?`,
    restart: 'Proovi uuesti',
  },
  hexGame: {
    title: 'Värvimäng: kuueteistkümnendsüsteem',
    explore: 'Liiguta liugureid ja vaata, kuidas värvikood muutub.',
    red: 'Punane (R)',
    green: 'Roheline (G)',
    blue: 'Sinine (B)',
    question: (code: string) => `Millist värvi on ${code}?`,
    option: (n: number) => `Valik ${n}`,
    correct: 'Õige! 🎉',
    wrong: (code: string) => `See on ${code}. Mõtle, kui palju on koodis punast, rohelist ja sinist.`,
    next: 'Järgmine',
    score: (n: number) => `Õigeid: ${n}`,
  },
  binaryGame: {
    title: 'Mäng: kahend- ja kümnendsüsteem',
    toBinary: (n: number) => `Kirjuta arv ${n} kahendsüsteemis. Klõpsa bittidel.`,
    toDecimal: (b: string) => `Mis arv on ${b} kümnendsüsteemis?`,
    answer: 'Vastus',
    check: 'Kontrolli',
    next: 'Järgmine',
    correct: 'Õige! 🎉',
    wrongBinary: (n: number) => `Praegu on seal arv ${n}. Proovi veel!`,
    wrongDecimal: 'Pole päris õige. Liida kokku nende bittide väärtused, kus on 1.',
    score: (n: number) => `Õigeid: ${n}`,
    bits4: '4 bitti',
    bits8: '8 bitti',
  },
} as const;

export function formatDate(d: Date): string {
  return d.toLocaleDateString('et-EE', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  });
}
