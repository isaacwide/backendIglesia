from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.

import os
import json


#evitar la saturacion de el back 
base_dir = os.path.dirname(os.path.abspath(__file__))
ruta_directa = os.path.join(base_dir, '..', 'data', 'Reina_Valera_1960.json')
#solo lo usamos porque cargamos toda la biblia y pues el json es gigantesco
try:
    with open(ruta_directa, 'r', encoding='utf-8') as f:
        data= json.load(f)
except Exception:
    data = None
class obtenerInfo(generics.CreateAPIView):

    def get(self, request, *args, **kwargs):

        #con eso obtenemos los datos de cada versiculo 
        if not data:
            return Response({"error": "Datos no disponibles"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:

            valor = int(request.query_params.get("value",0))
            N_capitulos = len(data["books"][valor]["chapters"])

            N_versiculos = {} #diccionario varcio 

            for i in range(N_capitulos):
                N_versiculos[i] = len(data["books"][valor]["chapters"][i]["verses"])

            informacion = {
                'N_capitulos':N_capitulos,
                'N_versiculos':N_versiculos
            }

        except (ValueError,IndexError,KeyError):

            return Response({"message": "Error interno"}, status=status.HTTP_404_NOT_FOUND)

        return Response(informacion,status = status.HTTP_200_OK)


class verview(generics.CreateAPIView):
    
    def get(self, request, *args, **kwargs):

        #obtener la direecion del json 

        if not data:
            return Response({"error": "Base de datos no disponible"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try :

            num_libro = int(request.query_params.get("libro", 0))
            capitulo_libro = int(request.query_params.get("capitulo", 0))
            versiculo = int(request.query_params.get("versiculo", 0))

            if num_libro <= 0 or capitulo_libro <= 0 or versiculo <= 0:
                    return Response({"message": "Los parámetros deben ser mayores a 0"}, status=status.HTTP_400_BAD_REQUEST)

            respuesta = {
                
                "verision" : data["version"], 
                "libro" : data["books"][num_libro-1]["name"],
                "capitulo" : data["books"][num_libro-1]["chapters"][capitulo_libro-1]["chapter"],
                "versiculo" :data["books"][num_libro-1]["chapters"][capitulo_libro-1]["verses"][versiculo-1]["verse"],
                "versiculocont" : data["books"][num_libro-1]["chapters"][capitulo_libro-1]["verses"][versiculo-1]["text"]

            }

        except (IndexError, KeyError, ValueError):

            return Response({"message": "versiculo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response(respuesta,status = status.HTTP_200_OK)
