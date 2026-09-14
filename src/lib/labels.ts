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
