from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.ML import ML

ml_bp = Blueprint("ml", __name__)
ml_api = Api(ml_bp)

class MLAPI(Resource):
    def get(self):
        id = request.args.get("id")
        ml = db.session.query(ML).get(id)
        if ml:
            return ml.to_dict()
        return {"message": "not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        parser.add_argument("password", required=True, type=str)
        args = parser.parse_args()
        ml = ML(args["username"], args["password"])

        try:
            db.session.add(ml)
            db.session.commit()
            return ml.to_dict(), 201
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)
        args = parser.parse_args()

        try:
            ml = db.session.query(ML).get(args["id"])
            if ml:
                if args["username"] is not None:
                    ml.username = args["username"]
                if args["password"] is not None:
                    ml.password = args["password"]
                db.session.commit()
                return ml.to_dict(), 200
            else:
                return {"message": "not found"}, 404
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            ml = db.session.query(ML).get(args["id"])
            if ml:
                db.session.delete(ml)
                db.session.commit()
                return ml.to_dict()
            else:
                return {"message": "not found"}, 404
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500


class MLListAPI(Resource):
    def get(self):
        mls = db.session.query(ML).all()
        return [ml.to_dict() for ml in mls]


ml_api.add_resource(MLAPI, "/ml")
ml_api.add_resource(MLListAPI, "/mlList")