import gradio as gr
import time
import plotly.express as px

df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig = px.pie(df, values='pop', names='country', title='Population of European continent')

theme = gr.themes.Soft(
    primary_hue="amber",
    secondary_hue="yellow",
    text_size="lg",
    spacing_size="lg",
    font=[gr.themes.GoogleFont('JetBrains Mono'), gr.themes.GoogleFont('Limelight'), 'system-ui', 'sans-serif'],
    # Montserrat 
).set(
    block_radius='*radius_xxl',
    button_large_radius='*radius_xl',
    button_large_text_size='*text_md',
    button_small_radius='*radius_xl',
)

def failure():
    raise gr.Error("Ошибка распознавания!")

def success():
    return True

def warning_file():
    gr.Warning("Выберите файл для распознавания!")
    
def warning_param():
    gr.Warning("Выберите параметры распознавания!")

def info_fn():
    gr.Info("Необходимо ввести текст или загрузить ваш файл и выбрать параметры отслеживания")

def text_processing(file, param, slider_1, progress=gr.Progress()):
    progress(0, desc="Starting")
    time.sleep(1)
    progress(0.05)
    if file:
        if param:
            time.sleep(0.25)
            success()
            return f"{param} - {slider_1}"
        else:
            warning_param()
    else:
        warning_file()


with gr.Blocks(theme=theme) as demo:
    gr.Markdown('<a name="readme-top"></a>\
        <p align="center" ><font size="30px"><strong style="font-family: Limelight">HELLIOS</strong></font></p> \
        <p align="center"><font size="5px">Автоматизированный инструмент анализа комментариев учащихся <br>\
            Создано <strong>megamen</strong>, совместно с платформой <strong>Geekbrains</strong> </font></p> ')
    
    # Var 2
    with gr.Row():
        with gr.Column():
            with gr.Tab('Обработка файлов'):
                textfile = gr.File(label="Документ с данными",)
            # with gr.Tab('Обработка текста'):
            #     subject = gr.Textbox(lines=6, label="Поле для текста", placeholder="Введите ваш текст сюда",)
            with gr.Column():
                with gr.Row(): 
                    btn = gr.Button(value="Начать распознавание",)
                    trigger_info = gr.Button(value="Подробнее",)
            with gr.Tab('Параметры'):
                verb = gr.CheckboxGroup(["Активность", "Поведение", "Технические проблемы", "Стоп-слова"], label="Параметры отслеживания")
                slider_1 = gr.Slider(1,20,step=1,value=4,label="Количество записей", )

            with gr.Tab('База знаний'):
                with gr.Row(): 
                    badwords = gr.File(label="Словарь стоп-слов",)
                    gooddomen = gr.File(label="Словарь разрешенных доменов",)
    
    with gr.Row():
        gr.Plot(fig, label="Активность пользователей")

    with gr.Row():
        output = gr.Textbox(label="Предобработка", placeholder="Здесь будут ключевые слова", interactive=False, lines=7,)
        output_1 = gr.Textbox(label="Результат обработки", placeholder="Здесь будет обработанный текст", interactive=False, lines=7)
    
    with gr.Row(): 
        with gr.Row(): 
            clr_btn = gr.ClearButton([textfile, verb, output_1], value="Очистить контекст",)
            # gr.Markdown()
        gr.Markdown()
  
    btn.click(text_processing, [textfile, verb, slider_1], output_1)
    trigger_info.click(info_fn, None)

demo.launch(allowed_paths=["/assets/"])


    