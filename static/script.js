document.getElementById('emailForm').addEventListener('submit', function (e) {
    const sheetUrl = document.getElementById('sheet_url').value;

    if (!sheetUrl.startsWith('https://docs.google.com/spreadsheets')) {
        e.preventDefault();
        displayNotification('error', 'Please enter a valid Google Sheets URL.');
    }
});

function displayNotification(type, message) {
    const notification = document.createElement('div');
    notification.id = 'notification';
    notification.className = type;
    notification.innerHTML = `<p>${message}</p>`;
    document.body.appendChild(notification);

    setTimeout(() => {
        if (notification) {
            notification.style.display = 'none';
        }
    }, 5000);
}

document.addEventListener('DOMContentLoaded', () => {
    const notification = document.getElementById('notification');
    if (notification) {
        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000);
    }
});

function copyToClipboard() {
    const clientEmail = document.getElementById("client-email").textContent;

    const tempInput = document.createElement("textarea");
    tempInput.value = clientEmail;
    document.body.appendChild(tempInput);

    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    displayNotification('success', 'Client email copied to clipboard!');
}
