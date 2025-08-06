function closeMessage() {
    const message = alertsContainer.querySelector('div');
    message.remove();
}


function closeMessages() {
    const messages = alertsContainer.querySelectorAll('div');
    let step = 600;
    let messageNum = 1;
    for (let message of messages) {
        setTimeout(closeMessage, messageNum * step);
        messageNum++;
    }
}
const alertsContainer = document.getElementById('alertsFixedContainer');
setTimeout(closeMessages, 2000);