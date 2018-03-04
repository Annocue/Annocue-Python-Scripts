import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from jinja2 import Template

# UTILITIES
import utility.send as message
import utility.time as now
import utility.directory as directory

# PACKAGES
import script.event.nba
import script.investment.stock
import script.weather.forecast

path = directory.Relative('../config-python-scripts/config.json').path()
firebasePath = directory.Relative('../config-python-scripts/firebase.json').path()

# Load necessary credentials and settings
config = json.load(open(path))

# Initialize Firebase Admin client
cred = credentials.Certificate(firebasePath)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Get today's date
zone = now.Zone(*config['timeZone'])
currentDate = now.datetime.now(zone).strftime('%Y-%m-%d')

# Pull reference to collection of users
users_ref = db.collection('users')
docs = users_ref.get()

# Go through each user's doc and send their custom email
objList = {}
context = {}
for doc in docs:
    user = doc.to_dict()
    email = user['email']
    templates = Template(user['templates'])
    scripts = json.loads(user['scripts'])

    # Create list of scripts with their array of inputs
    for key in scripts:
        objList[key] = eval(key)(scripts[key]).data()
        keySplit = key.split('.')[1:]
        keySplit[1] = keySplit[1].capitalize()
        contextKey = ''.join(keySplit)
        context[contextKey] = objList[key]

    # Input required values for their template
    renderEmail = templates.render(context)

    # Send custom template rendered email
    message.Email(config['senderEmail'], config['senderPassword'], email, f'Annocue ({currentDate})', renderEmail).send()
