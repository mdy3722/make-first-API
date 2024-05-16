from django.shortcuts import render, redirect
from .models import Poll
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PollSerializer

def severMessage(msg):
    return {'message' : f"{msg}"} 
# from .forms import PollForm

# def poll_detail(request, id):
#     poll = Poll.objects.get(pk=id)
#     return render(request, 'polls/poll_detail.html', context={'poll': poll})

# def poll_list(request):
#     polls = Poll.objects.all()
#     return render(request, 'polls/poll_list.html', {'polls': polls})

# def poll_create(request):       # 투표 만들기
#     if request.method == 'POST':
#         form = PollForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('poll_list')
#     else:
#         form = PollForm()
#     return render(request, 'polls/poll_create.html', {'form': form})
    
# def vote(request, id):
#     poll = Poll.objects.get(pk=id)

#     if request.method == 'POST':
#         choice = request.POST.get('투표')
#         if choice == 'agree':
#             poll.agrees += 1
#         else:
#             poll.disagrees += 1
#         poll.save()
#         return redirect('poll_detail', id=poll.id)
#     else:
#         # POST 요청이 아닌 경우 404 에러를 반환
#         return render(request, '404.html', status=404)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def poll_detail(request, pk):
    try:
        poll = Poll.objects.get(pk=pk)
    except Poll.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    match request.method:
        case 'GET':
            serializer = PollSerializer(poll)
            return Response(serializer.data)
        case 'PUT':     # 수정
            serializer = PollSerializer(poll, data=request.data) 
            # request 요청을 받은 poll 내용을 serializer에 담음
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        case 'DELETE':
            poll.delete()
            return Response(severMessage("삭제 완료"), status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def poll_list(request):
    match request.method:
        case 'GET':
            order = request.query_params.get('order')
            if order == 'oldest':
                polls = Poll.objects.all().order_by('createdAt')
            elif order == 'latest':
                polls = Poll.objects.all().order_by('-createdAt')

            elif order == 'agree':
                polls = Poll.objects.all().order_by('-agree')
            elif order == 'disagree':
                polls = Poll.objects.all().order_by('-disagree')    
            else:
                polls = Poll.objects.all().order_by('createdAt')
            serializer = PollSerializer(polls, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        case 'POST':
            serializer = PollSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def poll_create(request):
    serializer = PollSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def agree(request, pk):
    poll = Poll.objects.get(pk=pk)
    poll.agree += 1
    poll.calculate_rate()
    poll.save()
    return Response(severMessage("투표 성공 - agree"), status=status.HTTP_200_OK)  # 투표 성공

@api_view(['POST'])
def disagree(request, pk):
    poll = Poll.objects.get(pk=pk)
    poll.disagree += 1
    poll.calculate_rate()
    poll.save()
    return Response(severMessage("투표 성공 - disagree"), status=status.HTTP_200_OK)  # 투표 성공