# README #

Zadanie
Endpoint nr 1.
POST
Przyjmuje jsona z polem: "name" i zapisuje je do google datastore.
Można wysłać kilkakrotnie (w osobnych requestach) jsona z tą samą wartością pola "name".

Endpoint nr 2.
PUT
Przyjmuje jsona i pozwala zmieniać wartość pola "name" _tylko_ dla istniejących wpisów.

Endpoint nr 3.
GET
Pozwala pobrać wybrane "name" (tylko istniejące w bazie) wraz z informacją ile razy zostało dodane.
Jednym requestem pytamy tylko o jedno "name".

### RUN ###

* python3 __init__.py
* requesty za pomocą postmana

### Wymagania ###
* Python 3
* pip3 install -r requirements.txt
* google SDK
* autoryzacja do bazy google bądź własna

### Google Datasotre ###

w settings.py:
* CLIENT - swoja nazwa projektu w datasotre
* KIND - Rodzaj wncji

Wymagania encji:
* name - Ciąg
* count - Liczba (default 1)

### TODO ###
* UUUID
* Lepsza walidacja dancyh
* Logowanie po API_KEY
