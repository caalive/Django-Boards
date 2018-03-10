from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import NewTopicForm
from .models import Board, Topic, Post


def home(request):
    board = Board.objects.all()
    return render(request, 'home.html', {'boards': board})


def board_topics(request, pk):
    # try:
    #     board = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404
    # return render(request, 'topics.html', {'board': board})
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                messsage=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html', {'board': board, 'form': form})


    # if request.method == 'POST':
    #     subject = request.POST['subject']
    #     message = request.POST['message']
    #
    #     user = User.objects.first()
    #
    #     topic = Topic.objects.create(
    #         subject=subject,
    #         board=board,
    #         starter=user
    #     )
    #
    #     post = Post.objects.create(
    #         message=message,
    #         topic=topic,
    #         created_by=user
    #     )
    #     return redirect('board_topics', pk=board.pk)
    # return render(request, 'new_topic.html', {'board': board})


