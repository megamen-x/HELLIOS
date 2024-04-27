<a name="readme-top"></a>  

<div align="center">
  <p align="center">
    <h1 align="center">HELLIOS</h1>
  </p>

  <p align="center">
    <p><strong>Автоматизированный инструмент анализа комментариев учащихся.</strong></p>
    Создано <strong>megamen</strong>, совместно с совместно с платформой <strong>Geekbrains</strong>
    <br /><br />
    <a href="https://github.com/mireaMegaman/HELLIOS/issues" style="color: black;">Сообщить об ошибке</a>
    ·
    <a href="https://github.com/mireaMegaman/HELLIOS/discussions/1" style="color: black;">Предложить улучшение</a>
  </p>
</div>

**Содержание:**
- [Проблематика задачи](#title1)
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

    ```здесь будет схема решения```


 - **Использованные решения:**
    - **```Preprocessing```**:
      - обработка данных с помощью эвристик и регулярных выражений;
    - **```NLP```**:
      - cointegrated/rubert-tiny2;

Ссылки на скачивание моделей:
   - [HF-HUB](https://huggingface.co/)


**Серверная часть**

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


<p align="right">(<a href="#readme-top"><i>Вернуться наверх</i></a>)</p>

## <h3 align="start"><a id="title3">Развертка приложения</a></h3> 

<details>
  <summary> <strong><i>Локальный запуск приложения на устройстве:</i></strong> </summary>
  
  - Для запуска приложения:
  
  ```
  ./HELLIOS/hellios-app/Release/hellios.py
  ```

  - Для запуска сервера (Windows vs-code):
  
  ```
  cd hellios-server
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
  ```
  - После установки зависимостей (5-7 минут):
  ```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
  ```

</details> 

<p align="right">(<a href="#readme-top"><i>Вернуться наверх</i></a>)</p>

## <h3 align="start"><a id="title4">Обновления</a></h3> 

***Все обновления и нововведения будут размещаться здесь!***

<p align="right">(<a href="#readme-top"><i>Вернуться наверх</i></a>)</p>
