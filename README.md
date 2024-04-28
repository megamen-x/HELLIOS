<a name="readme-top"></a>  

<div align="center">
  <p align="center">
    <h1 align="center">HELLIOS</h1>
  </p>

  <p align="center">
    <p><strong>Автоматизированный инструмент анализа комментариев учащихся.</strong></p>
    Создано <strong>megamen</strong>, совместно с совместно с платформой <strong>Geekbrains</strong>
    <br /><br />
    <a href="https://github.com/megamen-x/HELLIOS/issues" style="color: black;">Сообщить об ошибке</a>
    ·
    <a href="https://github.com/megamen-x/HELLIOS/discussions/1" style="color: black;">Предложить улучшение</a>
  </p>
</div>

**Содержание:**
- [Проблематика](#title1)
- [Описание решения](#title2)
- [Развертка приложения](#title3)
- [Обновления](#title4)

## <h3 align="start"><a id="title1">Проблематика кейсодержателя</a></h3> 
Необходимо создать сервис, с применением технологий искусственного интеллекта, в виде программного модуля анализа комментариев учащихся на образовательной платформе.

Ключевые функции программного модуля:
* интерактивный мониторинг и анализ комментариев к уроку;
* определение и отслеживания ключевых индикаторов процессов обучения;
* определение технических неполадок вебинара с указанием тайм-кода;

<p align="right">(<a href="#readme-top"><i>Вернуться наверх</i></a>)</p>

## <h3 align="start"><a id="title2">Краткое описание решения</a></h3>

**Machine Learning:**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)

 - **Общая схема решения:**

    ![block 3](https://github.com/megamen-x/HELLIOS/assets/100156578/98cce222-fc0a-4efe-b67f-8cee1a26f13e)


 - **Использованные решения:**
    - **```Preprocessing```**:
      - регулярные выражения для определения стоп-слов;
      - ассоциативные правила для определения сообщений о тех. неполадках платформы;
      - оценка наличия комментариев первые k-min лекции;
      - оценка количества комментариев в окне n-min;
      - оценка общего количества комментариев за лекцию;
    - **```ML```**:
      - cointegrated/rubert-tiny2 (классификация спама и определение сообщений о тех. неполадках);

Пример генерации на основе лекций:
    - [Ссылка](https://github.com/megamen-x/HELLIOS/blob/main/hellios-app/data.json)

Опробовать решение:
   - [HELLIOS](https://huggingface.co/spaces/AtLan9/HELLIOS)

Ссылка на скачивание моделей:
   - [HF-HUB](https://huggingface.co/whatisslove11/labse)




<p align="right">(<a href="#readme-top"><i>Вернуться наверх</i></a>)</p>

## <h3 align="start"><a id="title3">Развертка приложения</a></h3> 

<details>
  <summary> <strong><i>Локальный запуск решения на устройстве:</i></strong> </summary>
  
  - Для запуска приложения:
  
  ```
  ./HELLIOS/hellios-app/app.py
  ```
  или 
   ```
  gradio app.py
  ```


</details> 

<p align="right">(<a href="#readme-top"><i>Вернуться наверх</i></a>)</p>

## <h3 align="start"><a id="title4">Обновления</a></h3> 

***Все обновления и нововведения будут размещаться здесь!***

<p align="right">(<a href="#readme-top"><i>Вернуться наверх</i></a>)</p>
