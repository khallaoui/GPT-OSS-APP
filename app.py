from openai import OpenAI
import gradio as gr

# Initialize the OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # <<< REMPLACEZ CECI
)

def respond(message, history):
    """Fonction pour envoyer la conversation à GPT-OSS-120B sur OpenRouter"""
    messages = [{"role": "system", "content": "Vous êtes un assistant santé utile et prudent. Fournissez des informations claires et recommandez toujours de consulter un médecin. Répondez dans la langue de l'utilisateur."}]
    for user_msg, assistant_msg in history:
        messages.extend([
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_msg}
        ])
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=messages,
        max_tokens=200,
    )
    return response.choices[0].message.content

# Créez l'interface de chat
demo = gr.ChatInterface(
    respond,
    title="Assistant Santé Harmony",
    description="Propulsé par GPT-OSS-120B via OpenRouter. **À des fins éducatives uniquement. Pas un avis médical.**"
)

# Lancez l'application
if __name__ == "__main__":
    demo.launch(share=True)  # Crée un lien public pour votre vidéo