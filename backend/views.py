from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .engine.voiceapi import TexttoAudio
from .engine.gptapi import generate_news_response
from .engine.file_management import get_static_file_path, create_directory
from .engine.voice_processing import timeline_process
from .engine.ue_data_processing import ue_data
from .engine.video_processing import video_generation
from django.conf import settings
import requests
import os

UNREAL_ENGINE_ENDPOINT = settings.UNREAL_ENGINE_ENDPOINT
# Group filenames
work_filenames = {
    'work_dir': get_static_file_path("work"),
    'final_dir': get_static_file_path("final"),
    'voice_final_filelname': get_static_file_path("work/final_voice.mp3"),
    'work_video_filename': get_static_file_path("work/final_video.mp4"),
}

@csrf_exempt
def my_view(request):
    # Access and print POST data
    user_prompt = request.POST.get('prompt', None)
    # Create directories
    create_directory(work_filenames['work_dir'])
    create_directory(work_filenames['final_dir'])

    news_list = generate_news_response(user_prompt)
    durations, timeline = timeline_process(news_list, work_filenames['voice_final_filelname'])
    desired_count  = timeline *30
    ue_string = ue_data(durations)
    print(ue_string)
    # Prepare the data to be sent
    data_to_send = {'txt_data': ue_string}
    try:
        # Make the POST request to the Unreal Engine endpoint
        response = requests.post(UNREAL_ENGINE_ENDPOINT, json=data_to_send)
        response.raise_for_status()
        print("OK - Unreal Engine")
        # Initialize a variable to keep track of the count
        count = 0
        work_dir = work_filenames['work_dir']
        work_video_filename = work_filenames['work_video_filename']
        final_music_filename = work_filenames['final_music_filename']
        # Iterate through the files in the directory
        for filename in os.listdir(work_dir):
            # Check if the file is an image (you can adjust the condition based on your file types)
            if filename.lower().endswith(('.jpeg')):
                count += 1  # Increment the count for each image
                
                videourl = video_generation(work_dir,work_video_filename, final_music_filename)
                print(videourl)
                # Prepare data to send as JSON
                response_data = {"message": "Data received", "videoUrl": "https://www.youtube.com/watch?v=UrcU3ovXsLI"}
                return JsonResponse(response_data)
            # Check if the count has reached the desired threshold
            if count >= desired_count:
                print(f"Reached or exceeded {desired_count} images.")
                break  # Exit the loop when the threshold is reached
        # Check the response status and return appropriate JSON response
        return JsonResponse({'message': 'Data successfully sent to Unreal Engine'}, status=200)
    except requests.exceptions.RequestException as e:
        print("No - Unreal Engine")

    