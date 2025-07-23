''' Для cmd
curl -X POST http://127.0.0.1:5000/predict_model -H "Content-Type: application/json" -d "{\"text\":\"Я хуйня\"}"
'''
from fastapi import FastAPI, Request, HTTPException
import dill
import pandas as pd
from pydantic import BaseModel

import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


app = FastAPI()



snowball = SnowballStemmer(language="russian")
russian_stop_words = stopwords.words("russian")

def tokenize_sentence(sentence: str, remove_stop_words: bool = True):
    tokens = word_tokenize(sentence, language="russian")
    tokens = [i for i in tokens if i not in string.punctuation]
    if remove_stop_words:
        tokens = [i for i in tokens if i not in russian_stop_words]
    tokens = [snowball.stem(i) for i in tokens]
    return tokens

# Загрузка модели (с проверкой)
with open('model.pkl', 'rb') as f:
    model = dill.load(f)


# Глобальный счетчик запросов
request_count = 0

# Модель для валидации входных данных
class PredictionInput(BaseModel):
    text: str  # Текст для классификации

@app.get("/")
def read_root():
    return {"message": "Сервер работает"}

@app.get("/stats")
def stats():
    return {"request_count": request_count}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/predict_model")
def predict_model(input_data: PredictionInput):
    global request_count
    request_count += 1

    predictions = model.predict([input_data.text])
        
    # Формируем ответ
    return {"Вывод:": "Это плохой комментарий" if predictions[0] == 1 else "Это обычный комментарий"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)