import os,gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
import logging
from bson.objectid import ObjectId

logging.basicConfig(level=logging.ERROR)

server = Flask(__name__)
server.debug = True

# server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo_video = PyMongo(server , uri="mongodb://host.minikube.internal:27017/videos")
mongo_mp3 = PyMongo(server , uri="mongodb://host.minikube.internal:27017/mp3s")

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login" , methods=["POST"])
def login():
    logging.error("Inside login")
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err

@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    if err:
        return err

    logging.error("Access : %s , Error : %s",access, err)

    access = json.loads(access)

    logging.error("Uploading :: %s" , {'access' : access})

    if access["admin"]:
        logging.error("Filest : %s :: len files :: %s" , request.files, len(request.files))
        if len(request.files) != 1:
            return "EXACTLY ONE FILE REQUIRED" , 400
        
        for k, file in request.files.items():
            err = util.upload(file, fs_videos, channel, access)

            if err:
                logging.error(err)
                return err
        return "SUCCESS" , 200
    else:
        return "NOT AUTHORIZED" , 401
    

@server.route("/download" , methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err

    logging.error("Access : %s , Error : %s",access, err)

    access = json.loads(access)

    logging.error("Uploading :: %s" , {'access' : access})


    if access["admin"]:
        fid_string = request.args.get("fid")
        
        if not fid_string:
            return "FID IS REQUIRED" , 400
        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out , download_name=f'{fid_string}.mp3')
        except Exception as err:
            logging.error(err)
            return "INTERNAL SERVER ERROR : GATEWAY : DOWNLOAD" , 500

    else:
        return "NOT AUTHORIZED" , 401



if __name__ == "__main__":
    print("Gateway started at 8080 : updated 23:33 : flush")
    server.run("0.0.0.0" , 8080, debug=True)