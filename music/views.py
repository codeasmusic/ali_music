from django.shortcuts import render

# Create your views here.
from .models import MusicChart


def index(request):
	mc = MusicChart()
	image_paths = mc.plot_all_artists()
	return render(request, 'music/index.html', {'image_paths': image_paths})


def query(request):
	if 'aid' in request.GET:
		artists_id = request.GET['aid']

		mc = MusicChart()
		image_path = mc.search_an_artist(artists_id)
		return render(request, 'music/an_artist_graph.html', {'image_path': image_path})
	else:
		return render(request, 'music/query.html', {})