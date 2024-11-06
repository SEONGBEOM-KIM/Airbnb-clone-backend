from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rooms.models import Room
from .models import Wishlist
from .serializers import WishlistsSerializer


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistsSerializer(
            all_wishlists,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serilalizer = WishlistsSerializer(data=request.data)
        if serilalizer.is_valid():
            wishlist = serilalizer.save(user=request.user)
            serilalizer = WishlistsSerializer(wishlist)
            return Response(serilalizer.data)
        else:
            return Response(serilalizer.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(
                pk=pk,
                user=user,
            )
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistsSerializer(
            wishlist,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistsSerializer(
            wishlist,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            updated_wishlist = serializer.save()
            serializer = WishlistsSerializer(updated_wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class WishlistToggle(APIView):

    permission_classes = [IsAuthenticated]

    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(
                pk=pk,
                user=user,
            )
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(
            pk,
            request.user,
        )
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)
