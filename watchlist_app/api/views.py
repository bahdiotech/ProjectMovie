from django.shortcuts import get_object_or_404
from watchlist_app.models import StreamPlatform, WatchList, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
# from rest_framework.decorators import api_view
from rest_framework import status
# from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchlistPagination, WatchlistLimitOffsetPagination, WatchlistCursorPagination



class UserReviewbyURL(generics.ListAPIView):
    """This is a filtering method example"""
    """Filter against url or optional keyword"""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)

class UserReview(generics.ListAPIView):
    """This is a filtering method example"""
    """Filtering against current user"""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.user
        return Review.objects.filter(review_user__username=username)

class UserReviewbyqueryparameter(generics.ListAPIView):
    """This is a filtering method example"""
    """Filter against query parameters """

    serializer_class = ReviewSerializer



    def get_queryset(self):
        # queryset = Review.objects.all()
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)
        # if username is not None:
        #     return Review.objects.filter(review_user__username=username)
        # return queryset


class ReviewList(generics.ListAPIView):

    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']


    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]




    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlistpk = WatchList.objects.get(pk=pk)

        cur_review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlistpk, review_user=cur_review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watch!")
        if watchlistpk.number_rating == 0:
            watchlistpk.avg_rating = serializer.validated_data['rating']
        else:
            watchlistpk.avg_rating =  (watchlistpk.avg_rating + serializer.validated_data['rating'])/2

        watchlistpk.number_rating+=1
        watchlistpk.save()

        serializer.save(watchlist=watchlistpk, review_user=cur_review_user)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    # def get_queryset(self):
    #     pk = self.kwargs['pk']
    #     return Review.objects.filter(watchlist=pk)


    permission_classes = [IsReviewUserOrReadOnly]


# class StreamPlatformView(viewsets.ReadOnlyModelViewSet):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer



class StreamPlatformView(viewsets.ModelViewSet):
    """ With viewsets you can create both the list and detail
    view with just short code and even auto generate your Url
    """
    permission_classes = [IsAdminOrReadOnly]

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class WatchListSV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']
    pagination_class = WatchlistCursorPagination



class WatchListAV(APIView):

    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchListDetailAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movies = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND )

        serializer = WatchListSerializer(movies)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        content = {'Delete'}
        movie.delete()
        return Response(content, status = status.HTTP_204_NO_CONTENT)


# class StreamPlatformView(viewsets.ViewSet):
#     """ A simple ViewSet for listing or retrieving users. """
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self, request, pk=None):
#         serializers = StreamPlatformSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         else:
#             return Response(serializers.errors)

#     def put(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(status = status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         content = {'Delete'}
#         stream.delete()
#         return Response(content, status = status.HTTP_204_NO_CONTENT)



# class StreamPlatformAV(generics.ListCreateAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer

# class StreamPlatformDetailAV(generics.RetrieveUpdateDestroyAPIView):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer


# class ReviewDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)




# class StreamPlatformAV(APIView):
#     def get(self, request):
#         platform = StreamPlatform.objects.all()
#         serializers = StreamPlatformSerializer(platform, many=True, context={'request': request})
#         return Response(serializers.data)

#     def post(self, request):
#         serializers = StreamPlatformSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         else:
#             return Response(serializers.errors)


# class StreamPlatformDetailAV(APIView):

#     def get(self,request, pk):
#         try:
#             streams = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'Error': 'Not found!'}, status=status.HTTP_404_NOT_FOUND )

#         serializer = StreamPlatformSerializer(streams, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(status = status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         content = {'Delete'}
#         stream.delete()
#         return Response(content, status = status.HTTP_204_NO_CONTENT)







# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):

#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND )

#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(status = status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         content = {'Delete'}
#         movie.delete()
#         return Response(content, status = status.HTTP_204_NO_CONTENT)
