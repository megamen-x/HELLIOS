import gradio as gr
import time

theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(c100="#f2fcde", c200="#dcf7bb", c300="#b8f08a", c400="#94de4a", c50="#fbfdf2", c500="#73c421", c600="#6aa216", c700="#557f15", c800="#396416", c900="#305214", c950="#2d4e13"),
    secondary_hue="emerald",
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

def warning_fn():
    gr.Warning("Введите текст или выберите файл для распознавания!")

def info_fn():
    gr.Info("Необходимо ввести текст или загрузить ваш файл и выбрать параметры отслеживания")


with gr.Blocks(theme=theme) as demo:
    gr.Markdown('<a name="readme-top"></a>\
        <p align="center" ><font size="30px"><strong style="font-family: Limelight">HELLIOS</strong></font></p> \
        <p align="center"><font size="5px">Автоматизированный инструмент анализа комментариев учащихся <br>\
            Создано <strong>megamen</strong>, совместно с платформой <strong>Geekbrains</strong> </font></p> ')

    # Var 1
    # with gr.Row():
    #     with gr.Column():
    #         gr.Markdown('<p align="center" ><font size="4px"><strong style="font-family: JetBrains Mono">Обработка файлов</strong></font></p>')
    #         textfile = gr.File(show_label=False,)
    #         with gr.Column():
    #             with gr.Row(): 
    #                 btn = gr.Button(value="Начать распознавание",)
    #                 trigger_info = gr.Button(value="Подробнее",)

    #     with gr.Column():
    #         gr.Markdown('<p align="center" ><font size="4px"><strong style="font-family: JetBrains Mono">Обработка текста</strong></font></p>')
    #         subject = gr.Textbox(lines=5, label="Поле для текста", placeholder="Введите ваш текст сюда",)
    #         verb = gr.CheckboxGroup(["Активность", "Поведение", "Технические проблемы", "Стоп-слова"], label="Параметры отслеживания",)
    
    # Var 2
    with gr.Row():
        with gr.Column():
            with gr.Tab('Обработка файлов'):
                textfile = gr.File(show_label=False,)
            with gr.Tab('Обработка текста'):
                subject = gr.Textbox(lines=6, label="Поле для текста", placeholder="Введите ваш текст сюда",)
            with gr.Column():
                with gr.Row(): 
                    btn = gr.Button(value="Начать распознавание",)
                    trigger_info = gr.Button(value="Подробнее",)
            with gr.Tab('Параметры'):
                verb = gr.CheckboxGroup(["Активность", "Поведение", "Технические проблемы", "Стоп-слова"], label="Параметры отслеживания",show_label=False)
            
    # Var 3 
    # with gr.Row():
    #     with gr.Row():
    #         with gr.Tab('Обработка файлов'):
    #             textfile = gr.File(show_label=False,)
    #         with gr.Tab('Обработка текста'):
    #             subject = gr.Textbox(lines=6, label="Поле для текста", placeholder="Введите ваш текст сюда",)
    #         with gr.Column():
    #             with gr.Tab('Параметры'):
    #                 verb = gr.CheckboxGroup(["Активность", "Поведение", "Технические проблемы", "Стоп-слова"], label="Параметры отслеживания",show_label=False)
    #             with gr.Row(): 
    #                 btn = gr.Button(value="Начать распознавание",)
    #                 trigger_info = gr.Button(value="Подробнее",)

    with gr.Row():
        output = gr.Textbox(label="Предобработка", placeholder="Здесь будут ключевые слова", interactive=False, lines=7,)
        output_1 = gr.Textbox(label="Результат обработки", placeholder="Здесь будет обработанный текст", interactive=False, lines=7)
    
    with gr.Row(): 
        with gr.Row(): 
            clr_btn = gr.ClearButton([subject, verb, output_1], value="Очистить контекст",)
            # gr.Markdown()
        gr.Markdown()


    def file_processing(param1, param2):
        if param1 and param2:
            success()
            return f"{param1} {param2}"
        else:
            warning_fn()
    
    def text_processing(param1, param2, progress=gr.Progress()):
        progress(0, desc="Starting")
        time.sleep(1)
        progress(0.05)
        if param1 and param2:
            time.sleep(0.25)
            success()
            return f"{param1} {param2}"
        else:
            warning_fn()
            
    btn.click(text_processing, [subject, verb], output_1)
    trigger_info.click(info_fn, None)

demo.launch(allowed_paths=["/assets/"])


    