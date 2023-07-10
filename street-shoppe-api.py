from flask import Flask, jsonify, request  
from streetShoppeApiUtils import StreetShoppeApiUtils
import requests as req
import joblib
import pandas as pd

app = Flask(__name__)

## load scalers 
offer_eligibility_scaler = joblib.load('../models/offer_eligibility_scaler.bin')

## load models
offer_predictor = joblib.load('../models/offer_eligibility_model.joblib')
minimum_spend_predictor = joblib.load('../models/minimum_spend_model.joblib')

## Routes
@app.route('/')
def alive():
   return jsonify(message="Street Shoppe APIs running !", status="healthy")

@app.route('/getUserPurchaseHistory/<string:userName>')
def getUserPurchaseHistory(userName : str):
    authToken = StreetShoppeApiUtils.retrieveAccessToken(request)
    response = StreetShoppeApiUtils.responseBuilder(req.get(f'https://street-shoppe.firebaseio.com/orders/{userName}/orders.json'), "no data found", 404)
    return response['data'], response['status'] 


@app.route('/getUserStreekInfo', methods=['POST'])
def getUserOfferEligibility():
    requestBody = StreetShoppeApiUtils.getRequestInfo(requestBody=request.json)
    predicted_offer = offer_predictor.predict(offer_eligibility_scaler.transform(pd.DataFrame(columns=['purchase_total_amount','purchase_streek',"next_streek_purchase_amount"], data=[requestBody])))
    predicted_min_spend = minimum_spend_predictor.predict(pd.DataFrame(columns=["purchase_total_amount","next_streek_purchase_amount"], data=[requestBody]))
    return jsonify(offer_eligibility=predicted_offer[0], minimum_spend=int(predicted_min_spend[0]), purchase_total_amount= requestBody['purchase_total_amount'], purchase_streek = requestBody['purchase_streek'], next_streek_purchase_amount = requestBody['next_streek_purchase_amount']), 200



    
