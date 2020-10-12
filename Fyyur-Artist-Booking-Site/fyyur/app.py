#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# Connect to a local postgresql database
migrate = Migrate(app, db)

# To create the first migration, run the following commands:
# flask db init
# flask db migrate
# flask db upgrade

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(250))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    shows = db.relationship('Show', backref='venue', cascade="all,delete", lazy=True)
    
    def __repr__(self):
      return f'<Venue : {self.id} {self.name}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venues = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(250))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    shows = db.relationship('Show', backref='artist', cascade="all,delete", lazy=True)

    def __repr__(self):
      return f'<Artist : {self.id} {self.name}>'

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer , db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer , db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime , nullable=False)

    def __repr__(self):
      return f'<Show : {self.id}>'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

def format_phone(phone):
  phone=phone.replace('-','')
  if(len(phone)==10):
    phone = phone[:3] +'-' +phone[3:6]+'-'+phone[6:]
  return phone

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  # recently added artists and venues
  artists = Artist.query.order_by(db.desc(Artist.creation_date)).limit(3)
  venues = Venue.query.order_by(db.desc(Venue.creation_date)).limit(3)
  return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  venues = Venue.query.all()
  venue_cities = set()
  
  for venue in venues:
    venue_cities.add((venue.city, venue.state))

  for venue_city in venue_cities:
    data.append({
      "city": venue_city[0],
      "state": venue_city[1],
      "venues": []})

  # get the number of upcoming shows for each venue
  for venue in venues:
    num_upcoming_shows = Show.query.filter_by(venue_id=venue.id).filter(Show.start_time > datetime.now()).all()
    
    # for each entry, add venues to matching city/state
    for entry in data:
      if venue.city == entry['city'] and venue.state == entry['state']:
        entry['venues'].append({
          "id": venue.id, 
          "name": venue.name,
          "num_upcoming_shows": len(num_upcoming_shows)
        })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  data = []
  count = 0

  search_term = request.form.get('search_term', '').lower() # case-insensitive search
  venues = Venue.query.all()

  for venue in venues:
    current_venue = venue.name.lower()
    if current_venue.find(search_term) != -1:
      data.append(venue)
      count += 1
    
  response = { 
    "count": count, 
    "data": data 
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  num_upcoming_shows = []
  num_past_shows = []

  venue = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id = venue_id).all()

  for show in shows:
    if show.start_time > datetime.now():
      # if an upcoming show
      num_upcoming_shows.append({
        "artist_id": show.artist_id,
        "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
        "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
        "start_time": format_datetime(str(show.start_time))
      })
    else:
      # if a past show
      num_past_shows.append({
        "artist_id": show.artist_id,
        "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
        "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
        "start_time": format_datetime(str(show.start_time))
      })

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": format_phone(venue.phone),
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": num_past_shows,
    "upcoming_shows": num_upcoming_shows,
    "past_shows_count": len(num_past_shows),
    "upcoming_shows_count": len(num_upcoming_shows)
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion

  try:
    seeking_talent = request.form.get('seeking_talent', None)
    # Try to create a new Venue record and add to the db
    venue = Venue(
      name = request.form['name'],
      address = request.form['address'],
      city = request.form['city'],
      state = request.form['state'],
      phone = request.form['phone'],
      genres = request.form.getlist('genres'),
      facebook_link = request.form['facebook_link'],
      website = request.form['website'],
      image_link = request.form['image_link'],
      seeking_talent = True if seeking_talent != None else False,
      seeking_description = request.form['seeking_description']
    )
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    # on unsuccessful db insert, flash an error instead
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail
  try:
    venue = venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue + ' was successfully deleted!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. '+ sys.exc_info()[0]+'. Venue ' + venue + ' could not be deleted.')
  finally:
    db.session.close()

  return render_template('layouts/main.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  data = []
  count = 0

  search_term = request.form.get('search_term', '').lower()
  artists = Artist.query.all() 
  
  for artist in artists:
    current_artist = artist.name.lower()
    if (current_artist.find(search_term) != -1):
      data.append(artist)
      count += 1

  response = {
   "data" : data,
   "count" : count
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  num_upcoming_shows = []
  num_past_shows = []

  artist = Artist.query.get(artist_id)
  shows = Show.query.filter_by(artist_id=artist_id)
  
  for show in shows:
    if show.start_time > datetime.now():
      # if an upcoming show
      num_upcoming_shows.append({
        "artist_id": show.artist_id,
        "venue_id" : show.venue_id,
        "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
        "venue_image_link": Venue.query.filter_by(id=show.venue_id).first().image_link,
        "start_time": format_datetime(str(show.start_time))
      })
    else:
      # if a past show
      num_past_shows.append({
        "artist_id": show.artist_id,
        "venue_id" : show.venue_id,
        "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
        "venue_image_link": Venue.query.filter_by(id=show.venue_id).first().image_link,
        "start_time": format_datetime(str(show.start_time))
      })
  
  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": format_phone(artist.phone),
    "website" : artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venues": artist.seeking_venues,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": num_past_shows,
    "upcoming_shows": num_upcoming_shows,
    "past_shows_count": len(num_past_shows),
    "upcoming_shows_count": len(num_upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  form.name.data = artist.name
  form.genres.data = artist.genres
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.website.data = artist.website
  form.facebook_link.data = artist.facebook_link
  form.seeking_venues.data = artist.seeking_venues
  form.seeking_description.data = artist.seeking_description
  form.image_link.data = artist.image_link
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)

  try:
    seeking_venues = request.form.get('seeking_venues', None)
    artist.name = request.form['name']
    artist.genres = ','.join(request.form.getlist('genres'))
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.website = request.form['website']
    artist.facebook_link = request.form['facebook_link']
    artist.seeking_venues = True if seeking_venues != None else False
    artist.seeking_description = request.form['seeking_description']
    artist.image_link = request.form['image_link']
    
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
    # on unsuccessful db insert, flash an error instead.
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  form.website.data = venue.website
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  venue = Venue.query.get(venue_id)

  try:
    seeking_talent = request.form.get('seeking_talent', None)
    venue.name = request.form['name']
    venue.genres = ','.join(request.form.getlist('genres'))
    venue.address = request.form['address']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.website = request.form['website']
    venue.facebook_link = request.form['facebook_link']
    venue.seeking_talent = True if seeking_talent != None else False
    venue.seeking_description = request.form['seeking_description']
    venue.image_link = request.form['image_link']
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    # on unsuccessful db insert, flash an error instead.
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  try:
    seeking_venues = request.form.get('seeking_venues', None)
    # Try to create a new Artist record and add to the db
    artist = Artist(  
      name = request.form['name'],
      genres = request.form.getlist('genres'),
      city = request.form['city'],
      state = request.form['state'],
      phone = request.form['phone'],
      website = request.form['website'],
      facebook_link = request.form['facebook_link'],
      seeking_venues = True if seeking_venues != None else False,
      seeking_description = request.form['seeking_description'],
      image_link = request.form['image_link']
    )
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    # on unsuccessful db insert, flash an error instead
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  data = []
  shows = Show.query.all()

  for show in shows: 
    data.append({
      "venue_id" : show.venue_id,
      "venue_name": Venue.query.filter_by(id=show.venue_id).first().name, 
      "artist_id": show.artist_id, 
      "artist_name": Artist.query.filter_by(id=show.artist_id).first().name, 
      "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
      "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead
  try:
    show = Show(
      venue_id = request.form['venue_id'],
      artist_id = request.form['artist_id'],
      start_time = request.form['start_time']
    )
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    # on unsuccessful db insert, flash an error instead
    db.session.rollback()
    flash('An error occurred, the show could not be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
