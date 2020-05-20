from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Itinerary, Attraction, Customer

class ItinerarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name= "itinerary",
            lookup_field = "id"
        )
        fields = ('id', 'url', 'starttime', 'attraction')
        depth = 2

class Itineraries(ViewSet):

    def list(self, request):
        customer = Customer.objects.get(user=request.auth.user)
        itineraries = Itinerary.objects.all()
        itineraries = itineraries.filter(customer = customer)

        serialize = ItinerarySerializer(itineraries, many=True, context={'request': request})

        return Response(serialize.data)
    
    def retrieve(self, request, pk=None):
        try:    
            itineraries = Itinerary.objects.get(pk=pk)
            serialize = ItinerarySerializer(itineraries, many=False, context={'request': request})
            return Response(serialize.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):

        newItinerary = Itinerary()
        newItinerary.starttime = request.data["starttime"]

        customer = Customer.objects.get(user=request.auth.user)
        newItinerary.customer = customer

        attraction = Attraction.objects.get(pk=request.data["attraction_id"])
        newItinerary.attraction = attraction

        newItinerary.save()

        serialize = ItinerarySerializer(newItinerary, context={"request":request})
        return Response(serialize.data)
    
    def destroy(self, request, pk=None):

        try:
            itin = Itinerary.objects.get(pk=pk)
            itin.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None): 

        editeditin = Itinerary.objects.get(pk=pk)
        editeditin.starttime = request.data["starttime"]
        #change to this\/
        attraction = Attraction.objects.get(pk=request.data["attraction_id"])
        editeditin.attraction = attraction
        editeditin.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    

        