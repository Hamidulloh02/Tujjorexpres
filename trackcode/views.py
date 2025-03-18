import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Faqat autentifikatsiyadan o'tgan foydalanuvchilar kirishi mumkin
def get_tracking_info(request):
    # Fetch the documentCode from the query parameters
    document_code = request.query_params.get('documentCode')

    if not document_code:
        # Return an error if documentCode is missing
        return Response({"error": "documentCode is required"}, status=400)

    # Print or log the documentCode for debugging

    # Construct the URL
    url = f"https://tms.fly-express.xyz/selectTrack.htm?documentCode={document_code}"
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        
        # Log the raw response text for debugging
        
        # Parse the JSON response
        try:
            data = response.json()
        except ValueError:
            # If the response is not JSON, return an error
            return Response({"error": "Failed to parse JSON response from tracking service"}, status=500)

        # Log the parsed data for debugging
        
        # Check if the response contains the 'ack' field and if it's 'true'
        if isinstance(data, list) and data[0].get('ack') == 'true':
            tracking_info = data[0].get('data', [])

            
            if tracking_info:
                # Prepare the simplified structure to return
                result = []
                for info in tracking_info:
                    track_details = info.get('trackDetails', [])
                    if len(track_details) >= 10:
                        tenth_track_date = track_details[9].get('track_date') if track_details else None
                    else:
                        tenth_track_date = None
                    

                for info in tracking_info:
                    track_details = info.get('trackDetails', [])
                    if len(track_details) >= 10:
                        nine_track_date = track_details[8].get('track_date') if track_details else None
                    else:
                        nine_track_date = None

                shipment_date = datetime.strptime(nine_track_date, "%Y-%m-%d %H:%M:%S")

                # 3 kun va 5 soat oldingi vaqtni hisoblaymiz
                shipmentDeparturedate = shipment_date - timedelta(days=1, hours=1)

                # Yangi sanani string ko‘rinishda chiqaramiz (T siz)
                new_date_str = shipmentDeparturedate.strftime("%Y-%m-%d %H:%M:%S")

                for info in tracking_info:
                    track_details = info.get('trackDetails', [])
                    if len(track_details) >= 10:
                        seven_track_date = track_details[7].get('track_date') if track_details else None
                    else:
                        seven_track_date = None
                for info in tracking_info:
                    track_details = info.get('trackDetails', [])
                    if len(track_details) >= 10:
                        zero_track_date = track_details[0].get('track_date')
                    else:
                        zero_track_date = None
                    simplified_data = {
                        'shipmentNumber': info.get('trackingNumber'),
                        'shipmentIdCreatTime': tenth_track_date,
                        'shipmentOrgName':'SARAY STORE MCHJ',
                        'shipmentOrgStir':'308 230 483',
                        'shipmentCountryCode':'CN',
                        'shipmentCountry':'China',
                        'shipmentSendOrg':"TIMU",
                        'shipmentDepartureTime':  new_date_str,
                        'shipmentEnterUzb': nine_track_date,
                        'shipmentProcessLocal':seven_track_date,
                        'shipmentReceivedInd':zero_track_date
                    }
                    result.append(simplified_data)

                # Return the cleaned-up tracking data
                return Response(result)

            else:
                return Response({"error": "No tracking data available"}, status=404)
        else:
            return Response({"error": "Invalid response from tracking service or ack not 'true'"}, status=400)
    
    except requests.exceptions.RequestException as e:
        return Response({"error": f"Request failed: {str(e)}"}, status=500)
