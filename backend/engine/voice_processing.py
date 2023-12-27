from .voiceapi import get_mp3_duration, concatenate_mp3_files, TexttoAudio
from .file_management import get_static_file_path

def timeline_process(news_list, voice_final_filelname):
    sex = ["Male", "Female"]
    age = ["18-30", "31-45", "46+"]
    voice_id = [0,1,2,3,4,5,6]
    index = 0
    filenames = []
    for sentence in news_list:
        print("AAA:", str(sentence))
        filename = get_static_file_path("work/" + str(index)+".mp3")
        TexttoAudio(str(sentence), sex[0], age[0], voice_id[4], filename)
        filenames.append(filename)
        index = index + 1
    
    durations = []
    timeline = 0
    concatenate_mp3_files(filenames, voice_final_filelname)
    for filename in filenames:
        duration = get_mp3_duration(filename)
        durations.append(duration)
        timeline = timeline + duration
    return durations, timeline