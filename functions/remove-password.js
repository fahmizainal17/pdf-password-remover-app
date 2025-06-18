// functions/remove-password.js
const { PDFDocument } = require('pdf-lib');

exports.handler = async (event) => {
  console.log('Function invoked, raw event.body:', event.body);

  try {
    if (!event.body) {
      throw new Error('Request body is empty');
    }
    const { fileBase64, password } = JSON.parse(event.body);

    if (!fileBase64) throw new Error('Missing "fileBase64"');
    if (!password)   throw new Error('Missing "password"');

    const pdfBytes = Buffer.from(fileBase64, 'base64');
    const pdfDoc   = await PDFDocument.load(pdfBytes, { password });
    const unlockedBytes  = await pdfDoc.save();
    const unlockedBase64 = unlockedBytes.toString('base64');

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ unlockedBase64 }),
    };
  } catch (err) {
    console.error('Error unlocking PDF:', err);

    return {
      statusCode: 400,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: err.message || 'Unknown error' }),
    };
  }
};
