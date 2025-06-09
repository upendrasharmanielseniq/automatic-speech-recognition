
from openai import AzureOpenAI
from schemas import TranscriptRequest
from config import (
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION
    )

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def build_prompt(chunks):
    full_text = " ".join([c.transcript for c in chunks])
    return f"""
  
    You are an expert in identifying TV shows and movies from dialogue transcripts.

    Your task is to analyze the following transcript and determine:
    1. **Title** of the show or movie (include year or series run if known).
    2. **Type**: Movie or TV Show.
    3. If it's a TV show, provide the **correct season and episode number** (or reply with "N/A" if not identifiable). Do **not** guess.
    4. Detect the **language** of the transcript.
    5. Provide a **confidence percentage** (0-100%).
    6. If confidence is **80% or higher**, return the prediction immediately.

    Use context clues such as character names, plot points, and dialogue. Avoid hallucination and only respond if you are reasonably certain.

    Transcript:
    \"\"\"
    {full_text}
    \"\"\"

    Respond in this format:
    Title: <Movie or TV Show title with year or series run>
    Type: <Movie or TV Show>
    Season: <Season number or "N/A"> # Omit if N/A
    Episode: <Episode number or "N/A"> # Omit if N/A
    Language: <Detected Language>
    Confidence: <Confidence score>
    """


def predict_content(transcript):
    """
    Predict the content of a transcription.
    """
    prompt = build_prompt(transcript.chunks)
    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a streaming content classifier."},
                {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
                )
        return parse_response(response.choices[0].message.content)
    except Exception as e:
        print("OpenAI API call failed:", e)
        return {"error": "Prediction failed", "details": str(e)}

def predict_content_chain(transcript):
    """
    Predict the content of a transcription.
    """
    
    try:

        full_transcript = " ".join([c.transcript for c in transcript.chunks])
        prompt = f"You are an expert in identifying TV shows and movies from dialogue transcripts. Identify only the name of the TV show or the movie as a single string from below transcript: \n\n{full_transcript}"
        # prompt = build_prompt_chain(transcript.chunks)
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a streaming content classifier."},
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        
        movie_show_name = response.choices[0].message.content.strip()
        print(f"MOVIE SHOW NAME: {movie_show_name}")

        prompt = f"You are an expert in summarizing transcripts from any language to English. Summarize the below transcript in English. \n\n{full_transcript}"
        # prompt = build_prompt_chain(transcript.chunks)
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        
        summary = response.choices[0].message.content.strip()

        print(f"SUMMARY: {summary}")

        prompt = f"""You are an expert in identifying the Episode Name of the TV shows given the name, summary of the transcript and the transcript. Search the internet for the episode name of the TV show {movie_show_name}. Only consider URLs that contain the keyword like {movie_show_name} episode list, {movie_show_name} season guide, {movie_show_name} episode summaries, \n\n {movie_show_name} episode where {summary}.
        Step-by-step: \n Formulate a search query. \n Filter results to include only URLs with "TV show", "Series", {movie_show_name} episode list, {movie_show_name} season guide, {movie_show_name} episode summaries". \n\n If {movie_show_name} is not a TV show return "N/A" else only Episode Name.\n\n Name is {movie_show_name} \n\n Summary is: {summary} \n\n Transcript is: {full_transcript} \n\n Only provide the episode name. Don't provide detailed explanation in the output"""

        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        episode_name = response.choices[0].message.content.strip()
        print(f"EPISODE NAME: {episode_name}")

        prompt = f"""You are an expert in identifying the season of the TV show given the name of the show and episode name. Google search the name of the TV show, name of the episode and provide the results and take the information from IMDB website as reliable. Verify the season number from reliable sources. Use the latest updated information. Think Step by Step. \n\n If {movie_show_name} is not a TV show return "N/A" else only Season Number.\n\n Name is {movie_show_name} \n\n \n\n \n\n Episode Name is: {episode_name} \n\n Provide the explanation as output"""

        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                # {"role": "system", "content": "You are a streaming content classifier."},
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        season = response.choices[0].message.content.strip()
        print(f"SEASON EXPLANATION: {season}")

        prompt = f"""You are an expert in verifying TV show and movie details. Given the TV show or movie name, Explanation for season number, Episode Name and Transcript, you need to provide a language of the transcript, episode number along with confidence for prediction. Google search the name of the TV show, name of the episode and provide the results and take the information on IMDB website as reliable where there are keywords like {episode_name}. Verify the episode number from reliable sources. Use the latest updated information. Think Step by step.
        Respond in the following format, adjust accordingly to movie or TV show:
        Title: <Movie or TV Show title with year if available or series run time>
        Type: <Movie or TV Show>
        Season: <Season number or "N/A"> Omit if N/A
        Episode: <Episode number or "N/A"> Omit if N/A
        Language: <Detected Language>
        Confidence: <Confidence percentage> n\n Name is {movie_show_name} \n\n Season number explanation is {season} \n\n Episode name is: {episode_name} \n\n Transcript is: {full_transcript}"""

        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a streaming content classifier."},
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        
        final_output = response.choices[0].message.content.strip()
        
        print(f"FINAL OUTPUT: \n {final_output}")
        
        return parse_response(final_output)
    except Exception as e:
        print("OpenAI API call failed:", e)
        return {"error": "Prediction failed", "details": str(e)}
    
