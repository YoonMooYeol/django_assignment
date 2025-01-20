# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Post
# from .forms import PostForm
# from django.views.decorators.http import require_http_methods

# @require_http_methods(['GET'])
# def postlistview(request):
#     posts = Post.objects.all().order_by('-created_at')
#     return render(request, 'post/post_list.html', {'posts': posts})

# @login_required
# @require_http_methods(['GET', 'POST'])
# def postdetailview(request, pk):
#     if request.method == 'POST':
#         post = get_object_or_404(Post, pk=pk)
#         post.comment_set.create(content=request.POST.get('content'), author=request.user)
#         return redirect('post_detail', pk=pk)
#     else:
#         post = get_object_or_404(Post, pk=pk)
#     return render(request, 'post/post_detail.html', {'post': post})

# @login_required
# @require_http_methods(['GET', 'POST'])
# def postcreateview(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'post/post_create.html', {'form': form})

# @login_required
# @require_http_methods(['GET', 'POST'])
# def postupdateview(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.user != post.author:
#         return redirect('post_list')
    
#     if request.method == 'POST':
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'post/post_update.html', {
#         'form': form,
#         'post': post  # post 객체를 context에 추가
#     })

# @login_required
# @require_http_methods(['POST'])
# def postdeleteview(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.user != post.author:
#         return redirect('post_list')
#     post.delete()
#     return redirect('post_list')



from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_assignment.permissions import IsOwnerOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostListCreateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostDetailUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    
    def get(self, request, pk):
        try:
            post = get_object_or_404(Post, pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(
            {"error": "게시글이 없습니다."},
            status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        
    def put(self, request, pk):
        try:
            post = get_object_or_404(Post, pk=pk)
            if request.user != post.author:
                return Response(
                    {"error": "본인만 수정할 수 있습니다."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response(
                {"error": "게시글이 없습니다."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get(self, request, pk): 
        comments = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk): 
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    

class CommentDetailUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get(self, request, pk, comment_pk):
        try:
            comment = get_object_or_404(Comment, pk=comment_pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(
                {"error": "댓글이 없습니다."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
     
    
    def put(self, request, pk, comment_pk):
        try:
            comment = get_object_or_404(Comment, pk=comment_pk)
            if request.user != comment.author:
                return Response(
                    {"error": "본인만 수정할 수 있습니다."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response(
                {"error": "댓글이 없습니다."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    def delete(self, request, pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user != comment.author:
            return Response(
                {"error": "본인의 댓글만 삭제할 수 있습니다."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    