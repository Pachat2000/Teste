import requests
from django.http import JsonResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build


def movie_list(request):
    response = requests.get('http://www.omdbapi.com/', params={
        's': 'Fast & Furious',
        'apikey': '1955a337'
    })
    data = response.json()
    movies = []
    for movie in data['Search']:
        Image = movie['Poster']
        Annee = movie['Year']
        Titre = movie['Title']
        IdFilm = movie['imdbID']
        response = requests.get('http://www.omdbapi.com/', params={
            'i': IdFilm,
            'apikey': '1955a337'
        })
        data2 = response.json()
        Realisateur = data2['Director']
        movies.append([Image, Titre, Annee, Realisateur])

    return JsonResponse({'movies': movies})


def Spreadsheet(request):
    response = requests.get('http://www.omdbapi.com/', params={
        's': 'star wars',
        'apikey': '1955a337'
    })
    data_1 = response.json()
    S_Actor = ""
    for data in data_1['Search']:
        response = requests.get('http://www.omdbapi.com/', params={
            't': data['Title'],
            'apikey': '1955a337'
        })
        data0 = response.json()
        S_Actor += data0['Actors']+","
    print(S_Actor)

    response = requests.get('http://www.omdbapi.com/', params={
        's': 'Pirates of the Caribbean',
        'apikey': '1955a337'
    })
    data = response.json()
    movies = []
    for movie in data['Search']:
        Image = movie['Poster']
        Annee = movie['Year']
        Titre = movie['Title']
        IdFilm = movie['imdbID']

        response = requests.get('http://www.omdbapi.com/', params={
            'i': IdFilm,
            'apikey': '1955a337'
        })
        data2 = response.json()
        Realisateur = data2['Director']

        response = requests.get('http://www.omdbapi.com/', params={
            't': Titre,
            'apikey': '1955a337'
        })
        data3 = response.json()
        acteur = []
        if 'Actors' in data3:
            acteur = data3['Actors']
        List_actor = ""
        resultat = ""
        for act in acteur:
            if act == ',' and (List_actor in S_Actor):
                resultat = resultat + " " + List_actor

                List_actor = " "
            List_actor += act
        movies.append([Image, Titre, Annee, Realisateur, int(
            Annee) < 2015, "Paul Walker" in acteur, resultat])

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets']
    secret_file = './Identifiant/identifiant.json'
    spreadsheet_id = '12k57QJTMysso-GQE3tDZ6uFXas0LB7WCKxnkQuVV_bk'
    credentials = service_account.Credentials.from_service_account_file(
        secret_file, scopes=scopes)

    service = build('sheets', 'v4', credentials=credentials)

    values = movies
    sheet_range = 'Feuille 1!A1'
    request_body = {
        'values': values
    }
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=sheet_range, valueInputOption='USER_ENTERED', body=request_body)
    response = request.execute()
