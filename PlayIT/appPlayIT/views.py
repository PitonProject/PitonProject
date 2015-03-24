from django.shortcuts import render, render_to_response

# Create your views here.
def mainpage(request):
   return render_to_response(
        'mainpage.html',
        {
                'titlehead': 'PlayIT app',
                'pagetitle': 'Benvingut a PlayIT. Una aplicacio de seleccio de musica per un local',
                'user': request.user
        })