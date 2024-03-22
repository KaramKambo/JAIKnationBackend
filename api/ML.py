from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from __init__ import db
from model.ML import ML
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

ml_bp = Blueprint("ml", __name__, url_prefix = '/api/ml')
ml_api = Api(ml_bp)

class MLAPI(Resource):
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
        
        
        passenger = pd.DataFrame({
            'name': args["name"],
            'pclass': args["socialclass"],
            'sex': args["sex"],
            'age': args["age"],
            'sibsp': args["siblings"],
            'parch': args["family"],
            'fare': args["fare"],
            'embarked': args["port"]
            'alone': args["alone"]
        })
        
        passenger['sex'] = passenger['sex'].apply(lambda x: 1 if x == 'male' else 0)
        passenger['alone'] = passenger['alone'].apply(lambda x: 1 if x == True else 0)
        
        enc = OneHotEncoder(handle_unknown='ignore')

        onehot = enc.transform(passenger[['embarked']]).toarray()
        cols = ['embarked_' + val for val in enc.categories_[0]]
        passenger[cols] = pd.DataFrame(onehot, index=passenger.index)
        passenger.drop(['name'], axis=1, inplace=True)
        passenger.drop(['embarked'], axis=1, inplace=True)
        
        logreg = LogisticRegression()
        dead_proba, alive_proba = np.squeeze(logreg.predict_proba(passenger))
        
        ml = ML(args["name"], args["socialclass"],args["age"],args["sex"],args["siblings"],args["family"], args["fare"], args["port"], args["alone"], alive_proba)

        try:
            db.session.add(ml)
            db.session.commit()
            return ml.to_dict(), 201
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

class MLListAPI(Resource):
    def get(self):
        mls = db.session.query(ML).all()
        return [ml.to_dict() for ml in mls][-1]

ml_api.add_resource(MLAPI, "/")
ml_api.add_resource(MLListAPI, "/mlList")