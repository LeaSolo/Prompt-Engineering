import os
import ssl
import httpx
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# עקיפת בעיות SSL שראינו בטרמינל שלך
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv(override=True) # override מוודא שהמפתח החדש ייקרא מהקובץ
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    # שימוש בלקוח HTTP גמיש יותר למקרה של חסימות רשת
    http_client=httpx.Client(verify=False)
)

def get_instructions():
    try:
        with open("prompts/type1.md", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "You are a CLI assistant. Return only the command."

def generate_cli(user_text):
    if not user_text: return ""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": get_instructions()},
                {"role": "user", "content": user_text}
            ],
            timeout=15.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"שגיאה: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🖥️ CLI Generator - New Key Test")
    input_box = gr.Textbox(label="הוראה אנושית")
    output_box = gr.Code(label="פקודת CLI", language="shell")
    submit_btn = gr.Button("צור פקודה", variant="primary")
    submit_btn.click(fn=generate_cli, inputs=input_box, outputs=output_box)

if __name__ == "__main__":
    demo.launch()