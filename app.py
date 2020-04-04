from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd

df = pd.read_csv('statewise_indian_poppulation.csv')

def get_info(state):
    """gets info that has to return to api user"""
    x = df[df['State or union territory'] == state] # dataframe for given state
    state = str(x['State or union territory']).split('\n')[0].split('    ')[1]
    population = str(x['Population']).split('\n')[0].split('    ')[1]
    decadal_growth = str(x['Decadal growth']).split('\n')[0].split('    ')[1]
    rural_population = str(x['Rural population']).split('\n')[0].split('    ')[1]
    urban_population = str(x['Urban population']).split('\n')[0].split('    ')[1]
    area = str(x['Area']).split('\n')[0].split('    ')[1].split('\xa0km2\xa0')[0] + ' sq. Km'
    density = str(x['Density']).split('\n')[0].split('    ')[1].split('/km2\xa0')[0] + ' /sq. km'
    sex_ratio = str(x['Sex ratio']).split('\n')[0].split('    ')[1].split('/km2\xa0')[0] + ' females /1000 males'
    return {'state': state, 'population': population, 'decadal growth': decadal_growth,
    'rural population': rural_population, 'urban population': urban_population,
    'area': area, 'density': density, 'sex ratio': sex_ratio}

def state_exists(state):
    """see if state given in api call exists in csv file"""
    for i in df['State or union territory']:
        if i == state:
            return True
    return False

def case_fix(state):
    """convert 1st letter to uppercase and rest to lowercase"""
    first = state[0]
    first = first.upper()
    rest = state[1:]
    rest = rest.lower()
    return first+rest

app = Flask(__name__)
api = Api(app)

# Parser is used to accept multiple arguments in a request
parser = reqparse.RequestParser()
parser.add_argument('state', type=str, required=True)

class Population(Resource):

    def __init__(self):
        self.state = parser.parse_args().get('state')
        self.state = case_fix(self.state)
    
    def get(self):
        if state_exists(self.state):
            return {'message': 'success', 'info': get_info(self.state) }
        else:  
            return {'message': 'failure'}

api.add_resource(Population, '/')

# if __name__ == "__main__":
#     app.run(debug=True) 