def predict_content_chain_new(transcript):
    """
    Predict the content of a transcription.
    """
    
    try:

        full_transcript = " ".join([c.transcript for c in transcript.chunks])
        
        prompt = f"Identify the language of the transcript. Transcript:\n\n{full_transcript} \n\n Only give the language as output."
        # prompt = build_prompt_chain(transcript.chunks)
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        
        language = response.choices[0].message.content.strip()

        print(f"LANGUAGE: {language}")
        
        prompt = f"You are an expert in summarizing transcripts from any language to English. Summarize the below transcript in English. \n\n{full_transcript}"
        # prompt = build_prompt_chain(transcript.chunks)
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        
        summary = response.choices[0].message.content.strip()

        print(f"SUMMARY: {summary}")

        if language.upper() != "ENGLISH":
            prompt = f"You are an expert in translating transcripts from any language to English. Translate the below transcript in English. \n\n{full_transcript}"
            # prompt = build_prompt_chain(transcript.chunks)
            response = client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "user", "content": prompt}
                    ],
                    temperature=0,
                    max_tokens=500
                    )
            
            translation = response.choices[0].message.content.strip()

            print(f"TRANSLATION: {translation}")

        if language.upper() != "ENGLISH":
            prompt = f"""Given the transcript and its translation of the TV show or a movie, identify the key moments from the transcript and the translation. Make the list of key moments as the output. \n\n Transcript: {full_transcript} \n\n Translation: {translation}"""
        else:
            prompt = f"""Given the transcript of the TV show or a movie, identify the key moments from the transcript. Make the list of key moments as the output. \n\n Transcript: {full_transcript}"""

        response = client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "user", "content": prompt}
                    ],
                    temperature=0,
                    max_tokens=500
                    )
            
        key_moments = response.choices[0].message.content.strip()

        print(f"KEY MOMENTS: {key_moments}")

        if language.upper() != "ENGLISH":
            prompt = f"You are an expert in identifying TV shows and movies from dialogue transcripts, English summary, key moments and translation. Identify only the name of the TV show or the movie as a single string from below Below details. Transcript: \n\n{full_transcript} \n\n English Translation: \n\n{translation} \n\n Summary: \n\n{summary} \n\n Key Moments: {key_moments}"
        else:
            prompt = f"You are an expert in identifying TV shows and movies from dialogue transcripts, English summary and , key moments. Identify only the name of the TV show or the movie as a single string from below Below details. Transcript: \n\n{full_transcript} \n\n English Summary: \n\n{summary} \n\n Key Moments: {key_moments}"

        # prompt = build_prompt_chain(transcript.chunks)
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a streaming content classifier."},
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        
        movie_show_name = response.choices[0].message.content.strip()
        print(f"MOVIE SHOW NAME: {movie_show_name}")

        if language.upper() != "ENGLISH":
            # prompt = f"""You are an expert in identifying the Episode Name of the TV shows given the name, summary of the transcript, the transcript and its english translation. Search the internet for the episode name of the TV show {movie_show_name}. Only consider URLs that contain the keyword like {movie_show_name} episode list, {movie_show_name} season guide, {movie_show_name} episode summaries, \n\n {movie_show_name} episode where {summary}.
            # Step-by-step: \n Formulate a search query. \n Filter results to include only URLs with "TV show", "Series", {movie_show_name} episode list, {movie_show_name} season guide, {movie_show_name} episode summaries". \n\n If {movie_show_name} is not a TV show return "N/A" else only Episode Name.\n\n Name is {movie_show_name} \n\n Summary is: {summary} \n\n Transcript is: {full_transcript} \n\n Translation is: {translation} Only provide the episode name. Don't provide detailed explanation in the output"""
            prompt = f"""You are an expert in identifying the Episode Name of the TV shows given the name, summary of the transcript, key moments, transcript and its its english translation. Search the internet for the episode name of the TV show {movie_show_name}. Only consider URLs that contain the keyword like {movie_show_name} episode list, {movie_show_name} season guide, {movie_show_name} episode summaries, \n\n {movie_show_name} episode where {summary}.
            Step-by-step: \n Formulate a search query. \n Filter results to include only URLs with "TV show", "Series", {movie_show_name} episode list, {movie_show_name} season guide, {movie_show_name} episode summaries". Preferably look up the links in IMDB website. \n\n If {movie_show_name} is not a TV show return "N/A" else only Episode Name.\n\n Name is {movie_show_name} \n\n Summary is: {summary} \n\n Key Moments: {key_moments} \n\n Transcript: {full_transcript} \n\n English Translation of transcript is: {translation} \n\n Only provide the episode name. Don't provide detailed explanation in the output"""
        else:
            prompt = f"""You are an expert in identifying the Episode Name of the TV shows given the name, summary of the transcript, key moments and the transcript. Search the internet for the episode name of the TV show {movie_show_name}. Only consider URLs that contain the keyword like {movie_show_name} episode list, {movie_show_name} season guide, {movie_show_name} episode summaries, \n\n {movie_show_name} episode where {summary}.
            Step-by-step: \n Formulate a search query. \n Filter results to include only URLs with "TV show", "Series", {movie_show_name} episode list, {movie_show_name} season guide, {movie_show_name} episode summaries". Preferably look up the links in IMDB website \n\n If {movie_show_name} is not a TV show return "N/A" else only Episode Name.\n\n Name is {movie_show_name} \n\n Summary is: {summary} \n\n Key Moments: {key_moments} \n\n Transcript is: {full_transcript} \n\n Only provide the episode name. Don't provide detailed explanation in the output"""

        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        episode_name = response.choices[0].message.content.strip()
        print(f"EPISODE NAME: {episode_name}")

        prompt = f"""You are an expert in identifying the season of the TV show given the name of the show, key moments and episode name. Google search the name of the TV show, name of the episode and provide the results and take the information from IMDB website as reliable. Verify the season number from reliable sources. Use the latest updated information. Think Step by Step. \n\n If {movie_show_name} is not a TV show return "N/A" else only Season Number.\n\n Name is {movie_show_name} \n\n \n\n \n\n Episode Name is: {episode_name} \n\n Key Moments: {key_moments} \n\n Provide the explanation as output"""

        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                # {"role": "system", "content": "You are a streaming content classifier."},
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        season = response.choices[0].message.content.strip()
        print(f"SEASON EXPLANATION: {season}")

        if language.upper() != "ENGLISH":
            prompt = f"""You are an expert in verifying TV show and movie details. Given the TV show or movie name, Explanation for season number, Episode Name, Episode summary, english translation and Transcript, you need to provide the episode number along with confidence for prediction. Google search the name of the TV show, name of the episode and provide the results and take the information on IMDB website as reliable where there are keywords like {episode_name}. Verify the episode number from reliable sources. Use the latest updated information. Think Step by step.
            Respond in the following format, adjust accordingly to movie or TV show:
            Title: <Movie or TV Show title with year if available or series run time>
            Type: <Movie or TV Show>
            Season: <Season number or "N/A"> Omit if N/A
            Episode: <Episode number or "N/A"> Omit if N/A
            Language: {language}
            Confidence: <Confidence percentage> n\n Name is {movie_show_name} \n\n Season number explanation is {season} \n\n Episode name is: {episode_name} \n\n Episode Summary is: {summary} \n\n English Transcript Translation is: {translation} \n\n Transcript is: {full_transcript}"""
        else:
            prompt = f"""You are an expert in verifying TV show and movie details. Given the TV show or movie name, Explanation for season number, Episode Name, Episode summary and Transcript, you need to provide the episode number along with confidence for prediction. Google search the name of the TV show, name of the episode and provide the results and take the information on IMDB website as reliable where there are keywords like {episode_name}. Verify the episode number from reliable sources. Use the latest updated information. Think Step by step.
            Respond in the following format, adjust accordingly to movie or TV show:
            Title: <Movie or TV Show title with year if available or series run time>
            Type: <Movie or TV Show>
            Season: <Season number or "N/A"> Omit if N/A
            Episode: <Episode number or "N/A"> Omit if N/A
            Language: {language}
            Confidence: <Confidence percentage> n\n Name is {movie_show_name} \n\n Season number explanation is {season} \n\n Episode name is: {episode_name} \n\n Episode Summary is: {summary} \n\n Transcript is: {full_transcript}"""

        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a streaming content classifier."},
                {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
                )
        
        final_output = response.choices[0].message.content.strip()
        
        print(f"FINAL OUTPUT: \n {final_output}")
        
        return parse_response(final_output)
    except Exception as e:
        print("OpenAI API call failed:", e)
        return {"error": "Prediction failed", "details": str(e)}

def sliding_window_prediction(chunks,window_size=2000, step_size=400):
    predictions = []

    for i in range(0, len(chunks) - - window_size + 1, step_size):
        window = chunks[i:i + window_size]
        transcript_request = TranscriptRequest(chunks=window)
        prediction = predict_content_chain(transcript_request)

        print(f"Window {i}-{i+window_size}: {prediction}")

        if prediction.get("title") and prediction["title"].lower() != "unknown":
            if prediction.get("confidence", "0").isdigit() and int(prediction["confidence"]) >= 7:
                return prediction
            else:
                predictions.append(prediction)
    
    return predictions[0] if predictions else {"error": "No confident prediction in any window"}
    
def parse_response(text):
    lines = text.strip().split("\n")
    result = {}
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            result[key.lower()] = value.strip()
    return result