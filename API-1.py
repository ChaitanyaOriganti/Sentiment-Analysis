

import pickle
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import re
    
@view_config(renderer='json')
def get_sentiment(request):
    text1 = request.params.get('text', 'No Name Provided')
    Dict={}
    Dict['Text']=text1
    text1 = re.sub('[^a-zA-Z\ ]', '', text1)
    text1 = text1.lower()
    text1 = text1.split()
    text1 = ' '.join(text1)
    text1 = cv.transform([text1]).toarray()
    text1 = tfidfconverter.transform(text1).toarray()
    label = classifier.predict(text1)[0]
    if(label==0):
        Dict['AirLine_Sentiment'] = 'Negative'
    else:
        Dict['AirLine_Sentiment'] = 'Positive'
    return Dict    

classifier = pickle.load(open('finalized_model.sav', 'rb'))
cv = pickle.load(open('vectorizer.pickle', 'rb')) 
tfidfconverter = pickle.load(open('tfidfconverter.pickle', 'rb')) 
config = Configurator()
config.add_route('sentiment', u'/sentiment')
config.add_view(get_sentiment, route_name='sentiment',renderer='json')
app = config.make_wsgi_app()
server = make_server('0.0.0.0', 6543, app)
print('Server has started, hit the request')
server.serve_forever()
