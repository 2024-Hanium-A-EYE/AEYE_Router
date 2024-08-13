from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import aeye_wno_models
from .serializers import aeye_wno_serializers
from colorama import Fore, Back, Style
from datetime import datetime
import requests
import asyncio
import aiohttp


def print_log(status, whoami, api, message) :
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if status == "active" :
        print("\n-----------------------------------------\n"   + 
              current_time + " [ " + whoami + " ] send to : " +Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.GREEN + "[active] " + Fore.RESET + "message: [ " + Fore.GREEN + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")
    elif status == "error" :
        print("\n-----------------------------------------\n"   + 
              current_time + " " + whoami + Fore.BLUE + "[ " + api + " ]\n" +  Fore.RESET +
              Fore.RED + "[error] " + Fore.RESET + "message: [ " + Fore.RED + message +" ]" + Fore.RESET +
              "\n-----------------------------------------")

i_am_api_wno = 'Router API - WNO'

url_server       = 'http://127.0.0.1:2000/'
mw_ai_inference  = 'mw/ai-inference/'

class aeye_wno_Viewsets(viewsets.ModelViewSet):
    queryset=aeye_wno_models.objects.all().order_by('id')
    serializer_class=aeye_wno_models

    def create(self, request) :
        serializer = aeye_wno_serializers(data = request.data)

        if serializer.is_valid() :
            i_am_client = serializer.validated_data.get('whoami')
            operation   = serializer.validated_data.get('operation')
            message     = serializer.validated_data.get('message')

            print_log('active', i_am_client, i_am_api_wno, 'Received Valid Data : {}, Oper: {}'.format(message, operation))
            
            if operation=='Inference' :
                image = request.FILES.get('image')

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response_from_server = loop.run_until_complete(aeye_ai_inference_request(i_am_client, image))
                print_log('active', i_am_client, i_am_api_wno, "GGGAA")

                
                i_am_server    = response_from_server.get('whoami')
                server_message = response_from_server.get('message')

                data={
                    'whoami' : i_am_api_wno,
                    'message': server_message
                } 
                return Response(data, status=status.HTTP_200_OK)

            elif operation=='Train':
                pass
            elif operation=='Test':
                pass
            elif operation=='database':
                pass
                        
        else :
            return Response('["ERROR"] WEB Server is Not Working!', status = status.HTTP_400_BAD_REQUEST)
    

async def aeye_ai_inference_request(i_am_client : str, image):
    message = "Failed to Receive Data [NetOper - WNO]"
    url='{}{}'.format(url_server, mw_ai_inference)
    print_log('active', i_am_client, i_am_api_wno, "Send Data to : {}".format(url))

    async with aiohttp.ClientSession() as session:
        message='Request AI Inference'
        form_data = aiohttp.FormData()
        form_data.add_field('whoami', i_am_api_wno)
        form_data.add_field('message', message)
        form_data.add_field('image', image.read(), filename=image.name, content_type=image.content_type)
        async with session.post(url, data=form_data) as response_from_server:
            result_from_server = await response_from_server

    
    print_log('active', i_am_client, i_am_api_wno, "Send Data to : {}".format(result_from_server))
