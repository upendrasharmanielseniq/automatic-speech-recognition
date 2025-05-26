from openai import OpenAI
# from backend.config import AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT
from config import OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)
# openai.api_type = "azure"
# openai.api_version = "2023-07-01-preview"
# openai.api_base = AZURE_OPENAI_ENDPOINT
# openai.api_key = AZURE_OPENAI_KEY


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello, can you confirm the connection is working?"}
    ]
)
print(response.choices[0].message.content)



def build_prompt(chunks):
    full_text = " ".join([c.transcript for c in chunks])
    """
    Build the prompt for the OpenAI model.
    """
    return f"""
    You are a movie and shows expert. Given a transcript of a movie or show, predict the content of the movie from transcript text.
    The transcript is: {full_text}

    Response format:
    Title: <Movie or TV Show>
    Season: <Season number or N/A>
    Episode: <Episode number or N/A>
    Language: <Detected Language>
    """

def predict_content(transcript):
    """
    Predict the content of a transcription.
    """
    prompt = build_prompt(transcript.chunks)
    try:
        response = client.chat.completions.create(
            # engine=AZURE_OPENAI_DEPLOYMENT,
            model="gpt-3.5-turbo",  # the problem could be the key, the model, or the network
            messages=[
                {"role": "system", "content": "You are a streaming content classifier."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            # max_tokens=1000,
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0
        )
        return parse_response(response['choices'][0]['message']['content'])    
    except Exception as e:
        print("OpenAI API call failed:", e)
        return {"error": "Prediction failed", "details": str(e)}

    
def parse_response(text):
    lines = text.strip().split("\n")
    result = {}
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            result[key.lower()] = value.strip()
    return result