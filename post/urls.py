# from django.urls import path
# from .views import postlistview, postdetailview, postcreateview, postupdateview, postdeleteview

# urlpatterns = [
#     path('', postlistview, name='post_list'),
#     path('<int:pk>', postdetailview, name='post_detail'),
#     path('create/', postcreateview, name='post_create'),
#     path('<int:pk>/update/', postupdateview, name='post_update'),
#     path('<int:pk>/delete/', postdeleteview, name='post_delete'),
# ]


from django.urls import path
from . import views 

urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailUpdateDestroyView.as_view(), name='post_detail'),
    path('<int:pk>/comments/', views.CommentListCreateView.as_view(), name='comment-list'),
    path('<int:pk>/comments/<int:comment_pk>/', views.CommentDetailUpdateDestroyView.as_view(), name='comment-detail'),
    
]
