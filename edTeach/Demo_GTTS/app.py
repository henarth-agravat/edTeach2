from flask import Flask, request, render_template, jsonify
from moviepy.editor import *
import assemblyai as aai
import google.generativeai as genai
import os
import json

def extract_substring(input_string):
    start_index = input_string.find('{')  # Find the index of the first occurrence of '{'
    if start_index == -1:  # If '{' is not found, return None
        return None
    
    # Reverse the string after the first '{'
    reversed_string = input_string[start_index+1:][::-1]
    
    # Find the index of the first occurrence of '}' in the reversed string
    end_index_reversed = reversed_string.find('}')
    
    if end_index_reversed == -1:  # If '}' is not found after the first '{', return None
        return None
    
    # Calculate the index of '}' in the original string
    end_index = len(input_string) - end_index_reversed - 1
    
    return input_string[start_index+1:end_index]  # Extract the substring between the first '{' and the matching '}'

app = Flask(__name__)

# Set up AssemblyAI API key
aai.settings.api_key = "6d2abea1c464428c85222a2904087c46"

# Set up Gemini API
genai.configure(api_key="AIzaSyAqr4W3mKq7wwI9ihI9BqHWoabUDJwDb90")

# Set up the Gemini model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)
convo = model.start_chat(history=[])



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Check if file is present in the request
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']

    # Check if the file is a video
    if file.filename == '':
        return "No file selected", 400

    if file and allowed_file(file.filename):
        # Save the uploaded video
        video_path = "uploaded_video.mp4"
        file.save(video_path)

        # Load the video
        video = VideoFileClip(video_path)

        # Extract audio from video and save it as an mp3 file
        video.audio.write_audiofile("uploaded_audio.mp3")

        # Close the video file to release resources
        video.close()

        # Transcribe the audio file
        transcript_text = transcribe_audio("uploaded_audio.mp3")

        # Delete the temporary audio file
        os.remove("uploaded_audio.mp3")
        os.remove(video_path)

        # Pass the transcript text to Gemini API
        prompt = "paragraph:\n" + transcript_text + "\n\n" + "query:\nCould you generate a 5-MCQ quiz in JSON format based on the provided paragraph? Use 'q1' to 'q5' for questions and 'q1_a' to 'q1_d' for options of each question. After all questions, include a key named 'answers' containing the correct answers. Please ensure that the response consists of a single JSON object and adheres to the specified key naming convention."
        convo.send_message(prompt)
        response_text = convo.last.text

        response_text = extract_substring(response_text)

        if(response_text == None):
            response_text = "{" + "}"
        else:
            response_text = "{" + response_text + "}"
            
        json_data = json.loads(response_text)
        json_string = json.dumps(json_data)

        print(json_string)

        
        data = {
            "text": transcript_text,
            "quiz": json_string
        }

        # Return the response as JSON
        return jsonify(data)

    return "Invalid file format", 400

def transcribe_audio(audio_path):
    # Initialize the transcriber
    transcriber = aai.Transcriber()

    # Transcribe the audio file
    transcript = transcriber.transcribe(audio_path)

    # Get the transcript text
    transcript_text = transcript.text

    return transcript_text

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'mov', 'avi'}

if __name__ == '__main__':
    app.run(debug=True)