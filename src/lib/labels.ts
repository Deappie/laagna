// All interface text in one place.
export const t = {
  courses: 'Klassid',
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
  types: {
    link: 'Link',
    video: 'Video',
    pdf: 'PDF',
    file: 'Fail',
    form: 'Vorm',
    game: 'Mäng',
  },
  game: {
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
