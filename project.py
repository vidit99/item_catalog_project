import requests
from flask import render_template
from flask import request
from oauth2client.client import FlowExchangeError
from flask import redirect
from flask import jsonify
import random
from flask import Flask 
from flask import url_for
import httplib2
from flask import flash
import string
from sqlalchemy import create_engine
from sqlalchemy import asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base
import json
from database_setup import Cloth
from database_setup import Item
from flask import make_response
from database_setup import Vidit
from flask import session as timelogin
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import AccessTokenCredentials

app = Flask(__name__)

CLIENT_ID = json.loads(open('vidi.json', 'r').read())['web']['client_id']  #picking client_id from vidi.json
APPLICATION_NAME = "Cloth Menu Application"

engine = create_engine('sqlite:///restaurantmenuwithusers.db') #connection to database
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/gdisconnect')  # code to logout from gmail
def gdisconnect():
    infor = timelogin.get('credentials') 
    if infor is None:
        behave = make_response(
            json.dumps('oops user currently not connected . please connect again '), 401)
        behave.headers['Content-Type'] = 'application/json'
        return behave
    access_token = infor
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del timelogin['credentials']
        del timelogin['gplus_id']
        del timelogin['username']
        del timelogin['email']
        del timelogin['picture']

        behave = make_response(json.dumps('Successfully disconnected.'), 200)
	behave = make_response(redirect(url_for('branddisplay')))    
    	behave.headers['Content-Type'] = 'application/json'
        return behave
    else:
        behave = make_response(
            json.dumps('oops failed', 400)) # oops token invalid
        behave.headers['Content-Type'] = 'application/json'
        return behave


@app.route('/login')
def Login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    timelogin['state'] = state
    return render_template('gmailconn.html', STATE=state)


def createUser(timelogin): # database user functions
    acc_new = Vidit(name=timelogin['username'], email=timelogin[
                   'email'], picture=timelogin['picture'])
    session.add(acc_new)
    session.commit()
    acc_user = session.query(Vidit).filter_by(email=timelogin['email']).one()
    return acc_user.id


def getUserInfo(user_id):
    acc_user = session.query(Vidit).filter_by(id=user_id).one()
    return acc_user


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(cloth_id):
    restaurant = session.query(Cloth).filter_by(id=cloth_id).one()
    things = session.query(Item).filter_by(
        cloth_id=cloth_id).all()
    return jsonify(MenuItems=[i.serialize for i in things])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    itemmenu = session.query(Item).filter_by(id=menu_id).one()
    return jsonify(itemmenu=itemmenu.serialize)


@app.route('/restaurant/JSON')
def restaurantsJSON():
    brands = session.query(Cloth).all()
    return jsonify(brands=[r.serialize for r in brands])

def getUserID(email):
    try:
        acc_user = session.query(Vidit).filter_by(email=email).one()
        return acc_user.id
    except:
        return None

@app.route('/')
@app.route('/restaurant/')
def branddisplay():  # code to display all brands 
    restaurants = session.query(Cloth).order_by(asc(Cloth.name))
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def brandnew():   # code to create a new brand
    if 'username' not in timelogin:
        return redirect('/login')
    if request.method == 'POST':
        brandnew = Cloth(name=request.form['name'], user_id=timelogin['user_id'])
        session.add(brandnew)
        flash('Cloth %s Created' % brandnew.name)
        session.commit()
        return redirect(url_for('branddisplay'))   #  redirect to branddisplay Function 
    else:
        return render_template('brandnew.html')  # move to brandnew.html


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def brandedit(restaurant_id):  # code to edit a brand
    if 'username' not in timelogin:
        return redirect('/login')
    brandedi = session.query(
        Cloth).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            brandedi.name = request.form['name']
            flash('Cloth %s edited' % brandedi.name )
            return redirect(url_for('branddisplay'))   #  redirect to branddisplay Function 
    else:
        return render_template('brandedit.html', restaurant=brandedi)  # move to brandedit.html


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def branddel(restaurant_id): # code to delete a brand
    if 'username' not in timelogin:
        return redirect('/login')
    delrest = session.query(
        Cloth).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(delrest)
        flash('%s Successfully Deleted' % delrest.name)
        session.commit()
        return redirect(url_for('branddisplay', restaurant_id=restaurant_id))   #  redirect to branddisplay Function 
    else:
        return render_template('branddel.html', restaurant=delrest)  # move to branddel.html


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def menuList(restaurant_id):   # code to show brand names 
    restaurant = session.query(Cloth).filter_by(id=restaurant_id).one()
    items = session.query(Item).filter_by(restaurant_id=restaurant_id).all()
    return render_template('brands.html', items=items, restaurant=restaurant)  # move to brands.html

