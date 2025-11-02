import gradio as gr
from src.rag.pipeline import answer_question


def run_gradio():
    with gr.Blocks(title="PaperMate") as demo:
        gr.Markdown("# 📄 PaperMate — Ask about research papers")
        question = gr.Textbox(
            label="Enter your question",
            placeholder="e.g. What is the NEMO paper about?",
            lines=15,
            max_lines=30,
        )
        output = gr.Textbox(label="Answer", lines=15, max_lines=30)

        btn = gr.Button("Ask")
        btn.click(fn=answer_question, inputs=question, outputs=output)

    demo.launch(server_name="0.0.0.0", server_port=8000)


if __name__ == "__main__":
    run_gradio()
