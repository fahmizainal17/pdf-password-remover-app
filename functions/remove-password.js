const { PDFDocument } = require('pdf-lib');

exports.handler = async (event) => {
  try {
    const { fileBase64, password } = JSON.parse(event.body);
    const pdfBytes = Buffer.from(fileBase64, 'base64');
    const pdfDoc   = await PDFDocument.load(pdfBytes, { password });
    const unlocked = await pdfDoc.save();
    return {
      statusCode: 200,
      body: JSON.stringify({
        unlockedBase64: Buffer.from(unlocked).toString('base64')
      })
    };
  } catch (err) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: err.message })
    };
  }
};
