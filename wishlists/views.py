from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
