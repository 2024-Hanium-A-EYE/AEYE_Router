from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_inference_models
from .serializers import aeye_inference_serializers
from .forms import aeye_image_form
from colorama import Fore, Back, Style
from datetime import datetime
import requests
import os

def print_log(status, whoami, mw, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[WEB Router - active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " + Fore.BLUE + "[ " + mw + " ]\n" +  Fore.RESET +
              Fore.RED + "[WEB Router - error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

i_am_mw_infer = 'MW - Inference'

server_url    = 'http://127.0.0.1:2000/'
url_hal_infer = 'hal/ai-inference/'

class aeye_inference_Viewswets(viewsets.ModelViewSet):
    queryset=aeye_inference_models.objects.all().order_by('id')
    serializer_class=aeye_inference_serializers

    def create(self, request) :
        serializer = aeye_inference_serializers(data = request.data)
        form = aeye_image_form(request.POST, request.FILES)

        if serializer.is_valid() :
            i_am_client    = serializer.validated_data.get('whoami')
            message_client = serializer.validated_data.get('message')
            image_client   = request.FILES.get('image')

            if form.is_valid():
                    
                print_log('active', i_am_client, i_am_mw_infer, "Succeed to Received Data : {}".format(message_client))

                response_server = aeye_ai_inference_request(image_client)

                if response_server.status_code==200:
                    response_data  = response_server.json()
                    i_am_server    = response_data.get('whoami')
                    message_server = response_data.get('message')
                    
                    print_log('active', i_am_mw_infer, i_am_mw_infer, message_server)
                    data={
                        'whoami' : i_am_mw_infer,
                        'message': message_server
                    }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    message="Failed to receive data from : {}{}".format(server_url, url_hal_infer)
                    data={
                        'whoami' : i_am_mw_infer,
                        'message': message
                    }
                    print('error', i_am_mw_infer, i_am_mw_infer, message)
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

            else:
                message='Failed to receive Image : '.format(form.errors)
                data={
                    'whoami' : i_am_mw_infer,
                    'message': message
                }
                print_log('error', i_am_mw_infer, i_am_mw_infer, message)

                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            print_log('error', i_am_mw_infer, i_am_mw_infer, "Failed to Received Data : {}".format(serializer.errors))

            message = "Client Sent Invalid Data"
            data = aeye_create_json_data(message)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



def aeye_ai_inference_request(image):
    files = aeye_create_json_files(i_am_mw_infer, image)
    data = {
        'whoami' : i_am_mw_infer,
        'operation' : 'Inference',
        'message' : 'Request AI Inference',
    }
    url='{}{}'.format(server_url, url_hal_infer)
    if files!=400:
        print_log('active', i_am_mw_infer, i_am_mw_infer, "Send Data to : {}".format(url))
        response = requests.post(url, data=data, files=files)

        return response


def aeye_create_json_files(whoami, image):
    
    files = {
            'image': (image.name, image.read(), image.content_type),
        }
    print_log('active', whoami, i_am_mw_infer, "Succeeded to add image file to JSON files")
    
    return files

def aeye_get_data_from_response(reponse):
    response_data = reponse.json()
    whoami = response_data.get('whoami', '')
    message = response_data.get('message', '')

    if whoami:
        if message:
            return whoami, message
        else:
            print_log('error', i_am_mw_infer, i_am_mw_infer, "Failed to Receive message from the server : {}"
                                                                                            .format(message))
            return 400
    else:
        print_log('error', i_am_mw_infer, i_am_mw_infer, "Failed to Receive whoami from the server : {}"
                                                                                            .format(whoami))
        return 400
    
def aeye_create_json_data(message):
    data = {
        'whoami' : i_am_mw_infer,
        'message' : message
    }

    return data