from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy 

# create new flask app
app = Flask(__name__)
# wrap app in an api
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Sculpt our db model
class VideoModel(db.Model):
    # primary key true since every id is unique
    id = db.Column(db.Integer, primary_key = True)
    # nullable false since name should not be empty
    name = db.Column(db.String(100), nullable = False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)
    favorites = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes}, favorites = {favorites})"

# create database
# **YOU SHOULD ONLY DO THIS ONCE**
# db.create_all()

# create request parser object
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type = str, help = "Name of the video is required", required = True)
video_put_args.add_argument("views", type = int, help = "Please enter views on the video", required = True)
video_put_args.add_argument("likes", type = int, help = "Please enter likes on the video", required = True)
video_put_args.add_argument("favorites", type = int)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type = str, help = "Name of the video is required")
video_update_args.add_argument("views", type = int, help = "Please enter views on the video")
video_update_args.add_argument("likes", type = int, help = "Please enter likes on the video")
video_update_args.add_argument("favorites", type = int)


# # empty dict that stores videos
# videos = {}

# # function to abort if video_id does not exist
# def abort_video_no_exist(video_id):
#     if video_id not in videos:
#         abort(404, message = "Video id is not valid...")

# # function to abort if video_id already exists
# def abort_video_exists(video_id):
#     if video_id in videos:
#         abort(409, message = "Video already exists with that id...")
# 
# define how objects are serialized
resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'views' : fields.Integer,
    'likes' : fields.Integer,
    'favorites' : fields.Integer
}

class Video(Resource):
    # take return value and serialize with resource_fields
    # get request to return video id
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message = "Could not find video with that id...")
        return result

    # put request to create new video
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()

        result = VideoModel.query.filter_by(id = video_id).first()
        if result:
            abort(409, message = 'Video id taken...')

        video = VideoModel(id = video_id, name = args['name'], views = args['views'], likes = args['likes'], favorites = args['favorites'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message = "Video doesn't exist. Cannot update...")
        
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        if args['favorites']:
            result.favorites = args['favorites']
        
        db.session.commit()

        return result


    # delete request to delete a video
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message = "Video doesn't exist. Cannot delete...")

        db.session.delete(result)
        db.session.commit()
        return '', 204

# when sending requests, pass a video_id
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug = True)