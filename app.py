from flask import Flask, request, abort, make_response
import hashlib
import pprint

import pdb
import redis
import meal_api

app = Flask(__name__)

prompt = "What is a 15 minute keto meal? Show the title at the top, then the directions, then the ingredients, and the source at the end."

#As part of the saving process, loop thru the ingredients and the meal type (ie: keto) and time, and add the meal ID to a list/set of each.  This way, when future requests are made, an id can be pulled from "requirement" (ie: chicken), and kept till it is made sure that all futher requirements are met (ie; its also in the 15 minute time line)

class Helper():
    #TODO Track session by session/cookie in case user is logged in at more than one location
    def __init__(self, redisHost="localhost"):
        self.storage = redis.StrictRedis(host=redisHost)

    def save_meal(self, recipe, ingredients, source, user_id, meal_hash):
        #Save the ingredients and recipe by the hash
        self.storage.hset(meal_hash, "recipe", recipe.encode())
        self.storage.hset(meal_hash, "ingredients", ingredients.encode())
        self.storage.hset(meal_hash, "source", source.encode())

        #Link the meal/hash with the user's account
        self.storage.rpush(user_id, meal_hash)

        self.link_meal_with_ingredients(meal_hash, ingredients.split("\n"))

        self.storage.incr("total_sents:{}".format(meal_hash))

    def link_meal_with_ingredients(self, meal_hash, ingredients):
        for ingredient in ingredients:
            self.storage.sadd(ingredient, meal_hash)
            print("[-] Added {} to {}".format(meal_hash, ingredient))

    def hash_recipe(self, recipe):
    #Hash the recipe for later look ups
        m = hashlib.sha256()
        m.update(recipe.encode())
        return m.hexdigest() 

    def normalize_items(self, items):
        final_items = []
        for item in items:
            item = item.strip()

            if item.startswith("-"):
                item = item[1:]

            if item.endswith("-"):
                item = item[:-1]

            if item.lower() == "ingredients" or item.lower() == "ingredients:":
                continue

            if item.lower() == "directions" or item.lower() == "directions:":
                continue

            if item == '' or item == '\n':
                continue

            item = item.strip()

            final_items.append(item)

        return final_items

    def extract_info(self, meal):
        meal_list = meal.split("\n")
        name = meal_list[0]

        directions_index = 0
        ingredients_index = 0
        origin_index = 0

        for i in range(len(meal_list[1:])):
            if "directions" in meal_list[1+i].lower():
                directions_index = 1 + i
                continue

            elif "ingredients" in meal_list[1+i].lower():
                ingredients_index = 1 + i
                continue

            elif "source" in meal_list[1+i].lower():
                origin_index = 1 + i
                continue
                
        directions = meal_list[directions_index+1:ingredients_index]
        ingredients = meal_list[ingredients_index+1:origin_index]
        if origin_index == len(meal_list) - 1:
            origin = meal_list[origin_index].replace("Source: ","")
        else:
            print("[!] Need to get origin")
            pdb.set_trace()

        return name, directions, ingredients, origin

def success():
    return "200"

@app.route("/login", methods=["POST"])
def login():
#The user will log in and initiate a session - users data should move into cache at this point
    if not request.method == "POST":
        abort(404)

    print("[+] Login successful")
    return success()

@app.route("/meal", methods=["GET"])
def main_page():
    if request.method == "GET":
        helper = Helper()

        data = request.get_data()

        #TODO - Look up session with user id
        #user_id = convert_session_to_user(data['session_cookie'])
        user_id = "user_id_1"

        #Get the meal
        meal = meal_api.meal(prompt)
        print(meal['choices'][0]['text'])

        #Pull out the source and meal
        name, recipe, ingredients, origin = helper.extract_info(meal['choices'][0]['text'].strip())

        #Hash recipe
        meal_hash = helper.hash_recipe("\n".join(recipe))

        #Get the ingredients from the meal
        #ingredients = helper.get_ingredients(recipe, meal_hash) 
        #ingredients = ingredients['choices'][0]['text'].strip().split("\n")
        ingredients = helper.normalize_items(ingredients)
        recipe = helper.normalize_items(recipe)

        data = {}
        data["name"] = name
        data["recipe"] = recipe
        data["ingredients"] = ingredients
        data["source"] = origin
        data['hash'] = meal_hash

        pprint.pprint(data)

        helper.save_meal("\n".join(data["recipe"]), "\n".join(data["ingredients"]), "\n".join(data['source']), user_id, meal_hash)

        return make_response(data)
        
    else:
        return abort(404)

    return success()

@app.route("/", methods=["GET"])
def index():
    return success()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)
