from flask import Flask, request
from datetime import datetime
from flask_restful import reqparse, Resource, Api, abort

app = Flask(__name__)
api = Api(app=app)

video_args = reqparse.RequestParser()
video_args.add_argument(
    'name', type=str, help='Name of the video', required=True)
video_args.add_argument(
    'views', type=int, help='Views the video has received', required=True)
video_args.add_argument(
    'likes', type=int, help='Likes for the video', required=True)

videos = {1: {'name': 'Python programming', 'views': 150240, 'likes': 1000},
          2: {'name': 'Machine Learning', 'views': 120332, 'likes': 14500},
          3: {'name': 'Deep learning', 'views': 23044, 'likes': 476}
          }

# Function to check whether the video_id exists.
def if_video_not_exists(video_id):
    if video_id not in videos:
        abort(404, message='The requested video does not exist')


class Video(Resource):
    def get(self, video_id):
        if_video_not_exists(video_id)
        return videos[video_id]

    def delete(self, video_id):
        if_video_not_exists(video_id)
        del videos[video_id]
        return 'Deleted', 204

    def put(self, video_id):
        if_video_not_exists(video_id)
        return videos[video_id]


# A class to display all videos in the list and add a new video to the list
class VideoList(Resource):
    def get(self):
        return videos

    def post(self):
        args = video_args.parse_args()
        video_id = int(max(videos.keys())) + 1
        video = {'name': args['name'],
                 'views': args['views'], 'likes': args['likes']}
        videos[video_id] = video
        return videos[video_id], 201


api.add_resource(Video, '/video/<int:video_id>')
api.add_resource(VideoList, '/video', '/videos')

if __name__ == '__main__':
    # Use debug=True only in development environment
    app.run(debug=True)
