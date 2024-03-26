
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from amadeus import Client, ResponseError, Location
import amadeus
from amadeus import Client, ResponseError
import json,os,requests
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from django.shortcuts import render
import requests
import json,html,time
from datetime import datetime
from crmApp.models import PNR_TABLE, Price_manipulation_amount,Price_manipulation_percentage,MarkupControl

# Use the imported functions


# Create your views here.

CLIENT_ID = os.environ.get('AMADEUS_CLIENT_ID','')
CLIENT_SECRET_ID = os.environ.get('AMADEUS_CLIENT_SECRET','')


amadeus = Client(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET_ID
)

def flightbook(request):
    return render(request,'flight_form.html')



def flight_search_view(request):
    if request.method == "GET":
        try:
                # uncomment this is production-------------------------------------
            # origin_code = request.GET.get("originIataCode")
            # print(origin_code)
            # destination_code = request.GET.get("destinationIataCode")
            # departure_date = request.GET.get("departureDate")
            # # print(departure_date)
            return_date = request.GET.get("returnDate")
            print(return_date)
            # adults = request.GET.get("adults")
            # print(adults)
            # children = request.GET.get("children")
            # infants = request.GET.get("infants")
            # travelClass = request.GET.get("class")
            # origin_city = request.GET.get("originCity")
            # destination_city = request.GET.get("destinationCity")
            # currencyCode = request.GET.get("currency")
            # SymbolResponse = requests.get(f"http://127.0.0.1:8000/{currencyCode}").json()

            origin_code = 'GAU'
            print(origin_code)
            destination_code = 'BOM'
            departure_date = '2024-03-28'
            # print(departure_date)
            return_date = None
            adults = 1
            print(adults)
            children = 0
            infants = 0
            travelClass = 'ECONOMY'
            origin_city = "Guwahati"
            destination_city = "Mumbai"
            currencyCode = "INR"
            SymbolResponse = requests.get(f"http://127.0.0.1:8000/{currencyCode}").json()
            print(SymbolResponse["currency"])
            
            price = {}

            markup_control_amount = MarkupControl.objects.get(type='amount')
            activation_amount = markup_control_amount.activation
            if activation_amount is True:
                amountObj = Price_manipulation_amount.objects.all()
                for amount in amountObj:
                    price["amount"] = amount.price
            else:
                percentObj = Price_manipulation_percentage.objects.all()
                for percent in percentObj:
                    price["percentage"] = percent.price
                    
            # # if oneway trip
            if return_date is None:
            #     # uncomment this is production-------------------------------------
                response_departure = amadeus.shopping.flight_offers_search.get(
                    originLocationCode = origin_code,
                    destinationLocationCode = destination_code,
                    departureDate = departure_date,
                    # returnDate=return_date,
                    adults=adults,
                    children=children,
                    infants=infants,
                    travelClass=travelClass,
                    currencyCode=currencyCode
                ).data
                # context1 = {}
                # try:
                #     file_path = "output.txt"
                #     with open(file_path, "r") as file:
                #         context1=json.load(file)
                #     # print(context1)
                #     # return JsonResponse(context)
                #     # return HttpResponse("success")
                # except Exception as e:
                #     print(f"An error occurred: {e}")
                # response_departure=context1["flight_offers_departure"]
                validating_airline_codes_set = set()

                # for data in response_departure:
                #     for dats in data["validatingAirlineCodes"]:
                #         validating_airline_codes_set.add(dats)
                for data in response_departure:
                    for dats in data["itineraries"]:
                        for segment in dats["segments"]:
                            # print(segment["carrierCode"])
                            validating_airline_codes_set.add(segment["carrierCode"])

                # Convert the set to a list if needed
                validating_airline_codes_list = list(validating_airline_codes_set)
                airline_codes_string = ','.join(validating_airline_codes_list)
                airlines = amadeus.reference_data.airlines.get(airlineCodes=airline_codes_string).data
                # print(airlines)
                result_dict = {item['iataCode']: item["businessName"] for item in airlines}
                result_dict2 = {item['iataCode']: item.get('icaoCode', item['iataCode']) for item in airlines}

                context = {
                    "flight_offers_departure" : response_departure,
                    "origin":origin_city,
                    "destination":destination_city,
                    "airlines":result_dict,
                    "airlines2":result_dict2,
                    "symbol":SymbolResponse["currency"],
                    "markup":price
                    # "data" : response_departure,
                    # "flight_offers_return" : response_return.data,
                    # "show_loading_spinner": show_loading_spinner,
                }
                if context is not None:
                    messages.success(request,"done")
                return render(request,'result.html',{"data":json.dumps(context)})
                # uncomment this is production-------------------------------------
                    
                  # context = {}
                  # try:
                  #     file_path = "output.txt"
                  #     with open(file_path, "r") as file:
                  #         context=json.load(file)
                  #     # print(context["flight_offers_departure"])
                  #     # return JsonResponse(context)
                  #     # return HttpResponse("success")
                  # except Exception as e:
                  #     print(f"An error occurred: {e}")
                  
                  # # if context is not None:
                  # #     messages.success(request,"done")
                  # # return JsonResponse(context)
                  # context = {
                  #     "flight_offers_departure" : context["flight_offers_departure"],
                  #     "origin":origin_city,
                  #     "destination":destination_city,
                  # }
                  # return render(request, "result.html",{"data":json.dumps(context)})
            
                # return JsonResponse(context)
                # return HttpResponse(context)

            
            # if round trip
            else:
                # ==============================================================
                response_departure = amadeus.shopping.flight_offers_search.get(
                    originLocationCode = origin_code,
                    destinationLocationCode = destination_code,
                    departureDate = departure_date,
                    # returnDate=return_date,
                    adults=adults,
                    children=children,
                    infants=infants,
                    travelClass=travelClass,
                    currencyCode=currencyCode
                ).data
                response_return = amadeus.shopping.flight_offers_search.get(
                    originLocationCode = destination_code,
                    destinationLocationCode = origin_code,
                    departureDate = return_date,
                    # returnDate=return_date,
                    adults=adults,
                    children=children,
                    infants=infants,
                    travelClass=travelClass,
                    currencyCode=currencyCode
                ).data
   # # uncomment this is production-------------------------------------
                # file_path = "dummyFlights.txt"
                # context1 = {}
                # try:
                #     # Write context1 to a file (in this case, a JSON file)
                #     with open(file_path, "r") as file:
                #         context1=json.load(file)
                # except Exception as e:
                #     print(f"An error occurred: {e}")
                
                # # # uncomment this is production-------------------------------------
                # # # if context is not None:
                # # #     messages.success(request,"done")
                # # # return JsonResponse(context)
                # response_departure=context1["flight_offers_departure"]
                # response_return=context1["flight_offers_return"]
                
                validating_airline_codes_set = set()

                # for data in response_departure:
                #     for dats in data["validatingAirlineCodes"]:
                #         validating_airline_codes_set.add(dats)
                # for data in response_return:
                #     for dats in data["validatingAirlineCodes"]:
                #         validating_airline_codes_set.add(dats)
                for data in response_departure:
                    for dats in data["itineraries"]:
                        for segment in dats["segments"]:

                            validating_airline_codes_set.add(segment["carrierCode"])
                for data in response_return:
                    for dats in data["itineraries"]:
                        for segment in dats["segments"]:
                            validating_airline_codes_set.add(segment["carrierCode"])

                # Convert the set to a list if needed
                validating_airline_codes_list = list(validating_airline_codes_set)
                airline_codes_string = ','.join(validating_airline_codes_list)
                airlines = amadeus.reference_data.airlines.get(airlineCodes=airline_codes_string).data
                result_dict = {item['iataCode']: item['businessName'] for item in airlines}
                result_dict2 = {item['iataCode']: item.get('icaoCode', item['iataCode']) for item in airlines}

                context = {
                    # "flight_offers_departure" : response_departure.data,
                    # "flight_offers_return" : response_return.data,
                    "flight_offers_departure" : response_departure,
                    "flight_offers_return" : response_return,
                    "origin":origin_city,
                    "destination":destination_city,
                    "airlines":result_dict,
                    "airlines2":result_dict2,
                    "symbol":SymbolResponse["currency"],
                    "markup": price
                }

                return render(request, "result.html",{"data":json.dumps(context)})
                # uncomment this is production-------------------------------------
                # return HttpResponse("success")
        except RecursionError as error:
            print(error)
            return JsonResponse({"error": "Invalid request method 3"})
    else:
        return JsonResponse({"error": "Invalid request method 4"})
    


