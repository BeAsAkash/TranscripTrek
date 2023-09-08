from flask import Flask, request, jsonify
from flask_cors import CORS

from model import nlp_model

app = Flask(__name__)
CORS(app)


@app.route('/api/', methods=['GET'])
def respond():


    vid_url = request.args.get("video_url", None)

    if "youtube.com" in vid_url:

        try:
            video_id = vid_url.split("=")[1]

            try:
                video_id = video_id.split("&")[0]

            except:
                video_id = "False"

        except:
            video_id = "False"

    elif "youtu.be" in vid_url:

        try:
            video_id = vid_url.split("/")[3]

        except:

            video_id = "False"

    else:
        video_id = "False"

 

    body = {}
    data = {}


    if not video_id:
        data['message'] = "Failed"
        data['error'] = "no video id found, please provide valid video id."

    elif str(video_id) == "False":
        data['message'] = "Failed"
        data['error'] = "video id invalid, please provide valid video id."


    else:

        if nlp_model(video_id) == "0":
            data['message'] = "Failed"
            data['error'] = "API's not able to retrive Video Transcript."

        else:
            data['message'] = "Success"
            data['id'] = video_id
            data['original_txt_length'], data['final_summ_length'], data['eng_summary'], data['hind_summary'], data['guj_summary'] = nlp_model(
                video_id)

    body["data"] = data


    return buildResponse(body)



@app.route('/')
def index():

    body = {}
    body['message'] = "Success"
    body['data'] = "Welcome to YTS API."

    return buildResponse(body)


def buildResponse(body):



    response = jsonify(body)


    return response


if __name__ == '__main__':


    app.run(threaded=True)


