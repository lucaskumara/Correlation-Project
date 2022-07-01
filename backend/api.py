import requests
import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

def calc_pearson_coeff(x_values, x_avg, y_values, y_avg):
	'''Calulates the pearson coefficient of the two value sets.'''
	if x_avg is None or len(x_values) < 3:
		return None

	combined = zip(x_values, y_values)

	# Calculate numerator
	numerator = 0

	for x, y in combined:
		numerator += (x - x_avg) * (y - y_avg)

	# Calculate denominator
	sum1 = 0
	sum2 = 0

	for x in x_values:
		sum1 += (x - x_avg) ** 2
	
	for y in y_values:
		sum2 += (y - y_avg) ** 2

	denominator = (sum1 * sum2) ** .5

	return numerator / denominator

def high_low_avg(values):
	'''Iterates through the list of values and finds the high, low and average.'''
	if values == []:
		return {
			'high': None,
			'low': None,
			'average': None
		}

	high = float('-inf')
	low = float('inf')
	average = 0

	for value in values:
		high = max(high, value)
		low = min(low, value)
		average += value

	average /= len(values)

	return {
		'high': high, 
		'low': low, 
		'average': average
	}

def get_observations(data, start_date, end_date):
	'''Return a list of observations between the start and end dates.'''
	observations = []

	for observation in data['observations']:
		date = [int(value) for value in observation['d'].split('-')]
		date = datetime.datetime(date[0], date[1], date[2])

		if start_date <= date <= end_date:
			observations.append(observation)

	return observations

def fetch_usd_cad_data(start_date, end_date):
	'''Fetch USD/CAD rates from the Bank of Canada.'''
	response = requests.get('https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json')

	# Extract the relevant rates from the response
	filtered_observations = get_observations(response.json(), start_date, end_date)
	filtered_values = [float(observation['FXUSDCAD']['v']) for observation in filtered_observations]

	return filtered_values

def fetch_corra_data(start_date, end_date):
	'''Fetch the CORRA rates from the Bank of Canada.'''
	response = requests.get('https://www.bankofcanada.ca/valet/observations/AVG.INTWO/json')

	# Extract the relevant rates from the response
	filtered_observations = get_observations(response.json(), start_date, end_date)
	filtered_values = [float(observation['AVG.INTWO']['v']) for observation in filtered_observations]

	return filtered_values

def parse_data(request_data):
	'''Parse request data into datetime objects.'''
	start = [int(value) for value in request_data['start'].split('-')]
	start = datetime.datetime(start[0], start[1], start[2])

	end = [int(value) for value in request_data['end'].split('-')]
	end = datetime.datetime(end[0], end[1], end[2])

	return start, end	

@app.route('/api', methods=['POST'])
def main():
	request_data = request.get_json()
	start, end = parse_data(request_data)

	# Get rates and calculate values
	usd_cad_values = fetch_usd_cad_data(start, end)
	corra_values = fetch_corra_data(start, end)

	usd_cad_data = high_low_avg(usd_cad_values)
	corra_data = high_low_avg(corra_values)
	pearson_coeff = calc_pearson_coeff(usd_cad_values, usd_cad_data['average'], corra_values, corra_data['average'])

	return {
		'usd/cad': usd_cad_data,
		'corra': corra_data,
		'pearson_coeff': pearson_coeff
	}