def multiCitySearch(request):
    if request.method == "POST":
        data = dict(request.POST)
        # print(data)
        # Initialize a list to store grouped trips as dictionaries
        grouped_trips_list = []
        travelerClass = data['class'][0]
        adults = int(data["adults"][0])
        children = int(data["children"][0])
        infants = int(data["infants"][0])
        travelerNo = int(data["travelerNo"][0])
        currencyCode = data['currency'][0]
        SymbolResponse = requests.get(f"http://127.0.0.1:8000/{currencyCode}").json()
        # Iterate through the keys of the data dictionary
        for key, value in data.items():
            # Check if the key starts with 'originCode' and extract the trip number
            if key.startswith('originCode'):
                trip_number = key[len('originCode'):]
                
                # Create a new trip dictionary for the current trip number
                trip_data = {
                    f'originCode': value[0],
                    f'originIataCode': data[f'originIataCode{trip_number}'][0],
                    f'originCity': data[f'originCity{trip_number}'][0],
                    f'destinationCode': data[f'destinationCode{trip_number}'][0],
                    f'destinationIataCode': data[f'destinationIataCode{trip_number}'][0],
                    f'destinationCity': data[f'destinationCity{trip_number}'][0],
                    f'departureDate': data[f'departureDate{trip_number}'][0],
                }
                
                # Append the trip data dictionary to the list
                grouped_trips_list.append(trip_data)

        # Print the resulting grouped_trips_list
        # print(grouped_trips_list)
        preparedData = []
        for data in grouped_trips_list:
            flight = {
                "sources": [
                "GDS"
                ],
                "searchCriteria": {
                    "flightFilters": {
                        "cabinRestrictions": [
                            {
                                "cabin": travelerClass ,
                                "coverage": "MOST_SEGMENTS",
                                "originDestinationIds":[
                                    "1"
                                    ]

                            }
                        ]
                    }
                },
                "currencyCode":currencyCode
            }
            origin_destinations = []
            trip_dict = {
                'id': '1',
                'originLocationCode': data['originCode'],
                'destinationLocationCode': data['destinationCode'],
                'departureDateTimeRange': {
                    'date': data['departureDate']
                }
            }
            origin_destinations.append(trip_dict)
            travelers = []
            for i in range(1, travelerNo + 1):
                if i <= adults:
                    print(f"{i} adult")
                    travlerAdult = {
                        "id": f"{i}",
                        "travelerType": "ADULT",
                        "fareOptions": [
                            "STANDARD"
                        ]
                    }
                    travelers.append(travlerAdult)
                elif i <= adults + children:
                    print(f"{i} children")
                    travlerChild = {
                        "id": f"{i}",
                        "travelerType": "CHILD",
                        "fareOptions": [
                            "STANDARD"
                        ]
                    }
                    travelers.append(travlerChild)
                else:
                    print(f"{i} infants")
                    travlerInfant = {
                        "id": f"{i}",
                        "travelerType": "SEATED_INFANT",
                        "fareOptions": [
                            "STANDARD"
                        ]
                    }
                    travelers.append(travlerInfant)
            flight["originDestinations"] = origin_destinations
            flight["travelers"] = travelers
            preparedData.append(flight)

        resultLists = []
        id = 1
        for body in preparedData:
            response = amadeus.shopping.flight_offers_search.post(body).data
            for fdata in response:
                fdata["id"] = f'{id}'
                id = id + 1
            # response = {"flight":"flight"}
            resultLists.append(response)
        # print(body)
        # file_path = "multiResult.txt"
        # with open(file_path, "r") as file:
        #     resultLists=json.load(file)

        # print(len(resultLists))
        for result in resultLists:
            for flightdata in result:
                for duration in flightdata["itineraries"]:
                    duration["duration"] = format_duration(duration["duration"])
                for segment in flightdata["itineraries"][0]["segments"]:
                    segment["departure"]["at"] = formatDateTime(segment["departure"]["at"])
                    segment["arrival"]["at"] = formatDateTime(segment["arrival"]["at"])
                # print(flightdata)

        # context = {
        #     "flightOffers": json.dumps(resultLists)
        # }
        validating_airline_codes_set = set()
        for flightDatas in resultLists:
            for offers in flightDatas:
                for dats in offers["itineraries"]:
                    for segment in dats["segments"]:
                        validating_airline_codes_set.add(segment["carrierCode"])

        # Convert the set to a list if needed
        validating_airline_codes_list = list(validating_airline_codes_set)
        airline_codes_string = ','.join(validating_airline_codes_list)
        airlines = amadeus.reference_data.airlines.get(airlineCodes=airline_codes_string).data
        result_dict = {item['iataCode']: item['businessName'] for item in airlines}
        result_dict2 = {item['iataCode']: item.get('icaoCode', item['iataCode']) for item in airlines}
        print(result_dict2)
        context = {
            "flightOffers": resultLists,
            "flightOffers1": json.dumps(resultLists),
            "symbol":SymbolResponse["currency"],
            "airlines2": result_dict2,
            "airlines3": json.dumps(result_dict2),
            "airlines":result_dict,
        }

        return render(request,"multi_result.html",context)


# Auto complete City and Airport Name
def origin_search(request):
    if request.method=='GET':
        try:
            data = amadeus.reference_data.locations.get(
                keyword=request.GET.get("term"), subType=Location.ANY).data
            context={
                "data": data
            }
            return JsonResponse(context)
        except Exception as e:
            print(f"Error: {e}")
            error_message = {"error": str(e)}
            return HttpResponse(json.dumps(error_message), content_type="application/json")


def destination_search(request):
    if request.method=='GET':
        try:
            data = amadeus.reference_data.locations.get(
                keyword=request.GET.get("term"), subType=Location.ANY).data
            context={
                "data": data
            }
            return JsonResponse(context)
        except Exception as e:
            print(f"Error: {e}")
            error_message = {"error": str(e)}
            return HttpResponse(json.dumps(error_message), content_type="application/json")

def customCredentials(request):
    json_data_param = request.GET.get('json_data')
    try:
        json_data = json.loads(json_data_param)
        data = json.dumps(json_data)
        # print("inside custom",data)
        context = {
            'json_data' : data,
        }
        return render(request, 'customer.html', context)
    except Exception as e:
        json_data = {}
        print(f"Error: {e}")
        error_message = {"error": str(e)}
        return HttpResponse(json.dumps(error_message), content_type="application/json")
    
def customCredentialsMulti(request):
    # json_data_param = request.GET.get('json_data')
    try:
        return render(request, 'multiCustomer.html')
    except Exception as e:
        json_data = {}
        print(f"Error: {e}")
        error_message = {"error": str(e)}
        return HttpResponse(json.dumps(error_message), content_type="application/json")



