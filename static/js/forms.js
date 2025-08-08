const codeCount = document.getElementById("count");
const textArea = document.querySelector('textarea');

const numChars = textArea.value.length;
codeCount.textContent = `${numChars}/5000`;

textArea.addEventListener('input', () => {
    const numChars = textArea.value.length;
    codeCount.textContent = `${numChars}/5000`;
})



// 1. Сохранение данных формы (по таймеру)
function saveDraft() {
const name = document.querySelector('input[name="name"]');
const lang = document.querySelector('select[name="lang"]');
const code = document.querySelector('textarea[name="code"]');
const formData = {
name: name.value,
lang: lang.value,
code: code.value,
}
// sendMessage("Данные формы сохранены");
localStorage.setItem(formDataKey, JSON.stringify(formData));
}

setInterval(saveDraft, 5000);