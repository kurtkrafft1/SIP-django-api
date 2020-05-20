from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction, ParkArea

class AttractionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Attraction
        url = serializers.HyperlinkedIdentityField(
            view_name="attraction",
            lookup_field = "id"
        )
        fields = ('id', 'url', 'name', 'area')

class Attractions(ViewSet):

    def list(self, request):

        attractions = Attraction.objects.all()
        serializer = AttractionSerializer(attractions, many=True, context = {'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):

        try:
            attraction = Attraction.objects.get(pk=pk)
            serializer = AttractionSerializer(attraction, many=False, context = {'request':request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):

        newAttraction =Attraction()
        newAttraction.name = request.data["name"]
        # newAttraction.area_id = request.data["area_id"]
        area = ParkArea.objects.get(pk=request.data["area_id"])
        newAttraction.area = area
        newAttraction.save()

        serialize = AttractionSerializer(newAttraction, many=False, context={'request':request})

        return Response(serialize.data)

    def destroy(self, request, pk=None):

        try:
            attraction = Attraction.objects.get(pk=pk)
            attraction.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Attraction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):

        attraction = Attraction.objects.get(pk=pk)
        attraction.name = request.data["name"]
        area = ParkArea.objects.get(pk=request.data["area_id"])
        attraction.area = area
        attraction.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
