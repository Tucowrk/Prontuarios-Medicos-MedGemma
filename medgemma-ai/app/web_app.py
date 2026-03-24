import gradio as gr
from model import MedGemmaModel

model = MedGemmaModel(use_8bit=True)

def chat_function(message, history, image):
    if image is None:
        return "Upload an image to begin analysis."

    temp_path = "temp_image.jpg"
    image.save(temp_path)

    response = model.analyze_image(
        image_path=temp_path,
        prompt=message,
        max_tokens=800,
        temperature=0.7
    )

    return response


custom_css = """
body {
    background-color: #ffffff !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 0 !important;
    box-shadow: none !important;
    border: none !important;
}

.header {
    padding: 24px 0;
    border-bottom: 1px solid #e5e7eb;
}

.header h1 {
    font-size: 20px;
    font-weight: 600;
    color: #111827;
    margin: 0;
}

.layout {
    display: flex;
    gap: 40px;
    padding: 40px 0;
}

.left-panel {
    width: 320px;
}

.right-panel {
    flex: 1;
}

button {
    background-color: #111827 !important;
    border-radius: 6px !important;
    border: none !important;
}

textarea {
    border-radius: 6px !important;
}

"""

with gr.Blocks(css=custom_css) as demo:

    with gr.Column(elem_classes="header"):
        gr.Markdown("### MedGemma Clinical Imaging Assistant")

    with gr.Row(elem_classes="layout"):

        with gr.Column(elem_classes="left-panel"):
            image_input = gr.Image(
                type="pil",
                label="Medical Image",
                height=350
            )

        with gr.Column(elem_classes="right-panel"):
            chat = gr.ChatInterface(
                fn=chat_function,
                additional_inputs=[image_input],
                textbox=gr.Textbox(
                    placeholder="Enter clinical question regarding the image...",
                    container=False
                )
            )

demo.launch()
