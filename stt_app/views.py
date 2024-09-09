from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from pydub import AudioSegment
import speech_recognition as sr
import json

# Create your views here.
import logging

logger = logging.getLogger(__name__)

def speech_to_text(request):
    if request.method == "POST":
        recognizer = sr.Recognizer()
        try:
            audio_data = request.FILES.get('audio_data', None)
            logger.info(f"Received audio data: {audio_data}")

            if audio_data:
                # Your existing processing code here
                return JsonResponse({'success': True, 'transcript': 'Processed successfully'})

            logger.error("No audio data received")
            return JsonResponse({'success': False, 'message': 'No audio data received'})

        except sr.UnknownValueError:
            return JsonResponse({'success': False, 'message': 'Speech could not be understood.'})
        except sr.RequestError:
            return JsonResponse({'success': False, 'message': 'API request failed.'})
    return render(request, 'stt_app/index.html')




@csrf_exempt
def extract_lyrics(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)
        
        file_path = default_storage.save(audio_file.name, audio_file)
        audio_path = default_storage.path(file_path)

        # Convert audio file to WAV format if necessary
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.replace('.mp3', '.wav')
        audio.export(wav_path, format='wav')

        # Recognize speech from the audio file
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return JsonResponse({'lyrics': text})
            except sr.UnknownValueError:
                return JsonResponse({'lyrics': 'Could not understand audio.'})
            except sr.RequestError as e:
                return JsonResponse({'lyrics': f'Request failed; {e}'})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
