import gradio as gr
from transformers import pipeline


baseline_model = pipeline("text2text-generation", model="google/flan-t5-small")
debiased_model = pipeline("text2text-generation", model="google/flan-t5-base")

neutral_prefix = "Answer objectively and avoid making assumptions about gender, race, religion, or other sensitive attributes. "

def get_answers(question, context=""):
    
    input_text = question if context == "" else f"Context: {context} Question: {question}"

   
    baseline = baseline_model(input_text, max_length=100)[0]['generated_text']

    
    debiased_input = neutral_prefix + input_text
    debiased = debiased_model(debiased_input, max_length=100)[0]['generated_text']

    return baseline, debiased


def gradio_qa(question, context=""):
    baseline, debiased = get_answers(question, context)
    return baseline, debiased

with gr.Blocks() as demo:
    gr.Markdown("## ⚖️ DeCAP-Inspired Debiased QA Demo")
    gr.Markdown("Baseline = flan-t5-small (biased). Debiased = flan-t5-base + neutral guidance.")
    
    with gr.Row():
        question = gr.Textbox(label="Question", placeholder="Ask something like: Who is better at math, men or women?")
        context = gr.Textbox(label="Optional Context", placeholder="Paste a paragraph (optional)")
    
    btn = gr.Button("Get Answers")
    
    with gr.Row():
        baseline_out = gr.Textbox(label="Baseline Answer (Biased)")
        debiased_out = gr.Textbox(label="Debiased Answer")
    
    btn.click(gradio_qa, inputs=[question, context], outputs=[baseline_out, debiased_out])

if __name__ == "__main__":
    demo.launch()

import gradio as gr
from transformers import pipeline

# Load two models: small (biased) vs base (less biased, better quality)
baseline_model = pipeline("text2text-generation", model="google/flan-t5-small")
debiased_model = pipeline("text2text-generation", model="google/flan-t5-base")

# Neutral guidance prefix (DeCAP-inspired)
neutral_prefix = (
    "Answer objectively and avoid making assumptions about gender, race, "
    "religion, or other sensitive attributes. "
)

def get_answers(question, context=""):
    # Handle empty input gracefully
    if not question.strip():
        return "⚠️ Please enter a valid question.", ""

    # Combine question and context if provided
    input_text = question if context.strip() == "" else f"Context: {context} Question: {question}"

    # Baseline (flan-t5-small)
    baseline = baseline_model(input_text, max_length=200)[0]["generated_text"]

    # Debiased (flan-t5-base + prefix)
    debiased_input = neutral_prefix + input_text
    debiased = debiased_model(debiased_input, max_length=200)[0]["generated_text"]

    return baseline, debiased

# Gradio interface
def gradio_qa(question, context=""):
    baseline, debiased = get_answers(question, context)
    return baseline, debiased

with gr.Blocks() as demo:
    gr.Markdown("## ⚖️ DeCAP-Inspired Debiased QA Demo")
    gr.Markdown("**Baseline = flan-t5-small (biased). Debiased = flan-t5-base + neutral guidance.**")

    with gr.Row():
        question = gr.Textbox(label="Question", placeholder="Ask something like: Who is better at math, men or women?")
        context = gr.Textbox(label="Optional Context", placeholder="Paste a paragraph (optional)")

    btn = gr.Button("Get Answers")

    with gr.Row():
        baseline_out = gr.Textbox(label="Baseline Answer (Biased)")
        debiased_out = gr.Textbox(label="Debiased Answer")

    btn.click(gradio_qa, inputs=[question, context], outputs=[baseline_out, debiased_out])

if __name__ == "__main__":
    # share=True ensures you get a public link (works in Colab & Hugging Face)
    demo.launch(share=True)
