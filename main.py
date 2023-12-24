from locations import locations
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import aiohttp
import asyncio
import json
from ant_colony import ant_colony_optimization_with_history, plot_distance_history, plot_graph

locationsGeoCodes = []
locationsMatrix = []

async def get_location_geocode(location, session, locationsGeoCodes):
    url = 'https://zeki-opt-e6841d5f67ed.herokuapp.com/getGeoCode'
    data = {'address': location}
    async with session.get(url, params=data) as response:
        result = await response.json()
        locationsGeoCodes[location] = result['geoCode']

async def get_locations_geocode(locations):
    locationsGeoCodes = {}
    async with aiohttp.ClientSession() as session:
        for location in locations:
            await get_location_geocode(location, session, locationsGeoCodes)
    response = [locationsGeoCodes[location] for location in locations]
    return response

async def get_matrix(locations, session):
    url = 'https://zeki-opt-e6841d5f67ed.herokuapp.com/getMatrix'
    data = {'locations': json.dumps(locations)}
    async with session.get(url, params=data) as response:
        result = await response.json()
        return convert_to_km_with_precision(result['matrix'])

def convert_to_km_with_precision(matrix):
    return [[round(distance / 1000, 2) for distance in row] for row in matrix]

async def main():
    async with aiohttp.ClientSession() as session:
        locationsGeoCodes = await get_locations_geocode(locations)
        locations_distances_matrix = await get_matrix(locationsGeoCodes, session)
        best_route, best_distance, distance_history = ant_colony_optimization_with_history(
        locations_distances_matrix, num_ants=5, num_iterations=100, alpha=1, beta=2, decay_rate=0.10, initial_pheromone=1.0)
        print("Best Route:", best_route)
        print("Best Distance:", best_distance)
        plot_distance_history(distance_history)
        plot_graph(best_route, locations_distances_matrix, locations)
        #print(locations_distances_matrix) -> to show matrix

if __name__ == "__main__":
    asyncio.run(main())
