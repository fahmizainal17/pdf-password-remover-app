const fileInput = document.getElementById('fileInput');
const pwdInput = document.getElementById('pwdInput');
const samePwd  = document.getElementById('samePwd');
const btn      = document.getElementById('go');

btn.addEventListener('click', async () => {
  const files = Array.from(fileInput.files);
  if (!files.length) return alert('Please select at least one PDF.');

  // If not samePwd, prompt per‐file
  let passwords = files.map(() =>
    samePwd.checked ? pwdInput.value : prompt('Password for this file:')
  );

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const pwd  = passwords[i];
    const arrayBuffer = await file.arrayBuffer();
    const base64 = btoa(
      new Uint8Array(arrayBuffer)
        .reduce((data, byte) => data + String.fromCharCode(byte), '')
    );

    // Call your function endpoint
    const resp = await fetch('/.netlify/functions/remove-password', {
      method: 'POST',
      body: JSON.stringify({ fileBase64: base64, password: pwd })
    });
    const { unlockedBase64, error } = await resp.json();
    if (error) {
      alert(`Failed for ${file.name}: ${error}`);
      continue;
    }

    // Trigger download
    const blob = new Blob(
      [Uint8Array.from(atob(unlockedBase64), c => c.charCodeAt(0))],
      { type: 'application/pdf' }
    );
    const url = URL.createObjectURL(blob);
    const a   = document.createElement('a');
    a.href    = url;
    a.download = `unlocked_${file.name}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  }
});
