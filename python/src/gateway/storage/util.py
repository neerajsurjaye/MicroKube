import pika, json

import pika.channel
import pika.spec
import logging

logging.basicConfig(level=logging.ERROR)


def upload(f, fs, channel, access):
    logging.error("uploading file : %s" , f)
    try:
        fid = fs.put(f)
    except Exception as err:
        logging.error(err)
        return "INTERNAL SERVER ERROR at util" , 500
    
    message = {
        "video_fid" : str(fid),
        "mp3_fid" : None,
        "username" : access["username"]
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        print(err)
        fs.delete(fid)
        return "INTERNAL SERVER ERROR" , 500