#search flight availability
def search_availability(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        # print("this is callede",json_data)
        city = set()
        try:
            
            if len(json_data["flight_offers_return"]) == 0:
                print("inside if ")
                # print(json_data["flight_offers_departure"][0])
                file_path = "response.txt"
                with open(file_path,"w") as file:
                    json.dump(json_data["flight_offers_departure"][0],file, indent=2)
                response = amadeus.shopping.flight_offers.pricing.post(json_data["flight_offers_departure"][0])
                response_departure = response.__dict__["result"]["data"]
                print(response.__dict__["result"]["data"]["bookingRequirements"])
                requirements = response.__dict__["result"]["data"]["bookingRequirements"]
                file_path = "response.txt"
                with open(file_path,"w") as file:
                    json.dump(json_data["flight_offers_departure"][0],file, indent=2)
                # body = {
                #     "data" : [
                #         response_departure["flightOffers"][0]
                #     ]
                # }
                # seatmaps_response = amadeus.shopping.seatmaps.post(body).data
                # print(len(seatmaps_response))
                context = {
                    "flightOffers": json_data["flight_offers_departure"][0],
                    "departureFlight" : response_departure["flightOffers"][0],
                    'bookingRequirements' : response.__dict__["result"]["data"]["bookingRequirements"],
                    # "seats" : seatmaps_response
                }
                return JsonResponse(context,safe=False)
            else:
                print("inside else")
                body = [
                    json_data["flight_offers_departure"][0],
                    json_data["flight_offers_return"][0]
                ]
                file_path = "response.txt"
                with open(file_path,"w") as file:
                    json.dump(body,file, indent=2)
                response_departure = amadeus.shopping.flight_offers.pricing.post(json_data["flight_offers_departure"][0]).data
                print("done1")
                id_of_departure_flight = int(json_data["flight_offers_departure"][0]["id"])
                json_data["flight_offers_return"][0]["id"] = f"{id_of_departure_flight+1}"
                response_return = amadeus.shopping.flight_offers.pricing.post(json_data["flight_offers_return"][0]).data
                for departureCode in response_departure["flightOffers"][0]["itineraries"][0]["segments"]:
                    city.add(departureCode["departure"]["iataCode"])
                    city.add(departureCode["arrival"]["iataCode"])
                for returnCode in response_return["flightOffers"][0]["itineraries"][0]["segments"]:
                    city.add(returnCode["departure"]["iataCode"])
                    city.add(returnCode["arrival"]["iataCode"])

                cityLists = list(city)
                json_data["flight_offers_departure"][0]["itineraries"].append(json_data["flight_offers_return"][0]["itineraries"][0]) # appending the itineraries of the return data to the departure data 
                
                for data_departure,data_return in zip(json_data["flight_offers_departure"][0]["travelerPricings"],json_data["flight_offers_return"][0]["travelerPricings"]):
                    for data_to_append in data_return["fareDetailsBySegment"]:
                        data_departure["fareDetailsBySegment"].append(data_to_append)

                # print(json_data["flight_offers_departure"][0])
                
                # response = amadeus.shopping.flight_offers.pricing.post(json_data["flight_offers_departure"][0]).data
                # body = {
                #     "data" : [
                #         response_departure["flightOffers"][0],
                #         response_return["flightOffers"][0]
                #     ]
                # }
                # seatmaps_response = amadeus.shopping.seatmaps.post(body).data
                # print(seatmaps_response)
                context = {
                    "flightOffers": json_data["flight_offers_departure"][0],
                    "departureFlight": response_departure["flightOffers"][0],
                    "returnFlight" : response_return["flightOffers"][0],
                    # "seats" : seatmaps_response
                }
                return JsonResponse(context,safe=False)
                # return HttpResponse("done")
        except ResponseError as e:
            # error = ClientError(e)
            print(e.response.result["errors"][0]["detail"])
            print(f"catch Error: {type(e)}")
            # error_message = {"error": str(e.response.result["errors"])}
            return JsonResponse(e.response.result["errors"],safe=False)
            



def seatmapView(request):
    if request.method == 'POST':
        json_data_param = request.GET.get('json_data')
        json_data = json.loads(request.body.decode('utf-8'))
        
        body={}
        try:
            if "returnFlight" in json_data:
                dept = json_data["departureFlight"]
                ret = json_data["returnFlight"]
                print(ret)
                id_of_departure_flight = int(dept["id"])
                ret["id"] = f"{id_of_departure_flight+1}"
                body = {
                    "data" : [
                        dept,
                        ret
                    ]
                }
                file_path = "testing.txt"

        # Open the file in write mode and write the JSON-formatted string
                with open(file_path, "w") as txt_file:
                    txt_file.write(json.dumps(body, indent=2))
            else:
                dept = json_data["departureFlight"]
                body={
                    "data" : [
                        dept,
                    ]
                }
            # Make the seatmaps request
            seatmaps_response = amadeus.shopping.seatmaps.post(body).data
            # file_path = 'seat.txt'

            # with open(file_path,"r") as file:
            #     seatmaps_response = json.loads(file.read())
                  
                        # body = body1['data']
            # print(seatmaps_response)
            # seatmaps_data = seatmaps_response
            # flight_data = json_data
            context = {
                "seats" : seatmaps_response,
            }
            return JsonResponse(context, safe=False)
            # return render(request,'seatmap.html')

        except ResponseError as e:
            # error = ClientError(e)
            print(e.response.result["errors"][0]["detail"])
            print(f"catch Error: {type(e)}")
            context = {
                "seats" : e.response.result["errors"]
            }
            # error_message = {"error": str(e.response.result["errors"])}
            return JsonResponse(context,safe=False)


def seatmapViewMulti(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        print(json_data)
        body={}
        try:
            body = {
                "data" : json_data
            }
            file_path = "testing.txt"

    # Open the file in write mode and write the JSON-formatted string
            with open(file_path, "w") as txt_file:
                txt_file.write(json.dumps(body, indent=2))
            # Make the seatmaps request
            seatmaps_response = amadeus.shopping.seatmaps.post(body).data
            # file_path = 'seat.txt'

            # with open(file_path,"r") as file:
            #     seatmaps_response = json.loads(file.read())
                  
                        # body = body1['data']
            # print(seatmaps_response)
            # seatmaps_data = seatmaps_response
            # flight_data = json_data
            context = {
                "seats" : seatmaps_response,
            }
            return JsonResponse(context, safe=False)
            # return render(request,'seatmap.html')

        except ResponseError as e:
            # error = ClientError(e)
            print(e.response.result["errors"][0]["detail"])
            print(f"catch Error: {type(e)}")
            context = {
                "seats" : e.response.result["errors"]
            }
            # error_message = {"error": str(e.response.result["errors"])}
            return JsonResponse(context,safe=False)


def seatMapTemplateView(request):
    # json_data_param = request.GET.get('json_data')
    # json_data = json.loads(json_data_param)
    # print(json_data)
    #     # print(json_data)
    # data = json.dumps(json_data)
    # # print(data)
    # print("called again")
    return render(request,'seatmap.html')

def create_orders(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        # print(json_data)
        flight_offer_data = json_data.get('flightOffer',{})
        selected_seats = json_data.get('selectedSeats', {})
        # print(selected_seats)
        if not selected_seats:
            print("empty")
        flightOffers=[]
        # flight_list = flight_offer_data["departureFlight"].append(flight_offer_data["returnFlight"])
        file_path = "my_file.txt"

        # Open the file in write mode and write the JSON-formatted string
        with open(file_path, "w") as txt_file:
            txt_file.write(json.dumps(flight_offer_data, indent=2))
        
        if flight_offer_data and 'returnFlight' in flight_offer_data:
            if not selected_seats:
                print("Seat selection is empty")
            else:
                for segment in selected_seats[0]["seatNumber"]["fareDetailsBySegment"]:
                # print(segment["segmentId"])
                # print(demo_segments[index])
                    for flight, seatnumber in zip(flight_offer_data["departureFlight"]["travelerPricings"], segment["additionalServices"]["chargeableSeatNumber"]):
                        # print(flight)
                        # print(flight["travelerId"])
                        for data in flight["fareDetailsBySegment"]:
                            
                            # if data['segmentId'] == segment["segmentId"]: #this will be uncommented during production
                            additional_services = {"additionalServices": {"chargeableSeatNumber":seatnumber}}
                            if data['segmentId'] == segment["segmentId"]:
                                data.update(additional_services)
                                # print(data)
                                break
                    # print(seatnumber)
                for segment in selected_seats[0]["seatNumber"]["fareDetailsBySegment"]:
                    # print(segment["segmentId"])
                    # print(demo_segments[index])
                    for flight, seatnumber in zip(flight_offer_data["returnFlight"]["travelerPricings"], segment["additionalServices"]["chargeableSeatNumber"]):
                        # print(flight)
                        # print(flight["travelerId"])
                        for data in flight["fareDetailsBySegment"]:
                            
                            # if data['segmentId'] == segment["segmentId"]: #this will be uncommented during production
                            additional_services = {"additionalServices": {"chargeableSeatNumber":seatnumber}}
                            if data['segmentId'] == segment["segmentId"]:
                                data.update(additional_services)
                                # print(data)
                                break
                        # print(seatnumber)
            departure_id = int(flight_offer_data["departureFlight"]["id"])
            flight_offer_data["returnFlight"]["id"] = f"{departure_id+1}"
            flightOffers=[
                    flight_offer_data["departureFlight"],
                    flight_offer_data["returnFlight"]
                ]
            print("inside if")
            file_path = "testing.txt"

            # Open the file in write mode and write the JSON-formatted string
            with open(file_path, "w") as txt_file:
                txt_file.write(json.dumps(flightOffers, indent=2))

        else:
            if not selected_seats:
                print("Seat selection is empty")
            else:
                for segment in selected_seats[0]["seatNumber"]["fareDetailsBySegment"]:
                # print(segment["segmentId"])
                # print(demo_segments[index])
                    for flight, seatnumber in zip(flight_offer_data["departureFlight"]["travelerPricings"], segment["additionalServices"]["chargeableSeatNumber"]):
                        # print(flight)
                        # print(flight["travelerId"])
                        for data in flight["fareDetailsBySegment"]:
                            
                            # if data['segmentId'] == segment["segmentId"]: #this will be uncommented during production
                            additional_services = {"additionalServices": {"chargeableSeatNumber":seatnumber}}
                            if data['segmentId'] == segment["segmentId"]:
                                data.update(additional_services)
                                # print(data)
                                break
                        # print(seatnumber)
            flightOffers=[
                flight_offer_data["departureFlight"]
            ]
        # print(flightOffers[0])
            file_path = "testing.txt"

            # Open the file in write mode and write the JSON-formatted string
            with open(file_path, "w") as txt_file:
                txt_file.write(json.dumps(flightOffers, indent=2))


        travelers = json_data.get('traveler')
        print(travelers)
        persons_list = travelers.get('persons', [])
        traveler_details = []

        for person in persons_list:
            dob = convert_date_format(person['dob'])
            # print(dob)
            formatted_person = {
                "id": str(len(traveler_details) + 1),  # You can adjust the ID logic as needed
                "dateOfBirth": dob,  # You might want to provide the actual date of birth
                "name": {"firstName": person['firstName'].upper(), "lastName": person['lastName'].upper()},
                "gender": person['sex'].upper(),  # Assuming 'MALE' or 'FEMALE' format
                "contact": {
                    "emailAddress": travelers['contact']['email'],  # Add the actual email address
                    "phones": [
                        {
                            "deviceType": "MOBILE",
                            "countryCallingCode": travelers['contact']['callingCode'],  # Add the actual country calling code
                            "number": travelers['contact']['phone']  # Add the actual phone number
                        }
                    ],
                }
            }
            if "passportNo" in person:
                expiry = convert_date_format(person["expiry"])
                documents=[
                    {
                        "documentType": "PASSPORT",
                        "number": person["passportNo"],
                        "expiryDate": expiry,
                        "issuanceCountry": person["issuance"],
                        "nationality": person["nationality"],
                        "holder": True
                    }
                ]
                formatted_person["documents"] = documents
            
            traveler_details.append(formatted_person)
        file_path = "my_file_tra.txt"

        # Open the file in write mode and write the JSON-formatted string
        with open(file_path, "w") as txt_file:
            txt_file.write(json.dumps(traveler_details, indent=2))
        # Print the result
        # print(traveler_details)
          
        # traveler = [{
        #     "id": "1",
        #     "dateOfBirth": "1982-01-16",
        #     "name": {"firstName": "JORGE", "lastName": "GONZALES"},
        #     "gender": "MALE",
        #     "contact": {
        #         "emailAddress": "jorge.gonzales833@telefonica.es",
        #         "phones": [
        #             {
        #                 "deviceType": "MOBILE",
        #                 "countryCallingCode": "34",
        #                 "number": "480080076",
        #             }
        #         ],
        #     },
        #     "documents": [
        #         {
        #             "documentType": "PASSPORT",
        #             "birthPlace": "Madrid",
        #             "issuanceLocation": "Madrid",
        #             "issuanceDate": "2015-04-14",
        #             "number": "00000000",
        #             "expiryDate": "2025-04-14",
        #             "issuanceCountry": "ES",
        #             "validityCountry": "ES",
        #             "nationality": "ES",
        #             "holder": True,
        #         }
        #     ],
        # },
        # {
        #     "id": "2",
        #     "dateOfBirth": "1982-01-16",
        #     "name": {"firstName": "JORGE", "lastName": "GONZALES"},
        #     "gender": "MALE",
        #     "contact": {
        #         "emailAddress": "jorge.gonzales833@telefonica.es",
        #         "phones": [
        #             {
        #                 "deviceType": "MOBILE",
        #                 "countryCallingCode": "34",
        #                 "number": "480080076",
        #             }
        #         ],
        #     },
        #     "documents": [
        #         {
        #             "documentType": "PASSPORT",
        #             "birthPlace": "Madrid",
        #             "issuanceLocation": "Madrid",
        #             "issuanceDate": "2015-04-14",
        #             "number": "00000000",
        #             "expiryDate": "2025-04-14",
        #             "issuanceCountry": "ES",
        #             "validityCountry": "ES",
        #             "nationality": "ES",
        #             "holder": True,
        #         }
        #     ],
        # }]
        try:
            response = {}
            print("hi")
            # print(flightOffers)
            flight_price = amadeus.shopping.flight_offers.pricing.post(flightOffers)
            flight_price_confirmed = amadeus.shopping.flight_offers.pricing.post(flightOffers).data
            print(flight_price_confirmed)
            file_path="test3.txt"
            with open(file_path,"w") as file:
                file.write(json.dumps(flight_price_confirmed["flightOffers"],indent=2))
            if "warnings" in flight_price.__dict__["result"]:
                print("warning present")
                order_response = amadeus.booking.flight_orders.post(flight_price_confirmed["flightOffers"],traveler_details).data # to be uncommented when working with real data
                print("nothing happend")
            else:
                print("no warnings")
                order_response = amadeus.booking.flight_orders.post(flight_price_confirmed["flightOffers"],traveler_details).data # to be uncommented when working with real data
                print("nothing happened")
            # body = flight_price_confirmed['flightOffers']
            response=order_response
            total_base_price = 0
            currency = ''
            for data in response["flightOffers"]:
                print(data["price"]["grandTotal"])
                print(data["price"]["currency"])
          
                currency = data["price"]["currency"]
                base_price = float(data["price"]["grandTotal"])
                total_base_price += base_price
                print(f"Base Price: {base_price} {data['price']['currency']}")

            # print(f"Total Base Price: {total_base_price} {response['flightOffers'][0]['price']['currency']}")
            total_base_price = markupCalculator(total_base_price)
            print(f"Total Base Price: {total_base_price} {response['flightOffers'][0]['price']['currency']}")
            SymbolResponse = requests.get(f"http://127.0.0.1:8000/{currency}").json()
            print(SymbolResponse["currency"])
            baggage_fee = 200
            seat_selection_fee = 50
            airport_tax = 20
            security_fee = 30
            asap_fee = 50
            other_fees = 100

            # print(response["flightOffers"])

            context = {
                'user_Address':travelers['address'],
                'flight_order_data': response,
                'currency': currency,
                'total_base': total_base_price,
                'baggage_fee': baggage_fee,
                'seat_selection_fee':seat_selection_fee,
                'airport_tax': airport_tax,
                'security_fee': security_fee,
                'agency_fee': asap_fee,
                'other_fees': 100,
                'symbol': SymbolResponse["currency"],
            }

            pnr_data = PNR_TABLE.objects.create(email=travelers['contact']['email'],phone=travelers['contact']['phone'],address=travelers["address"]["address"],zip=travelers["address"]["zip"],city=travelers["address"]["city"],ref_id=response["id"])
            # pnr_data = PNR_TABLE.objects.create(email=travelers['contact']['email'],phone=travelers['contact']['phone'],address=travelers["address"]["address"],zip=travelers["address"]["zip"],city=travelers["address"]["city"],ref_id=response["id"])
            # pnr_data = PNR_TABLE.objects.create(email=travelers['contact']['email'],phone=travelers['contact']['phone'],ref_id=response["id"],address=travelers['address'],zipcode=travelers['zip'],city=travelers['city'])
            # print(response["id"])
            # response = amadeus.booking.flight_orders.post(flightOffers,traveler_details).data # to be uncommented when working with real data
            # return JsonResponse("done")
            # response = {
            #           "type": "flight-order",
                      
            #           "id": "eJzTd9f3cTU1MfcDAAp%2BAiU%3D",
            #           "queuingOfficeId": "NCE4D31SB",
            #           "associatedRecords": [
            #             {
            #               "reference": "LE547N",
            #               "creationDate": "2023-12-09T08:49:00.000",
            #               "originSystemCode": "GDS",
            #               "flightOfferId": "1"
            #             }
            #           ],
            #           "flightOffers": [
            #             {
            #               "type": "flight-offer",
            #               "id": "1",
            #               "source": "GDS",
            #               "nonHomogeneous": False,
            #               "lastTicketingDate": "2023-12-09",
            #               "itineraries": [
            #                 {
            #                   "segments": [
            #                     {
            #                       "departure": {
            #                         "iataCode": "GAU",
            #                         "at": "2023-12-15T18:15:00"
            #                       },
            #                       "arrival": {
            #                         "iataCode": "DEL",
            #                         "terminal": "3",
            #                         "at": "2023-12-15T20:45:00"
            #                       },
            #                       "carrierCode": "UK",
            #                       "number": "722",
            #                       "aircraft": {
            #                         "code": "320"
            #                       },
            #                       "duration": "PT2H30M",
            #                       "id": "40",
            #                       "numberOfStops": 0,
            #                       "co2Emissions": [
            #                         {
            #                           "weight": 110,
            #                           "weightUnit": "KG",
            #                           "cabin": "ECONOMY"
            #                         }
            #                       ]
            #                     },
            #                     {
            #                       "departure": {
            #                         "iataCode": "DEL",
            #                         "terminal": "3",
            #                         "at": "2023-12-15T21:40:00"
            #                       },
            #                       "arrival": {
            #                         "iataCode": "BOM",
            #                         "terminal": "2",
            #                         "at": "2023-12-15T23:50:00"
            #                       },
            #                       "carrierCode": "UK",
            #                       "number": "981",
            #                       "aircraft": {
            #                         "code": "320"
            #                       },
            #                       "duration": "PT2H10M",
            #                       "id": "41",
            #                       "numberOfStops": 0,
            #                       "co2Emissions": [
            #                         {
            #                           "weight": 92,
            #                           "weightUnit": "KG",
            #                           "cabin": "ECONOMY"
            #                         }
            #                       ]
            #                     }
            #                   ]
            #                 }
            #               ],
            #               "price": {
            #                 "currency": "EUR",
            #                 "total": "202.86",
            #                 "base": "182.00",
            #                 "fees": [
            #                   {
            #                     "amount": "0.00",
            #                     "type": "TICKETING"
            #                   },
            #                   {
            #                     "amount": "0.00",
            #                     "type": "SUPPLIER"
            #                   },
            #                   {
            #                     "amount": "0.00",
            #                     "type": "FORM_OF_PAYMENT"
            #                   }
            #                 ],
            #                 "grandTotal": "205.06",
            #                 "billingCurrency": "EUR",
            #                 "additionalServices": [
            #                   {
            #                     "amount": "2.20",
            #                     "type": "SEATS"
            #                   }
            #                 ]
            #               },
            #               "pricingOptions": {
            #                 "fareType": [
            #                   "PUBLISHED"
            #                 ],
            #                 "includedCheckedBagsOnly": True
            #               },
            #               "validatingAirlineCodes": [
            #                 "UK"
            #               ],
            #               "travelerPricings": [
            #                 {
            #                   "travelerId": "1",
            #                   "fareOption": "STANDARD",
            #                   "travelerType": "ADULT",
            #                   "price": {
            #                     "currency": "EUR",
            #                     "total": "101.43",
            #                     "base": "91.00",
            #                     "taxes": [
            #                       {
            #                         "amount": "5.53",
            #                         "code": "IN"
            #                       },
            #                       {
            #                         "amount": "2.59",
            #                         "code": "P2"
            #                       },
            #                       {
            #                         "amount": "2.31",
            #                         "code": "YR"
            #                       }
            #                     ],
            #                     "refundableTaxes": "10.43"
            #                   },
            #                   "fareDetailsBySegment": [
            #                     {
            #                       "segmentId": "40",
            #                       "cabin": "ECONOMY",
            #                       "fareBasis": "VL1PTFYS",
            #                       "brandedFare": "ECOYS",
            #                       "class": "V",
            #                       "includedCheckedBags": {
            #                         "weight": 15,
            #                         "weightUnit": "KG"
            #                       },
            #                       "additionalServices": {
            #                         "chargeableSeatNumber": "20A"
            #                       }
            #                     },
            #                     {
            #                       "segmentId": "41",
            #                       "cabin": "ECONOMY",
            #                       "fareBasis": "VL1PTFYS",
            #                       "brandedFare": "ECOYS",
            #                       "class": "V",
            #                       "includedCheckedBags": {
            #                         "weight": 15,
            #                         "weightUnit": "KG"
            #                       },
            #                       "additionalServices": {
            #                         "chargeableSeatNumber": "28D"
            #                       }
            #                     }
            #                   ]
            #                 },
            #                 {
            #                   "travelerId": "2",
            #                   "fareOption": "STANDARD",
            #                   "travelerType": "ADULT",
            #                   "price": {
            #                     "currency": "EUR",
            #                     "total": "101.43",
            #                     "base": "91.00",
            #                     "taxes": [
            #                       {
            #                         "amount": "5.53",
            #                         "code": "IN"
            #                       },
            #                       {
            #                         "amount": "2.59",
            #                         "code": "P2"
            #                       },
            #                       {
            #                         "amount": "2.31",
            #                         "code": "YR"
            #                       }
            #                     ],
            #                     "refundableTaxes": "10.43"
            #                   },
            #                   "fareDetailsBySegment": [
            #                     {
            #                       "segmentId": "40",
            #                       "cabin": "ECONOMY",
            #                       "fareBasis": "VL1PTFYS",
            #                       "brandedFare": "ECOYS",
            #                       "class": "V",
            #                       "includedCheckedBags": {
            #                         "weight": 15,
            #                         "weightUnit": "KG"
            #                       },
            #                       "additionalServices": {
            #                         "chargeableSeatNumber": "18B"
            #                       }
            #                     },
            #                     {
            #                       "segmentId": "41",
            #                       "cabin": "ECONOMY",
            #                       "fareBasis": "VL1PTFYS",
            #                       "brandedFare": "ECOYS",
            #                       "class": "V",
            #                       "includedCheckedBags": {
            #                         "weight": 15,
            #                         "weightUnit": "KG"
            #                       },
            #                       "additionalServices": {
            #                         "chargeableSeatNumber": "24E"
            #                       }
            #                     }
            #                   ]
            #                 }
            #               ]
            #             }
            #           ],
            #           "travelers": [
            #             {
            #               "id": "1",
            #               "dateOfBirth": "1982-01-16",
            #               "gender": "MALE",
            #               "name": {
            #                 "firstName": "JORGE",
            #                 "lastName": "GONZALES"
            #               },
            #               "documents": [
            #                 {
            #                   "number": "00000000",
            #                   "issuanceDate": "2015-04-14",
            #                   "expiryDate": "2025-04-14",
            #                   "issuanceCountry": "ES",
            #                   "issuanceLocation": "Madrid",
            #                   "nationality": "ES",
            #                   "birthPlace": "Madrid",
            #                   "documentType": "PASSPORT",
            #                   "holder": True
            #                 }
            #               ],
            #               "contact": {
            #                 "purpose": "STANDARD",
            #                 "phones": [
            #                   {
            #                     "deviceType": "MOBILE",
            #                     "countryCallingCode": "34",
            #                     "number": "480080076"
            #                   }
            #                 ],
            #                 "emailAddress": "jorge.gonzales833@telefonica.es"
            #               }
            #             },
            #             {
            #               "id": "2",
            #               "dateOfBirth": "1982-01-16",
            #               "gender": "MALE",
            #               "name": {
            #                 "firstName": "JORGE",
            #                 "lastName": "GONZALES"
            #               },
            #               "documents": [
            #                 {
            #                   "number": "00000000",
            #                   "issuanceDate": "2015-04-14",
            #                   "expiryDate": "2025-04-14",
            #                   "issuanceCountry": "ES",
            #                   "issuanceLocation": "Madrid",
            #                   "nationality": "ES",
            #                   "birthPlace": "Madrid",
            #                   "documentType": "PASSPORT",
            #                   "holder": True
            #                 }
            #               ],
            #               "contact": {
            #                 "purpose": "STANDARD",
            #                 "phones": [
            #                   {
            #                     "deviceType": "MOBILE",
            #                     "countryCallingCode": "34",
            #                     "number": "480080076"
            #                   }
            #                 ],
            #                 "emailAddress": "jorge.gonzales833@telefonica.es"
            #               }
            #             }
            #           ],
            #           "remarks": {
            #             "general": [
            #               {
            #                 "subType": "GENERAL_MISCELLANEOUS",
            #                 "text": "ONLINE BOOKING FROM INCREIBLE VIAJES"
            #               }
            #             ]
            #           },
            #           "ticketingAgreement": {
            #             "option": "DELAY_TO_CANCEL",
            #             "delay": "6D"
            #           },
            #           "automatedProcess": [
            #             {
            #               "code": "IMMEDIATE",
            #               "queue": {
            #                 "number": "0",
            #                 "category": "0"
            #               },
            #               "officeId": "NCE4D31SB"
            #             }
            #           ],
            #           "contacts": [
            #             {
            #               "addresseeName": {
            #                 "firstName": "PABLO RODRIGUEZ"
            #               },
            #               "address": {
            #                 "lines": [
            #                   "Calle Prado, 16"
            #                 ],
            #                 "postalCode": "28014",
            #                 "countryCode": "ES",
            #                 "cityName": "Madrid"
            #               },
            #               "purpose": "STANDARD",
            #               "phones": [
            #                 {
            #                   "deviceType": "LANDLINE",
            #                   "countryCallingCode": "34",
            #                   "number": "480080071"
            #                 },
            #                 {
            #                   "deviceType": "MOBILE",
            #                   "countryCallingCode": "33",
            #                   "number": "480080072"
            #                 }
            #               ],
            #               "companyName": "INCREIBLE VIAJES",
            #               "emailAddress": "support@increibleviajes.es"
            #             }
            #           ]
            #         }
            
            return JsonResponse(context,safe=False)
        except ResponseError as e:
            # error = ClientError(e)
            print(e.response.result["errors"][0]["detail"])
            # error_message = {"error": str(e.response.result["errors"])}
            return JsonResponse(e.response.result["errors"],safe=False)
        



def create_orders_multi(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        # print(json_data)
        flight_offer_data = json_data.get('flightOffer',{})
        selected_seats = json_data.get('selectedSeats', {})
        # print(selected_seats)
        print(flight_offer_data)
        if not selected_seats:
            print("empty")
        flightOffers=[]
        # flight_list = flight_offer_data["departureFlight"].append(flight_offer_data["returnFlight"])
        file_path = "my_file.txt"

        # Open the file in write mode and write the JSON-formatted string
        with open(file_path, "w") as txt_file:
            txt_file.write(json.dumps(flight_offer_data, indent=2))
        if not selected_seats:
            print("Seat selection is empty")
        else:
            for flights in flight_offer_data:
                    for segment in selected_seats[0]["seatNumber"]["fareDetailsBySegment"]:
                    # print(segment["segmentId"])
                    # print(demo_segments[index])
                        for flight, seatnumber in zip(flights["travelerPricings"], segment["additionalServices"]["chargeableSeatNumber"]):
                            # print(flight)
                            # print(flight["travelerId"])
                            for data in flight["fareDetailsBySegment"]:
                                
                                # if data['segmentId'] == segment["segmentId"]: #this will be uncommented during production
                                additional_services = {"additionalServices": {"chargeableSeatNumber":seatnumber}}
                                if data['segmentId'] == segment["segmentId"]:
                                    data.update(additional_services)
                                    # print(data)
                                    break
                            # print(seatnumber)

        # flightOffers=[
        #     flight_offer_data["departureFlight"]
        # ]
        # # print(flightOffers[0])
        file_path = "testing.txt"

        # Open the file in write mode and write the JSON-formatted string
        with open(file_path, "w") as txt_file:
            txt_file.write(json.dumps(flight_offer_data, indent=2))


        travelers = json_data.get('traveler')
        print(travelers)
        persons_list = travelers.get('persons', [])
        traveler_details = []

        for person in persons_list:
            dob = convert_date_format(person['dob'])
            # print(dob)
            formatted_person = {
                "id": str(len(traveler_details) + 1),  # You can adjust the ID logic as needed
                "dateOfBirth": dob,  # You might want to provide the actual date of birth
                "name": {"firstName": person['firstName'].upper(), "lastName": person['lastName'].upper()},
                "gender": person['sex'].upper(),  # Assuming 'MALE' or 'FEMALE' format
                "contact": {
                    "emailAddress": travelers['contact']['email'],  # Add the actual email address
                    "phones": [
                        {
                            "deviceType": "MOBILE",
                            "countryCallingCode": travelers['contact']['callingCode'],  # Add the actual country calling code
                            "number": travelers['contact']['phone']  # Add the actual phone number
                        }
                    ],
                }
            }
            if "passportNo" in person:
                expiry = convert_date_format(person["expiry"])
                documents=[
                    {
                        "documentType": "PASSPORT",
                        "number": person["passportNo"],
                        "expiryDate": expiry,
                        "issuanceCountry": person["issuance"],
                        "nationality": person["nationality"],
                        "holder": True
                    }
                ]
                formatted_person["documents"] = documents
            
            traveler_details.append(formatted_person)
        file_path = "my_file_tra.txt"

        # Open the file in write mode and write the JSON-formatted string
        print(traveler_details)
        with open(file_path, "w") as txt_file:
            txt_file.write(json.dumps(traveler_details, indent=2))
        # Print the result
        # print(traveler_details)
          
        # traveler = [{
        #     "id": "1",
        #     "dateOfBirth": "1982-01-16",
        #     "name": {"firstName": "JORGE", "lastName": "GONZALES"},
        #     "gender": "MALE",
        #     "contact": {
        #         "emailAddress": "jorge.gonzales833@telefonica.es",
        #         "phones": [
        #             {
        #                 "deviceType": "MOBILE",
        #                 "countryCallingCode": "34",
        #                 "number": "480080076",
        #             }
        #         ],
        #     },
        #     "documents": [
        #         {
        #             "documentType": "PASSPORT",
        #             "birthPlace": "Madrid",
        #             "issuanceLocation": "Madrid",
        #             "issuanceDate": "2015-04-14",
        #             "number": "00000000",
        #             "expiryDate": "2025-04-14",
        #             "issuanceCountry": "ES",
        #             "validityCountry": "ES",
        #             "nationality": "ES",
        #             "holder": True,
        #         }
        #     ],
        # },
        # {
        #     "id": "2",
        #     "dateOfBirth": "1982-01-16",
        #     "name": {"firstName": "JORGE", "lastName": "GONZALES"},
        #     "gender": "MALE",
        #     "contact": {
        #         "emailAddress": "jorge.gonzales833@telefonica.es",
        #         "phones": [
        #             {
        #                 "deviceType": "MOBILE",
        #                 "countryCallingCode": "34",
        #                 "number": "480080076",
        #             }
        #         ],
        #     },
        #     "documents": [
        #         {
        #             "documentType": "PASSPORT",
        #             "birthPlace": "Madrid",
        #             "issuanceLocation": "Madrid",
        #             "issuanceDate": "2015-04-14",
        #             "number": "00000000",
        #             "expiryDate": "2025-04-14",
        #             "issuanceCountry": "ES",
        #             "validityCountry": "ES",
        #             "nationality": "ES",
        #             "holder": True,
        #         }
        #     ],
        # }]
        try:
            response = {}
            print("hi")
            # print(flightOffers)
            flight_price = amadeus.shopping.flight_offers.pricing.post(flight_offer_data)
            flight_price_confirmed = amadeus.shopping.flight_offers.pricing.post(flight_offer_data).data
            print(flight_price_confirmed)
            file_path="test3.txt"
            with open(file_path,"w") as file:
                file.write(json.dumps(flight_price_confirmed["flightOffers"],indent=2))
            if "warnings" in flight_price.__dict__["result"]:
                print("warning present")
                order_response = amadeus.booking.flight_orders.post(flight_price_confirmed["flightOffers"],traveler_details).data # to be uncommented when working with real data
                print("nothing happend")
            else:
                print("no warnings")
                order_response = amadeus.booking.flight_orders.post(flight_price_confirmed["flightOffers"],traveler_details).data # to be uncommented when working with real data
                print("nothing happened")
            # body = flight_price_confirmed['flightOffers']
            response=order_response
            total_base_price = 0
            currency = ''
            for data in response["flightOffers"]:
                print(data["price"]["grandTotal"])
                print(data["price"]["currency"])
          
                currency = data["price"]["currency"]
                base_price = float(data["price"]["grandTotal"])
                total_base_price += base_price
                print(f"Base Price: {base_price} {data['price']['currency']}")

            # print(f"Total Base Price: {total_base_price} {response['flightOffers'][0]['price']['currency']}")
            total_base_price = markupCalculator(total_base_price)
            print(f"Total Base Price: {total_base_price} {response['flightOffers'][0]['price']['currency']}")
            SymbolResponse = requests.get(f"http://127.0.0.1:8000/{currency}").json()
            print(SymbolResponse["currency"])
            baggage_fee = 200
            seat_selection_fee = 50
            airport_tax = 20
            security_fee = 30
            asap_fee = 50
            other_fees = 100

            # print(response["flightOffers"])

            context = {
                'user_Address':travelers['address'],
                'flight_order_data': response,
                'currency': currency,
                'total_base': total_base_price,
                'baggage_fee': baggage_fee,
                'seat_selection_fee':seat_selection_fee,
                'airport_tax': airport_tax,
                'security_fee': security_fee,
                'agency_fee': asap_fee,
                'other_fees': 100,
                'symbol': SymbolResponse["currency"],
            }

            pnr_data = PNR_TABLE.objects.create(email=travelers['contact']['email'],phone=travelers['contact']['phone'],address=travelers["address"]["address"],zip=travelers["address"]["zip"],city=travelers["address"]["city"],ref_id=response["id"])
            # pnr_data = PNR_TABLE.objects.create(email=travelers['contact']['email'],phone=travelers['contact']['phone'],address=travelers["address"]["address"],zip=travelers["address"]["zip"],city=travelers["address"]["city"],ref_id=response["id"])
            # pnr_data = PNR_TABLE.objects.create(email=travelers['contact']['email'],phone=travelers['contact']['phone'],ref_id=response["id"],address=travelers['address'],zipcode=travelers['zip'],city=travelers['city'])
            # print(response["id"])
            # response = amadeus.booking.flight_orders.post(flightOffers,traveler_details).data # to be uncommented when working with real data
            # return JsonResponse("done")
            # response = {
            #           "type": "flight-order",
                      
            #           "id": "eJzTd9f3cTU1MfcDAAp%2BAiU%3D",
            #           "queuingOfficeId": "NCE4D31SB",
            #           "associatedRecords": [
            #             {
            #               "reference": "LE547N",
            #               "creationDate": "2023-12-09T08:49:00.000",
            #               "originSystemCode": "GDS",
            #               "flightOfferId": "1"
            #             }
            #           ],
            #           "flightOffers": [
            #             {
            #               "type": "flight-offer",
            #               "id": "1",
            #               "source": "GDS",
            #               "nonHomogeneous": False,
            #               "lastTicketingDate": "2023-12-09",
            #               "itineraries": [
            #                 {
            #                   "segments": [
            #                     {
            #                       "departure": {
            #                         "iataCode": "GAU",
            #                         "at": "2023-12-15T18:15:00"
            #                       },
            #                       "arrival": {
            #                         "iataCode": "DEL",
            #                         "terminal": "3",
            #                         "at": "2023-12-15T20:45:00"
            #                       },
            #                       "carrierCode": "UK",
            #                       "number": "722",
            #                       "aircraft": {
            #                         "code": "320"
            #                       },
            #                       "duration": "PT2H30M",
            #                       "id": "40",
            #                       "numberOfStops": 0,
            #                       "co2Emissions": [
            #                         {
            #                           "weight": 110,
            #                           "weightUnit": "KG",
            #                           "cabin": "ECONOMY"
            #                         }
            #                       ]
            #                     },
            #                     {
            #                       "departure": {
            #                         "iataCode": "DEL",
            #                         "terminal": "3",
            #                         "at": "2023-12-15T21:40:00"
            #                       },
            #                       "arrival": {
            #                         "iataCode": "BOM",
            #                         "terminal": "2",
            #                         "at": "2023-12-15T23:50:00"
            #                       },
            #                       "carrierCode": "UK",
            #                       "number": "981",
            #                       "aircraft": {
            #                         "code": "320"
            #                       },
            #                       "duration": "PT2H10M",
            #                       "id": "41",
            #                       "numberOfStops": 0,
            #                       "co2Emissions": [
            #                         {
            #                           "weight": 92,
            #                           "weightUnit": "KG",
            #                           "cabin": "ECONOMY"
            #                         }
            #                       ]
            #                     }
            #                   ]
            #                 }
            #               ],
            #               "price": {
            #                 "currency": "EUR",
            #                 "total": "202.86",
            #                 "base": "182.00",
            #                 "fees": [
            #                   {
            #                     "amount": "0.00",
            #                     "type": "TICKETING"
            #                   },
            #                   {
            #                     "amount": "0.00",
            #                     "type": "SUPPLIER"
            #                   },
            #                   {
            #                     "amount": "0.00",
            #                     "type": "FORM_OF_PAYMENT"
            #                   }
            #                 ],
            #                 "grandTotal": "205.06",
            #                 "billingCurrency": "EUR",
            #                 "additionalServices": [
            #                   {
            #                     "amount": "2.20",
            #                     "type": "SEATS"
            #                   }
            #                 ]
            #               },
            #               "pricingOptions": {
            #                 "fareType": [
            #                   "PUBLISHED"
            #                 ],
            #                 "includedCheckedBagsOnly": True
            #               },
            #               "validatingAirlineCodes": [
            #                 "UK"
            #               ],
            #               "travelerPricings": [
            #                 {
            #                   "travelerId": "1",
            #                   "fareOption": "STANDARD",
            #                   "travelerType": "ADULT",
            #                   "price": {
            #                     "currency": "EUR",
            #                     "total": "101.43",
            #                     "base": "91.00",
            #                     "taxes": [
            #                       {
            #                         "amount": "5.53",
            #                         "code": "IN"
            #                       },
            #                       {
            #                         "amount": "2.59",
            #                         "code": "P2"
            #                       },
            #                       {
            #                         "amount": "2.31",
            #                         "code": "YR"
            #                       }
            #                     ],
            #                     "refundableTaxes": "10.43"
            #                   },
            #                   "fareDetailsBySegment": [
            #                     {
            #                       "segmentId": "40",
            #                       "cabin": "ECONOMY",
            #                       "fareBasis": "VL1PTFYS",
            #                       "brandedFare": "ECOYS",
            #                       "class": "V",
            #                       "includedCheckedBags": {
            #                         "weight": 15,
            #                         "weightUnit": "KG"
            #                       },
            #                       "additionalServices": {
            #                         "chargeableSeatNumber": "20A"
            #                       }
            #                     },
            #                     {
            #                       "segmentId": "41",
            #                       "cabin": "ECONOMY",
            #                       "fareBasis": "VL1PTFYS",
            #                       "brandedFare": "ECOYS",
            #                       "class": "V",
            #                       "includedCheckedBags": {
            #                         "weight": 15,
            #                         "weightUnit": "KG"
            #                       },
            #                       "additionalServices": {
            #                         "chargeableSeatNumber": "28D"
            #                       }
            #                     }
            #                   ]
            #                 },
            #                 {
            #                   "travelerId": "2",
            #                   "fareOption": "STANDARD",
            #                   "travelerType": "ADULT",
            #                   "price": {
            #                     "currency": "EUR",
            #                     "total": "101.43",
            #                     "base": "91.00",
            #                     "taxes": [
            #                       {
            #                         "amount": "5.53",
            #                         "code": "IN"
            #                       },
            #                       {
            #                         "amount": "2.59",
            #                         "code": "P2"
            #                       },
            #                       {
            #                         "amount": "2.31",
            #                         "code": "YR"
            #                       }
            #                     ],
            #                     "refundableTaxes": "10.43"
            #                   },
            #                   "fareDetailsBySegment": [
            #                     {
            #                       "segmentId": "40",
            #                       "cabin": "ECONOMY",
            #                       "fareBasis": "VL1PTFYS",
            #                       "brandedFare": "ECOYS",
            #                       "class": "V",
            #                       "includedCheckedBags": {
            #                         "weight": 15,
            #                         "weightUnit": "KG"
            #                       },
            #                       "additionalServices": {
            #                         "chargeableSeatNumber": "18B"
            #                       }
            #                     },
            #                     {
            #                       "segmentId": "41",
            #                       "cabin": "ECONOMY",
            #                       "fareBasis": "VL1PTFYS",
            #                       "brandedFare": "ECOYS",
            #                       "class": "V",
            #                       "includedCheckedBags": {
            #                         "weight": 15,
            #                         "weightUnit": "KG"
            #                       },
            #                       "additionalServices": {
            #                         "chargeableSeatNumber": "24E"
            #                       }
            #                     }
            #                   ]
            #                 }
            #               ]
            #             }
            #           ],
            #           "travelers": [
            #             {
            #               "id": "1",
            #               "dateOfBirth": "1982-01-16",
            #               "gender": "MALE",
            #               "name": {
            #                 "firstName": "JORGE",
            #                 "lastName": "GONZALES"
            #               },
            #               "documents": [
            #                 {
            #                   "number": "00000000",
            #                   "issuanceDate": "2015-04-14",
            #                   "expiryDate": "2025-04-14",
            #                   "issuanceCountry": "ES",
            #                   "issuanceLocation": "Madrid",
            #                   "nationality": "ES",
            #                   "birthPlace": "Madrid",
            #                   "documentType": "PASSPORT",
            #                   "holder": True
            #                 }
            #               ],
            #               "contact": {
            #                 "purpose": "STANDARD",
            #                 "phones": [
            #                   {
            #                     "deviceType": "MOBILE",
            #                     "countryCallingCode": "34",
            #                     "number": "480080076"
            #                   }
            #                 ],
            #                 "emailAddress": "jorge.gonzales833@telefonica.es"
            #               }
            #             },
            #             {
            #               "id": "2",
            #               "dateOfBirth": "1982-01-16",
            #               "gender": "MALE",
            #               "name": {
            #                 "firstName": "JORGE",
            #                 "lastName": "GONZALES"
            #               },
            #               "documents": [
            #                 {
            #                   "number": "00000000",
            #                   "issuanceDate": "2015-04-14",
            #                   "expiryDate": "2025-04-14",
            #                   "issuanceCountry": "ES",
            #                   "issuanceLocation": "Madrid",
            #                   "nationality": "ES",
            #                   "birthPlace": "Madrid",
            #                   "documentType": "PASSPORT",
            #                   "holder": True
            #                 }
            #               ],
            #               "contact": {
            #                 "purpose": "STANDARD",
            #                 "phones": [
            #                   {
            #                     "deviceType": "MOBILE",
            #                     "countryCallingCode": "34",
            #                     "number": "480080076"
            #                   }
            #                 ],
            #                 "emailAddress": "jorge.gonzales833@telefonica.es"
            #               }
            #             }
            #           ],
            #           "remarks": {
            #             "general": [
            #               {
            #                 "subType": "GENERAL_MISCELLANEOUS",
            #                 "text": "ONLINE BOOKING FROM INCREIBLE VIAJES"
            #               }
            #             ]
            #           },
            #           "ticketingAgreement": {
            #             "option": "DELAY_TO_CANCEL",
            #             "delay": "6D"
            #           },
            #           "automatedProcess": [
            #             {
            #               "code": "IMMEDIATE",
            #               "queue": {
            #                 "number": "0",
            #                 "category": "0"
            #               },
            #               "officeId": "NCE4D31SB"
            #             }
            #           ],
            #           "contacts": [
            #             {
            #               "addresseeName": {
            #                 "firstName": "PABLO RODRIGUEZ"
            #               },
            #               "address": {
            #                 "lines": [
            #                   "Calle Prado, 16"
            #                 ],
            #                 "postalCode": "28014",
            #                 "countryCode": "ES",
            #                 "cityName": "Madrid"
            #               },
            #               "purpose": "STANDARD",
            #               "phones": [
            #                 {
            #                   "deviceType": "LANDLINE",
            #                   "countryCallingCode": "34",
            #                   "number": "480080071"
            #                 },
            #                 {
            #                   "deviceType": "MOBILE",
            #                   "countryCallingCode": "33",
            #                   "number": "480080072"
            #                 }
            #               ],
            #               "companyName": "INCREIBLE VIAJES",
            #               "emailAddress": "support@increibleviajes.es"
            #             }
            #           ]
            #         }
            
            return JsonResponse(context,safe=False)
        except ResponseError as e:
            # error = ClientError(e)
            print(e.response.result["errors"][0]["detail"])
            # error_message = {"error": str(e.response.result["errors"])}
            return JsonResponse(e.response.result["errors"],safe=False)


        


def airline_code_lookup(request):
    if request.method == 'GET':
        try:
          code = request.GET.get('code')
          response = amadeus.reference_data.airlines.get(airlineCodes=code).json_data
          return JsonResponse(response)
        except Exception as e:
            
            print(f"Error: {e}")
            error_message = {"error": str(e)}
            return JsonResponse(json.dumps(error_message), content_type="application/json", safe=False)
      


def offers_search_multicity(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        # print(json_data)
        for result in json_data:
            for duration in result["itineraries"]:
                duration["duration"] = revert_duration(duration["duration"])
            for segment in result["itineraries"][0]["segments"]:
                segment["departure"]["at"] = revertDateTime(segment["departure"]["at"])
                segment["arrival"]["at"] = revertDateTime(segment["arrival"]["at"])
        body = {
            "data":{
                "flightOffers": json_data
            }
        }
        print(json_data)
        try:
            response = amadeus.shopping.flight_offers.pricing.post(json_data).data
            print(response)
            context = {
                "flightOffers" : response["flightOffers"],
            }
            return JsonResponse(context)
        
        except ResponseError as e:
            # error = ClientError(e)
            print(e.response.result["errors"][0]["detail"])
            print(f"catch Error: {type(e)}")
            # error_message = {"error": str(e.response.result["errors"])}
            return JsonResponse(e.response.result["errors"],safe=False)

        # return HttpResponse("hello")




def thankyou_page(request):
    return render(request,'thankyou.html')





def summary(request):
    return render(request,"summary.html")


def summary_multi(request):
    return render(request,"summary_multi.html")






def markupCalculator(priceSring):
    price = int(priceSring)
    markup_control_amount = MarkupControl.objects.get(type='amount')
    activation_amount = markup_control_amount.activation
    if activation_amount is True:
        amountAdd = 0
        amountObj = Price_manipulation_amount.objects.all()
        for amount in amountObj:
            amountAdd = amount.price
        calculated_price = price + amountAdd
        print(price)
        print(calculated_price)
        return calculated_price
    else:
        amountPrecentage = 0
        percentObj = Price_manipulation_percentage.objects.all()
        for percent in percentObj:
            amountPrecentage = percent.price
        amountAdd = (price * amountPrecentage)/100
        calculated_price = price + amountAdd
        print(price)
        print(calculated_price)
        return calculated_price
    




def formatDateTime(dateTime):
    parsed_date = datetime.strptime(dateTime, "%Y-%m-%dT%H:%M:%S")

    # Format the datetime object as a string in the desired format
    formatted_date = parsed_date.strftime("%b %d,%Y, %I:%M %p")
    return formatted_date


# Function to parse duration string and format it
def format_duration(duration_string):
    # Initialize indices
    hours_index = 2
    minutes_index = duration_string.find('M')

    # Extract hours and minutes from the duration string
    if 'H' in duration_string:
        hours_index = duration_string.index('H')
    hours = int(duration_string[2:hours_index]) if hours_index > 2 else 0

    if 'M' in duration_string:
        minutes_index = duration_string.index('M')
    minutes = int(duration_string[hours_index + 1:minutes_index]) if minutes_index > hours_index + 1 else 0

    # Format the duration as a string
    formatted_duration = "{:02}H {:02}M".format(hours, minutes)
    return formatted_duration


# date conversion
def convert_date_format(input_date):
    # Convert the input date to a datetime object
    original_date = datetime.strptime(input_date, "%m-%d-%Y")

    # Convert the datetime object to the desired format
    formatted_date = original_date.strftime("%Y-%m-%d")

    return formatted_date



def revert_duration(formatted_duration):
    # Split the formatted duration into hours and minutes
    parts = formatted_duration.split()
    hours, minutes = int(parts[0][:-1]), int(parts[1][:-1])

    # Create the original duration string
    original_duration = "PT{}H{}M".format(hours, minutes)
    return original_duration


def revertDateTime(formatted_date):
    # Parse the formatted date string
    parsed_date = datetime.strptime(formatted_date, "%b %d,%Y, %I:%M %p")

    # Format the datetime object as a string in the original format
    original_date = parsed_date.strftime("%Y-%m-%dT%H:%M:%S")
    return original_date