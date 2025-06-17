const { PDFDocument } = require('pdf-lib');

exports.handler = async (event) => {
  try {
    // Expect base64 PDF + password in JSON body
    const { fileBase64, password } = JSON.parse(event.body);
    const pdfBytes = Buffer.from(fileBase64, 'base64');

    // Load encrypted PDF
    const pdfDoc = await PDFDocument.load(pdfBytes, { password });

    // Save unlocked PDF
    const unlockedBytes = await pdfDoc.save();
    const unlockedBase64 = Buffer.from(unlockedBytes).toString('base64');

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ unlockedBase64 })
    };
  } catch (err) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: err.message })
    };
  }
};
