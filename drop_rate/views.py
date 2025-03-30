from django.shortcuts import render

def events(request):
    return render(request,'drop_rate/events.html')