@app.route('/gconnect', methods=['POST'])
def gconnect():  # connect to gmail account
    if request.args.get('state') != timelogin['state']:  # check for token
        behave = make_response(json.dumps('Invalid state parameter.'), 401)
        behave.headers['Content-Type'] = 'application/json'
        return behave
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('vidi.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        infor = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        behave = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        behave.headers['Content-Type'] = 'application/json'
        return behave

    access_token = infor.access_token  # Check whether access token is valid.
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        behave = make_response(json.dumps(result.get('error')), 500)
        behave.headers['Content-Type'] = 'application/json'
        return behave

    # Verify that the access token is used for the intended user.
    gplus_id = infor.id_token['sub']
    if result['user_id'] != gplus_id:
        behave = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        behave.headers['Content-Type'] = 'application/json'
        return behave

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        behave = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        behave.headers['Content-Type'] = 'application/json'
        return behave

    stored_credentials = timelogin.get('credentials')
    stored_gplus_id = timelogin.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        behave = make_response(json.dumps('Current user is already connected.'),
                                 200)
        behave.headers['Content-Type'] = 'application/json'
        return behave

    
    timelogin['credentials'] = infor.access_token # It stores the access_token to be used later
    timelogin['gplus_id'] = gplus_id
    access_token = AccessTokenCredentials(timelogin['credentials'], 'user-agent-value') # used for returning credential object

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': infor.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    timelogin['username'] = data['name']
    timelogin['picture'] = data['picture']
    timelogin['email'] = data['email']

    user_id = getUserID(timelogin['email'])		#check whether user exist
    if not user_id:		
	    user_id = createUser(timelogin)		
    timelogin['user_id'] = user_id	

    output = ''
    output += '<h1>Welcome, '
    output += timelogin['username']
    output += '!</h1>'
    output += '<img src="'
    output += timelogin['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % timelogin['username'])
    print "done!"
    return output

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def itemnew(restaurant_id):  # code for new menu item 
    if 'username' not in timelogin:
        return redirect('/login')
    restaurant = session.query(Cloth).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        addit = Item(name=request.form['name'], description=request.form['description'],
		price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id, user_id=restaurant.user_id)
        session.add(addit)
        session.commit()
        flash('menu tem %s created' % (addit.name))
        return redirect(url_for('menuList', restaurant_id=restaurant_id))  # redirect to menuList Function 
    else:
        return render_template('itemnew.html', restaurant_id=restaurant_id)  # shift to itemnew.html page


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def itemeditm(restaurant_id, menu_id): # menu item edit
    if 'username' not in timelogin:
        return redirect('/login')
    itemedit = session.query(Item).filter_by(id=menu_id).one()
    restaurant = session.query(Cloth).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            itemedit.name = request.form['name']
        if request.form['description']:
            itemedit.description = request.form['description']
        if request.form['price']:
            itemedit.price = request.form['price']
        if request.form['course']:
            itemedit.course = request.form['course']
        session.add(itemedit)
        session.commit()
        flash('udated menu item')
        return redirect(url_for('menuList', restaurant_id=restaurant_id))  # redirect to menuList Function 
    else:
        return render_template('itemedit.html', restaurant_id=restaurant_id, menu_id=menu_id, item=itemedit)   #shift to itemedit.html


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def itemdelete(restaurant_id, menu_id):  # code to delete item
    if 'username' not in timelogin:
        return redirect('/login')  
    restaurant = session.query(Cloth).filter_by(id=restaurant_id).one()
    removeitem = session.query(Item).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(removeitem)
        session.commit()
        flash('updated item menu')
        return redirect(url_for('menuList', restaurant_id=restaurant_id)) # redirect to menuList Function 
    else:
        return render_template('itemdel.html', item=removeitem)  #shift to itemdel.html page


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	 # run on localhost:5000