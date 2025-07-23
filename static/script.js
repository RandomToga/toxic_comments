document.getElementById('commentForm').addEventListener('submit', async function (e) {
  e.preventDefault(); // отменяет стандартную отправку формы

  const commentText = document.getElementById('commentInput').value;
  const resultElement = document.getElementById('result');

  try {
    const response = await fetch('/predict_model', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: commentText }) // отправка JSON с текстом
    });

    const data = await response.json(); // получение ответа
    resultElement.textContent = data["Вывод:"] || "Ошибка: ответ не распознан";
  } catch (error) {
    resultElement.textContent = "Ошибка при отправке запроса";
    console.error(error);
  }
});
