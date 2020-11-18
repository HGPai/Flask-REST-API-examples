from flask import Flask, request
from flask_restful import Resource, reqparse, abort, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app=app)


def abort_if_video_id_doesnot_exist(video_id):
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
        abort(404, 'Video does not exist!')


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    views = db.Column(db.Integer, nullable=True)
    likes = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"


# Note for VSCode users - pip install pylint-flask-sqlalchemy
# run this line only once so that a new database is not created every single time
# db.create_all()


video_args = reqparse.RequestParser()
video_args.add_argument(
    'name', type=str, help='Name of the video', required=True)
video_args.add_argument(
    'views', type=int, help='Views the video has received', required=True)
video_args.add_argument(
    'likes', type=int, help='Likes the video has received', required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    'name', type=str, help='Name of the video', required=True)
video_update_args.add_argument(
    'views', type=int, help='Views the video has received', required=True)
video_update_args.add_argument(
    'likes', type=int, help='Likes the video has received', required=True)


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='No such video found!')
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message='Video ID already taken!')

        video = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    # patch is a method for updating requests
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Video does not exist! cannot update')

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result

    def delete(self, video_id):
        abort_if_video_id_doesnot_exist(video_id)
        result = VideoModel.query.filter_by(id=video_id).first()
        db.session.delete(result)
        db.session.commit()
        return 'Deleted the video'


api.add_resource(Video, '/video/<int:video_id>')

if __name__ == "__main__":
    app.run(debug=True)
