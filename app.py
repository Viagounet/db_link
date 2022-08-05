import datetime

from firebasedatabase import FirebaseDatabase
from models import AnimeRecommendation, StoryRequest

db = FirebaseDatabase('credentials/myanimestory-882d3-firebase-adminsdk-41x5n-7e9fd9473a.json',
                      'https://myanimestory-882d3-default-rtdb.europe-west1.firebasedatabase.app/')


request = StoryRequest(story='The story of the day that never comes',
                       recommendations=[AnimeRecommendation(title='One Piece',
                                      story='The story of the day that never comes--',
                                      mal_score=9.5,
                                      similarity_score=9.1,
                                      global_score=9.3)],
                       date=datetime.datetime.now())

request.to_firebase(db)