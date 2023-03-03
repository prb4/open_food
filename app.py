from flask import Flask, request, abort, make_response

import pdb
import redis
import meal_api

app = Flask(__name__)

prompt = "What is a 15 minute keto meal? Include the source at the end"

#As part of the saving process, loop thru the ingredients and the meal type (ie: keto) and time, and add the meal ID to a list/set of each.  This way, when future requests are made, an id can be pulled from "requirement" (ie: chicken), and kept till it is made sure that all futher requirements are met (ie; its also in the 15 minute time line)

def get_ingredients(meal):
    ingredients_prompt = "Pull the ingredients out of this recipe: {}".format(meal['choices'][0]['text'])
    ingredients = meal_api.meal(ingredients_prompt)

    return ingredients
 
def save_meal(openapi_id, recipe, ingredients, user_id):
    storage = redis.StrictRedis()
    storage.hset(openapi_id, "recipe", recipe)
    storage.hset(openapi_id, "ingredients", ingredients)

    storage.rpush(user_id, openapi_id)

def success():
    return "200"

@app.route("/login", methods=["POST"])
def login():
    if not request.method == "POST":
        abort(404)

    print("[+] Login successful")
    return success()

@app.route("/meal", methods=["GET"])
def main_page():
    if request.method == "GET":
        data = request.get_data()

        #TODO - make/get legitamate user_id
        #user_id = data["user_id"]
        user_id = "user_id_1"

        meal = meal_api.meal(prompt)

        ingredients = get_ingredients(meal) 

        data = {}
        data["id"] = meal["id"]
        data["recipe"] = meal['choices'][0]['text'].split("\n")[:-1]
        data["recipe"] = "\n".join(data["recipe"])

        data["ingredients"] = ingredients['choices'][0]['text']
        data["source"] = data["recipe"].split("\n")[-1]

        save_meal(data["id"], data["recipe"], data["ingredients"], user_id)

        return make_response(data)
        
    else:
        return abort(404)

    return success()

@app.route("/", methods=["GET"])
def index():
    return success()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)
