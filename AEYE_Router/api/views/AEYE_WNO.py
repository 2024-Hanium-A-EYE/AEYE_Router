from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_wno_models
from .serializers import aeye_wno_serializers
from colorama import Fore, Back, Style
from datetime import datetime
import requests

def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[AI NetOper - active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.RED + "[AI NetOper - error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

api = 'API - ANO'

url = 'http://127.0.0.1:2000/mw/ai-inference/'

class aeye_wno_Viewsets(viewsets.ModelViewSet):
    queryset=aeye_wno_models.objects.all().order_by('id')
    serializer_class=aeye_wno_models

    def create(self, request) :
        serializer = aeye_wno_serializers(data = request.data)

        if serializer.is_valid() :
            whoami    = serializer.validated_data.get('whoami')
            operation = serializer.validated_data.get('operation')
            message   = serializer.validated_data.get('message')

            print_log('active', whoami, api, 'Received Valid Data : {}, Oper: {}'.format(message, operation))
            
            if operation=='Inference' :
                image = request.FILES.get('image')

                response = aeye_ai_inference_request(whoami, image, url)
                
                if response.status_code==200:
                    whoami, message = aeye_get_data_from_response(response)
                    data = aeye_create_json_file(message)

                    return Response(data, status = status.HTTP_200_OK)
                else:
                    message = 'Failed to Receive Data From Server'
                    data = aeye_create_json_file(message)

                    return Response(data, status = status.HTTP_400_BAD_REQUEST)
                
            elif operation=='Train':
                pass
            elif operation=='Test':
                pass
            elif operation=='database':
                pass
            
            return response
            
        else :
            return Response('["ERROR"] WEB Server is Not Working!', status = status.HTTP_400_BAD_REQUEST)
    

def aeye_ai_inference_request(whoami, image, url):
    message = "Failed to Receive Data [NetOper - WNO]"
    files = {'image': (image.name, image.read(), image.content_type)}
    data = {
        'whoami' : 'AEYE NetOper WNO',
        'message' : 'Request AI Inference'
    }

    print_log('active', whoami, api, "Send Data to : {}".format(url))

    response = requests.post(url, data=data, files=files)

    if response.status_code==200:
        print_log('active', whoami, api, "Received Data from : {}".format(url))

        response_data = response.json()
        whoami, message = aeye_get_data_from_response(response_data)
        
        print_log('active', whoami, api, "Succedd to Receive Data : {}".format(message) )
        return response
    else:
        print_log('error', whoami, api, "Failed to Receive Data : {}".format(message) )
        return response


def aeye_get_data_from_response(reponse):
    response_data = reponse.json()
    whoami = response_data.get('whoami', '')
    message = response_data.get('message', '')

    if whoami:
        if message:
            return whoami, message
        else:
            print_log('error', 'AEYE NetOper WNO', api, "Failed to Receive message from the server : {}"
                                                                                            .format(message))
            return 400
    else:
        print_log('error', 'AEYE NetOper WNO', api, "Failed to Receive whoami from the server : {}"
                                                                                            .format(whoami))
        return 400
    
def aeye_create_json_file(message):
    data = {
        'whoami' : "AEYE NetOper WNO",
        'message' : message
    }

    return data