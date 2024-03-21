from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from __init__ import db
from model.ML import ML

ml_bp = Blueprint("ml", __name__, url_prefix = '/api/ml')
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
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("socialclass", required=True, type=int)
        parser.add_argument("age", required=True, type=int)
        parser.add_argument("sex", required=True, type=str)
        parser.add_argument("siblings", required=True, type=int)
        parser.add_argument("family", required=True, type=int)
        parser.add_argument("fare", required=True, type=int)
        parser.add_argument("port", required=True, type=str)
        parser.add_argument("alone", required=True, type=bool)
        args = parser.parse_args()
        ml = ML(args["name"], args["socialclass"],args["age"],args["sex"],args["siblings"],args["family"], args["fare"], args["port"], args["alone"])

        try:
            db.session.add(ml)
            db.session.commit()
            return ml.to_dict(), 201
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("socialclass", required=True, type=int)
        parser.add_argument("age", required=True, type=int)
        parser.add_argument("sex", required=True, type=str)
        parser.add_argument("siblings", required=True, type=int)
        parser.add_argument("family", required=True, type=int)
        parser.add_argument("fare", required=True, type=int)
        parser.add_argument("port", required=True, type=str)
        parser.add_argument("alone", required=True, type=bool)
        args = parser.parse_args()

        try:
            ml = db.session.query(ML).get(args["id"])
            if ml:
                if args["name"] is not None:
                    ml.name = args["name"]
                if args["socialclass"] is not None:
                    ml.socialclass = args["socialclass"]
                if args["age"] is not None:
                    ml.age = args["age"]
                if args["sex"] is not None:
                    ml.sex = args["sex"]
                if args["siblings"] is not None:
                    ml.siblings = args["siblings"]
                if args["family"] is not None:
                    ml.family = args["family"]
                if args["fare"] is not None:
                    ml.fare = args["fare"]
                if args["port"] is not None:
                    ml.port = args["port"]
                if args["alone"] is not None:
                    ml.alone = args["alone"]
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


ml_api.add_resource(MLAPI, "/")
ml_api.add_resource(MLListAPI, "/mlList")