from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ProductSerializer, FileSerialzier
from rest_framework import status
import os
import json
from . import clip
from . import milvus
from .models import Image
from django.http import HttpResponse
import requests

class AddData(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FileSerialzier(data=request.data)
        if serializer.is_valid():
            file = request.data.get("file")
            _, file_extension = os.path.splitext(file.name)
            if file_extension.lower() != ".json":
                return Response(
                    data={"error": "please sent .json file"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                data = json.load(file)
                print(data)
                print(type(data[0]["images"]))
            except json.JSONDecodeError:
                return Response(data={"error": "JSONDecodeError"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ProductSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Search(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            query = request.data.get("query", None)
        except Exception as er:
            return Response(data={"error":str(er)}, status=status.HTTP_400_BAD_REQUEST)

        cli = clip.Clip()
        emb = cli.text_embeding(query)
        db = milvus.Milvus()
        result = db.search(
            vectors_to_search=[emb],
            collection_name = "Mori",
            search_params={
                "metric_type": "IP",
                "params": {"nprobe": 10},
            },
            field="embeddings",
            limit=1,
            output_fields=["pk"]
        )
        try:
            image = Image.objects.get(id=result[0][0].id)
            response = requests.get(image.url)
            content_type = response.headers['Content-Type']
            return HttpResponse(response.content, content_type=content_type, status=status.HTTP_200_OK)
        except Exception as er:
            print(str(er))
            return Response(data={"error":str(er)}, status=status.HTTP_400_BAD_REQUEST)







