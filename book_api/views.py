from urllib import response
from django.shortcuts import render
from book_api.models import Book
from rest_framework.decorators import api_view
from rest_framework.response import Response
from book_api.serializer import BookSerializer

# Create your views here.
# class or function => data 를 return 하는 end point
@api_view(['GET'])
def book_list(request):
  # db에서 데이터 가져오기
  # complex data -> python code로 변경 필요
  books = Book.objects.all()
  # python data structure(DS)
  serializer = BookSerializer(books, many=True)
  return Response(serializer.data)

@api_view(['POST'])
def book_create(request):
  # json -> db 데이터로 변경
  serializer = BookSerializer(data=request.data)
  # 유효성 검증
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  else:
    return Response(serializer.error)
  
# 특정 id 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def book(request, pk):
  book = Book.objects.get(pk=pk)
  if request.method == 'GET':
    serializer = BookSerializer(book)
    return Response(serializer.data)
  
  if request.method == 'PUT':
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return serializer.errors
  
  if request.method == 'DELETE':
    book.delete()
    return Response({
      'delete': True
    })