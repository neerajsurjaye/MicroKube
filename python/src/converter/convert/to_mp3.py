import pika, json, tempfile, os
from bson.objectid import ObjectId
import pika.spec
from moviepy.video.io.VideoFileClip import VideoFileClip

def start(message, fs_video, fs_mp3s, channel):
    message = json.loads(message)

    # empty temp file
    tf = tempfile.NamedTemporaryFile()

    # video contet
    out = fs_video.get(ObjectId(message["video_fid"]))
    # Adds video content to empty file
    tf.write(out.read())
    tf.flush()

    # creates audio
    audio = VideoFileClip(tf.name).audio

    tf.close()

    # path to audio file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    # save file to mongo
    f = open(tf_path , "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    # removes temp file
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        # Removes the file from mongo if message cannot be published
        fs_mp3s.delete(fid)
        return "FAILED TO PUBLISH MESSAGE :: to_mp3"
    
