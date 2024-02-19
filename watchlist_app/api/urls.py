from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_details, movie_list
from watchlist_app.api.views import ( WatchListAV,ReviewList,ReviewDetail,ReviewCreate,StreamPlatformView,
    WatchListDetailAV, UserReview, UserReviewbyURL, UserReviewbyqueryparameter, WatchListSV, WatchListCreate)

router = DefaultRouter()
router.register('stream', StreamPlatformView, basename='streamplatform')

urlpatterns = [
    path('',  WatchListAV.as_view(), name='watchlist'),
    path('create/',  WatchListCreate.as_view(), name='watchcreate'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name='watchlist-detail'),
    path('list2/', WatchListSV.as_view(), name='watch-list'),

    path('', include(router.urls)),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('reviews/me', UserReview.as_view(), name='user-review-detail'),
    path('reviews/ruser=<str:username>/', UserReviewbyURL.as_view(), name='user-review-detail'),
    path('reviews/', UserReviewbyqueryparameter.as_view(), name='user-review-detail'),
]
