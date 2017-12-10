from flask import Flask, render_template, request
from random import randint
import json, musicgenres, requests

app = Flask(__name__)

url = 'https://api.foursquare.com/v2/venues/explore'
foursquare_limit = 50

# get user location
# send_url = 'http://freegeoip.net/json'
# r = requests.get(send_url)
# j = json.loads(r.text)
# lat = j['latitude']
# lon = j['longitude']

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/books")
def books():
	return render_template('books.html', category='music')

@app.route("/movie", methods=['POST'])
def movie():
	value = request.form["genres"]
	pages = [randint(1,200), randint(1,200), randint(1,200)]
	return render_template('movies.html', id=value, pages=pages)

@app.route("/game", methods=['POST'])
def game():
	value = request.form["genres"];

	return render_template('games.html', id=value)

@app.route("/book", methods=['POST'])
def book():
	value = request.form["genres"]
	return render_template('books.html', id=value)

@app.route("/music", methods=['POST'])
def music():
	genreid = request.form["genres"]
	genres = musicgenres.GetMusicGenres()
	genrename = ""
	for genre in genres:
		if (genre['id'] == int(genreid)):
			genrename = genre['genreName']
	return render_template('music.html', genreId=genreid, genreName=genrename)

@app.route("/cultural", methods=['POST'])
def cultural():
	value = request.form["genres"]
	params = dict(
	    client_id = 'NGZ03R5TJK50MJKXMBM1TDVBCZCVBISG4BRTSZWZOFPRPHIC',
	    client_secret = 'IQJBFZMQZVB0MZIF1JUOMZ30HAHBBAJTK02FMC42DTY1XT5P',
	    v = '20170801',
	    near = 'Istanbul',
	    query = value,
	    venuePhotos = 1,
	    limit = foursquare_limit
	)
	resp = requests.get(url=url, params=params)
	data = json.loads(resp.text)

	items = []
	item_image_url = []
	item_name = []
	item_location = []

	random = []
	r1 = randint(0, foursquare_limit)
	random.append(r1)
	r2 = randint(0, foursquare_limit)
	r3 = randint(0, foursquare_limit)

	for i in range(0,foursquare_limit):
		items.append(data['response']['groups'][0]['items'][i])

		item_name.append(items[i]['venue']['name'])
		item_image_url.append(items[i]['venue']['featuredPhotos']['items'][0]['prefix']+'original'+items[i]['venue']['featuredPhotos']['items'][0]['suffix'])
		item_location.append(items[i]['venue']['location']['formattedAddress'])

	while (r2 == r1 or r3 == r1):
		if r2 == r1:
			r2 = randint(0, foursquare_limit)
		if r3 == r1:
			r3 = randint(0, foursquare_limit)
	random.append(r2)
	random.append(r3)

	return render_template('cultural.html', number=foursquare_limit, names=item_name, imgurls=item_image_url, addresses=item_location, random=random)

@app.route("/concert")
def deneme():
	return render_template("concert.html")

@app.route("/cinema")
def cinema():
	return render_template("cinema.html")

@app.route("/line")
def line():
	return render_template("eventsuggester.html")

if __name__ == "__main__":
	app.debug = True
	app.run()