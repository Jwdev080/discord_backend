import cv2
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import datetime
from django.conf import settings

def video_generation(work_dir,work_video_filename, final_music_filename):
    print("Generating the video...")
    # Rest of the code...
    fps = 30
    VIDEO_CODEC = 'libx264'
    AUDIO_CODEC = 'aac'
    # Get the list of image filenames
    image_files = sorted([os.path.join(work_dir, f) for f in os.listdir(work_dir) if f.endswith('.jpeg')])
    # Get the dimensions of the first image (assuming all images are the same size)
    first_image = cv2.imread(image_files[0])
    height, width, layers = first_image.shape
    # Initialize the video writer
    video_writer = cv2.VideoWriter(work_video_filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    # Write each frame to the video
    for image_file in image_files:
        frame = cv2.imread(image_file)
        video_writer.write(frame)
    # Release the video writer
    video_writer.release()
    # Load the video clip
    video_clip = VideoFileClip(work_video_filename)
    # Load the audio clip
    audio_clip = AudioFileClip(final_music_filename)
    # Set the audio of the video clip
    video_clip = video_clip.set_audio(audio_clip)
    print("Generating the final video...")
    # Write the final video with audio
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    final_videoname = f"final_output_{timestamp}.mp4"
    final_video_filename = os.path.join(settings.STATICFILES_DIRS[0], "final/", final_videoname)
    video_clip.write_videofile(final_video_filename, codec=VIDEO_CODEC, audio_codec=AUDIO_CODEC)
    video_url = os.path.join(settings.STATIC_URL, "final/", final_videoname)
    return video_url