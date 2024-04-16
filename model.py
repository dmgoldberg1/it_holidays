import json
import time
import requests
import json

yandex_cloud_catalog = "b1glihj9h7pkj7mnd6at"
yandex_api_key = "AQVNyJRotHlHIhGec5YfWrslmo8tsbsc8eatOf_V"

yandex_gpt_model = "yandexgpt"

def get_gpt_questions():
    prompt = "Ты работодатель, который принимает людей на работу. Cоставь список из 10 вопросов, с помощью которых можно оценить коммуникативные навыки кандидата"
    system_prompt = "Выведи только список вопросов и всё: 1. вопрос1 2.вопрос2 3. вопрос3. Пожалуйста, не пиши ничего, кроме списка"

    body = {
        "modelUri": f"gpt://{yandex_cloud_catalog}/{yandex_gpt_model}",
        "completionOptions": {"stream": False, "temperature": 0.3, "maxTokens": "2000"},
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user", "text": prompt},
        ],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_api_key}",
        "x-folder-id": yandex_cloud_catalog,
    }

    response = requests.post(url, headers=headers, json=body)
    response_json = json.loads(response.text)
    question = response_json["result"]["alternatives"][0]["message"]["text"]
    return question


temperature = 0.6
# prompt = f"Ты устраиваешься на работу, ответь на вопросы о твоих коммуникативных навыках {question}"
# system_prompt = 'Выведи только ответы в виде: 1. ответ 1   2. ответ 2   3. ответ 3'
#
# body = {
#     "modelUri": f"gpt://{yandex_cloud_catalog}/{yandex_gpt_model}",
#     "completionOptions": {"stream": False, "temperature": temperature, "maxTokens": "2000"},
#     "messages": [
#         {"role": "system", "text": system_prompt},
#         {"role": "user", "text": prompt},
#     ],
# }
#
# url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Api-Key {yandex_api_key}",
#     "x-folder-id": yandex_cloud_catalog,
# }
#
# response = requests.post(url, headers=headers, json=body)
# response_json = json.loads(response.text)
#
# answer = response_json["result"]["alternatives"][0]["message"]["text"]
def get_mark_gpt(answer, question):
    prompt = f'Ты принимаешь человека на работу и даешь человеку следущие вопросы для оценки его коммуникативных навыков {question} Далее ты получаешь ответы. Выведи только одну строчку с оценками ответов от 1 до 5 через запятую(примерно так: 3, 4, 4) {answer}'

    body = {
        "modelUri": f"gpt://{yandex_cloud_catalog}/{yandex_gpt_model}",
        "completionOptions": {"stream": False, "temperature": temperature, "maxTokens": "2000"},
        "messages": [
            {"role": "user", "text": prompt},
        ],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_api_key}",
        "x-folder-id": yandex_cloud_catalog,
    }

    response = requests.post(url, headers=headers, json=body)
    response_json = json.loads(response.text)

    itog = response_json["result"]["alternatives"][0]["message"]["text"]
    return round(sum(map(float, itog.split(', '))) / 10, 1)

