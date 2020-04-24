from django.shortcuts import render,HttpResponse
import requests
import json

# The url doesn't need to be defined in a function as formatting can be done after
url = "https://dictionaryapi.com/api/v3/references/collegiate/json/{}?key=${{ secrets.API_KEY }}"

def index(request):
    return render(request, template_name="base.html")

def searchWord(request):
    try:
        word = request.GET.get('q')
        resp = requests.get(url.format(word)) # format is for formatting the word into the url
        data = resp.json()
        Wordlist = []
        for item in data:
            Wordlist.append({
                "word": item['meta']['id'],
                "pos" : item['fl'],
                "defn": item['shortdef'],
            })                            # for prettier reading capability and improved spacing in some functions
        return render(request, "word.html", {"Wordlist": Wordlist, "searchWord": word})
    except requests.exceptions.ConnectionError:
        return render(request, "interneterror.html")
    except KeyError:
        return render(request, "word.html", {"Wordlist": Wordlist, "searchWord": word})
    except TypeError:
        return render(request, "worderror.html", {"suggWords": data, "searchWord": word})

