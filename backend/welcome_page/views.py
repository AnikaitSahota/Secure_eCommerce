# from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index_page(request) :
	return HttpResponse('<div class="tenor-gif-embed" data-postid="9862070" data-share-method="host" data-aspect-ratio="1.33333" data-width="100%"><a href="https://tenor.com/view/hello-mother-fucker-well-hello-mother-fucker-gif-9862070">Hello Mother Fucker GIF</a>from <a href="https://tenor.com/search/hello-gifs">Hello GIFs</a></div> <script type="text/javascript" async src="https://tenor.com/embed.js"></script>')
