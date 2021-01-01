#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for
  )
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

#connect to a local postgresql database
migrate = Migrate(app, db)


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

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


# ----------------------------------------------------------------- 
# Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  data=[]
  venues=Venue.query.all()
  places=Venue.query.distinct(Venue.city, Venue.state).all()

  for place in places:
    data.append({
      'city':place.city,
      'state':place.state,
      'venues':[
        {
        'id':venue.id,
        'name':venue.name,
        } 
        for venue in venues if
          venue.city==place.city and venue.state ==place.state
      ]
    })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search=request.form.get('search_term')
  venues=Venue.query.filter(Venue.name.ilike(f"%{search}%")).all()
  response={'count':len(venues),'data':venues}

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue=Venue.query.filter_by(id=venue_id).first_or_404()
  #create new attributes for past and upcoming shows
  setattr(venue,'past_shows',[])
  setattr(venue,'upcoming_shows',[])

  past_shows=(
    db.session.query(Artist, Show).join(Show).join(Venue). \
      filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time < datetime.now()
      ).all()
    )

  upcoming_shows=(
    db.session.query(Artist, Show).join(Show).join(Venue). \
      filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time >= datetime.now()
      ).all()
    )

  data = {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "facebook_link": venue.facebook_link,
            "website": venue.website,
            "image_link": venue.image_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "upcoming_shows_count": len(upcoming_shows),
            "upcoming_shows":  [{
                                  'artist_id': artist.id,
                                  'artist_name': artist.name,
                                  'artist_image_link': artist.image_link,
                                  'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
                              } for artist, show in upcoming_shows],
            "past_shows": [{
                                'artist_id': artist.id,
                                "artist_name": artist.name,
                                "artist_image_link": artist.image_link,
                                "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
                            } for artist, show in past_shows],
            "past_shows_count": len(past_shows),

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
  error=False
  form = VenueForm(request.form)
  try:
      venue=Venue()
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()

  except Exception as e:
    error=True
    db.session.rollback()
    print(f'Exception occured -- {e}')

  finally:
    db.session.close()

  if error:
    flash(
      f'An error occured during insert'
      f'Venue {request.form["name"]} could not be added'
      'error'
    )
  else:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error=False
  venue=Venue.query.get(venue_id)
  # print(venue)

  try:
    db.session.delete(venue)
    db.session.commit()
  except Exception as e:
    error=True
    print(f'Exception occured -- {e}')
    db.session.rollback()
  finally:
    db.session.close()
  
  if error:
    flash(
      f'An error occured during delete'
      f'Venue {venue.name} could not be deleted'
      'error'
    )
  else:
    flash(f'Venue {venue.name} was successfully deleted')

  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  #artists query
  data=Artist.query.all()
 
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search=request.form.get('search_term')
  artists=Artist.query.filter(Artist.name.ilike(f'%{search}%')).all()
  response={'count':len(artists),'data':artists}

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  curr_date = datetime.now()
  artist = Artist.query.filter_by(id=artist_id).first_or_404()
  #create additional atributes to collect the shows info
  setattr(artist, 'past_shows', [])
  setattr(artist, 'upcoming_shows', [])


  past_shows=(
    db.session.query(Venue, Show).join(Show).join(Artist). \
      filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time < datetime.now()
      ).all()
    )

  upcoming_shows=(
    db.session.query(Venue, Show).join(Show).join(Artist). \
      filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time >= datetime.now()
      ).all()
    )

  data = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "facebook_link": artist.facebook_link,
            "website": artist.website,
            "image_link": artist.image_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "upcoming_shows_count": len(upcoming_shows),
            "upcoming_shows":  [{
                                  'venue_id': venue.id,
                                  'venue_name': venue.name,
                                  'venue_image_link': venue.image_link,
                                  'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
                              } for venue, show in upcoming_shows],
            "past_shows": [{
                                'venue_id': venue.id,
                                "venue_name": venue.name,
                                "venue_image_link": venue.image_link,
                                "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
                            } for venue, show in past_shows],
            "past_shows_count": len(past_shows),

        }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist=Artist.query.get(artist_id)  
  form = ArtistForm()
  #prepopulate form with the artist data
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  
  return render_template('forms/edit_artist.html', form=form, artist=artists)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error=False
  
  artist=Artist.query.get(artist_id)
  form=ArtistForm(request.form)
  
  if form.validate():

    try:
      artist.name=form.name.data
      artist.city=form.city.data
      artist.state=form.state.data
      artist.phone=form.phone.data 
      artist.genres=form.genres.data
      artist.facebook_link=form.facebook_link.data

      # Artist.update(artist)
      db.session.commit()
    
    except Exception as e:
      error=True
      print(f'Exception occured -- {e}')
      print(sys.exc_info())
      db.session.rollback()
    finally:
      db.session.close()
  
  if error:
    flash(
      f'An error occured during update'
      f'Artist {artist.name} could not be updated'
      f'{form.errors}'
    )
  else:
    flash(f'Artist {artist.name} was successfully updated!')
  
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue=Venue.query.get(venue_id)
  form = VenueForm()

  form.name.data =  venue.name
  form.genres.data =  venue.genres
  form.address.data =  venue.address
  form.city.data =  venue.city
  form.state.data =  venue.state
  form.phone.data =  venue.phone
  form.website.data =  venue.website
  form.facebook_link.data =  venue.facebook_link
  form.seeking_talent.data =  venue.seeking_talent
  form.seeking_description.data =  venue.seeking_description
  form.image_link.data =  venue.image_link

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error=False
  
  venue=Venue.query.get(venue_id)
  form=VenueForm(request.form)
  
  if form.validate():

    try:
      venue.name = form.name.data
      venue.genres = form.genres.data 
      venue.address = form.address.data 
      venue.city = form.city.data 
      venue.state = form.state.data 
      venue.phone = form.phone.data 
      venue.website = form.website.data 
      venue.facebook_link = form.facebook_link.data 
      venue.seeking_talent  =  form.seeking_talent.data
      venue.seeking_description  = form.seeking_description.data 
      venue.image_link =  form.image_link.data 

      # Venue.update(venue)
      db.session.commit()
    
    except Exception as e:
      error=True
      print(f'Exception occured -- {e}')
      print(sys.exc_info())
      db.session.rollback()
    finally:
      db.session.close()
  
  if error:
    flash(
      f'An error occured during update'
      f'Artist {venue.name} could not be updated'
      f'{form.errors}'
    )
  else:
    flash(f'Artist {venue.name} was successfully updated!')
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form --works
  error=False

  form=ArtistForm(request.form)
  try:
      artist=Artist()
      form.populate_obj(artist)
      db.session.add(artist)
      db.session.commit()

  except Exception as e:
    error=True
    db.session.rollback()
    print(f'Exception occured -- {e}')

  finally:
    db.session.close()

  if error:
    flash(
      f'An error occured during insert'
      f'Artist {request.form["name"]} could not be added'
      'error'
    )
  else:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  shows=Show.query.all()
  for show in shows:
    show.venue_name = Venue.query.get(show.venue_id).name
    artist =Artist.query.get(show.artist_id)
    show.artist_name=artist.name
    show.artist_image_link=artist.image_link
    show.start_time=str(show.start_time)

  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  error = False

  format = '%Y-%m-%d %H:%M:%S'
  
  form=ShowForm(request.form)
  try:
      show = Show()
      form.populate_obj(show)
      # show['start_time'] = datetime.strptime(data['start_time'], format)
      db.session.add(show)
      db.session.commit()
  except Exception as e:
      error = True
      db.session.rollback()
      print(f'Exception ==> {e}')
  finally:
      db.session.close()

  if error:
    flash(
      f'An error occured during insert '
      f'Show could not be added '
      'error'
    )
  else:
    # on successful db insert, flash success
    flash('Show ' + ' was successfully listed!')

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
