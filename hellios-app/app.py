import gradio as gr
import time
import plotly.express as px
from preprocess import *

text = 'Здесь будут общие данные'

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

def warning_file():
    gr.Warning("Выберите файл для распознавания!")

def info_fn():
    gr.Info("Необходимо загрузить ваш файл и при необходимости дополнить стоп-слова и разрешенные домены")

def info_req():
    gr.Info("Стоп-слова и разрешенные домены взяты по-умолчанию")
    
def info_res():
    gr.Info("Полный JSON-файл можно найти в папке проекта")

def text_processing(textfile, badwords, gooddomen, ):
    time.sleep(1)
    bad_path = str(badwords)
    urls_path = str(gooddomen)
    if textfile:
        if badwords and gooddomen:
            return data_processing(textfile, bad_path, urls_path)
        else:
            info_req()
            time.sleep(0.25)
            df, string = data_processing(textfile, )
            info_res()
            return df, string
    else:
        warning_file()
   
output = [gr.Dataframe(row_count = (4, "dynamic"), col_count=(4, "fixed"), label="Predictions")]

with gr.Blocks(theme=theme) as demo:
    gr.Markdown('<a name="readme-top"></a>\
        <p align="center" ><font size="30px"><strong style="font-family: Limelight">HELLIOS</strong></font></p> \
        <p align="center"><font size="5px">Автоматизированный инструмент анализа комментариев учащихся <br>\
            Создано <strong>megamen</strong>, совместно с платформой <strong>Geekbrains</strong> </font></p> ')

    with gr.Row():
        with gr.Column():
            with gr.Tab('Обработка файлов'):
                textfile = gr.File(label="Документ с данными", file_types=['.csv','.xlsx'])
            with gr.Row():
                with gr.Tab('База знаний'):
                    with gr.Row(): 
                        badwords = gr.File(label="Словарь стоп-слов", file_types=['.txt',])
                        gooddomen = gr.File(label="Словарь разрешенных доменов",file_types=['.txt',])
            with gr.Column():
                with gr.Row(): 
                    btn = gr.Button(value="Начать распознавание",)
                    trigger_info = gr.Button(value="Подробнее",)

    with gr.Row():
        output = gr.Dataframe()
        output_1 = gr.Textbox(label="Результат обработки", placeholder="Здесь будут общие данные по файлу", interactive=False, lines=7)
    
    with gr.Row(): 
        with gr.Row(): 
            clr_btn = gr.ClearButton([textfile, output_1, output, badwords, gooddomen], value="Очистить контекст",)
        gr.Markdown()

    btn.click(text_processing, inputs=[textfile, badwords, gooddomen, ], outputs=[output, output_1,])
    trigger_info.click(info_fn, None)

demo.launch()


    