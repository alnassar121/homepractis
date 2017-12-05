from django.shortcuts import render
from django.http import JsonResponse
import requests

def text_search(request):
	API_KEY = "AIzaSyAa4FjnN77dQQ1mtIQ5sCD4G-q41t1wSC4"
	query = "backyard"
	next_page_token = request.GET.get("next_page_token")

	TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+query+"&key="+API_KEY+"&region=kw"

	if next_page_token is not None:
		TEXT_SEARCH_URL += "&pagetoken=" + next_page_token

	response = requests.get(TEXT_SEARCH_URL)

	context = {
		"response": response.json(),
	}

	return render(request, 'place_search.html', context)

	#return JsonResponse(response.json(), safe=False)


def place_detail(request):
	API_KEY = "AIzaSyAa4FjnN77dQQ1mtIQ5sCD4G-q41t1wSC4"
	reference = request.GET.get("reference", "")
	# maps_key = "AIzaSyAa4FjnN77dQQ1mtIQ5sCD4G"
	maps_key = "AIzaSyBaNTrAzkvNVi1gFLhsZ0A1PG95XIHMrcw"

	PLACE_ID_URL = "https://maps.googleapis.com/maps/api/place/details/json?reference="+reference+"&key="+API_KEY
	response = requests.get(PLACE_ID_URL)

	context = {
		"response": response.json(),
		"api_key": maps_key,
	}

	return render(request, 'place_detail.html', context)

	#return JsonResponse(response.json(), safe=False)