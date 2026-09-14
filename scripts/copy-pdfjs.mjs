// Copies pdf.js runtime data (fonts, character maps, image decoders) into public/pdfjs/
// so PDFs that don't embed their fonts, or contain scanned images, display correctly.
import fs from 'node:fs';

const src = 'node_modules/pdfjs-dist';
const dest = 'public/pdfjs';

fs.rmSync(dest, { recursive: true, force: true });
for (const dir of ['standard_fonts', 'cmaps', 'wasm']) {
  fs.cpSync(`${src}/${dir}`, `${dest}/${dir}`, { recursive: true });
}
