from datetime import date, timedelta, datetime

class StreetShoppeApiUtils:

    def retrieveAccessToken(request):
       return

    def responseBuilder(response, errorMessage, errorStatus):
       return {"data" : errorMessage, "status" : errorStatus} if response.text == "null" else {"data" : response.json(), "status" : 200}

    def getRequestInfo(requestBody):
        purchase_streek = requestBody['purchase_streek']
        purchases = [purchase for purchase in requestBody['purchase_history'] if ((datetime.strptime(purchase['invoice_date'], "%Y-%m-%d") - datetime.strptime(requestBody['last_streek_date'], "%Y-%m-%d")).days < 30)]
        purchase_total_amount = 0
        for invoice in purchases:
          purchase_total_amount += invoice['purchase_amount']
          if(purchase_total_amount >= ((purchase_streek + 1)*100)):
            purchase_streek += 1
            purchase_total_amount = 0
        return { "purchase_total_amount" : purchase_total_amount, "purchase_streek" : purchase_streek, "next_streek_purchase_amount" : ((purchase_streek + 1)*100) }
 