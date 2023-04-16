# Your name: Luciana Solorzano
# Your student id: 82482379
# Your email: lusolorz@umich.edu
# List who you have worked with on this homework: NA

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest



def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, db)
    conn = sqlite3.connect(full_path)
    cur = conn.cursor()
    val = cur.execute(
        'SELECT restaurants.name, categories.category, buildings.building, restaurants.rating FROM restaurants INNER JOIN categories ON restaurants.category_id = categories.id INNER JOIN buildings ON restaurants.building_id = buildings.id'
    )
    mario = cur.fetchall()
    ret = {}
    for item in mario:
        temp = {}
        temp["category"] = item[1]
        temp["building"] = item[2]
        temp["rating"] = item[3]
        ret[item[0]] = temp
    return ret

    

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    betty = load_rest_data(db)
    ret = {}
    for item in betty:
        if betty[item]['category'] in ret:
            ret[betty[item]['category']] += 1
        else:
            ret[betty[item]['category']] = 1
    sortead =  sorted(ret.items(), key=lambda x:x[1])
    cats = []
    counts = []
    for item in sortead:
        cats.append(item[0])
        counts.append(item[1])

    plt.barh(cats, counts)
    plt.title("Number of each category")
    plt.ylabel('Restaurant Categories')
    plt.xlabel("Number of Restaurants")
    plt.show()
    return ret
    

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, db)
    conn = sqlite3.connect(full_path)
    cur = conn.cursor()
    val = cur.execute(
        'SELECT restaurants.name FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = ? ORDER BY restaurants.rating DESC', (building_num, )
    )
    mario_sr = cur.fetchall()
    ret = []
    for item in mario_sr:
        ret.append(item[0])
    return ret

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, db)
    conn = sqlite3.connect(full_path)
    cur = conn.cursor()
    val = cur.execute(
        'SELECT categories.category, restaurants.rating FROM restaurants JOIN categories ON restaurants.category_id = categories.id'
    )
    cat_to_ratings = cur.fetchall()
    dic_avg_rating = {}
    for item in cat_to_ratings:
        if item[0] in dic_avg_rating:
            dic_avg_rating[item[0]]['count'] += 1
            tem = dic_avg_rating[item[0]]['avg']
            dic_avg_rating[item[0]]['avg'] = (item[1] + tem)/dic_avg_rating[item[0]]['count']
        else:
            temp = {}
            dic_avg_rating[item[0]]['count'] = 1
            dic_avg_rating[item[0]]['avg'] = item[1]
   

    return 1

#Try calling your functions here
def main():
    one = load_rest_data('South_U_Restaurants.db')
    two = plot_rest_categories('South_U_Restaurants.db')
    three = find_rest_in_building(1140, 'South_U_Restaurants.db')
    four = get_highest_rating('South_U_Restaurants.db')

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        pass
        #highest_rating = get_highest_rating('South_U_Restaurants.db')
        #self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
