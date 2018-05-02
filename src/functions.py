# 1. Gets the encoded image data and send to Google Cloud, return the
# [endpoint] = POST req
import json
import requests
import config

FOOD_API_KEY = config.FOOD_API_KEY
GOOGLE_API_KEY = config.GOOGLE_API_KEY


FOOD_API_URL = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients"
GOOGLE_CLOUD_VISION_URL = "https://vision.googleapis.com/v1/images:annotate"

# # 1. Prepares data for Google API
# - [input_img] = base64. [result_dict] = dictionary
# Parse input to json
def generate_img_json(input_img):
    result_dict ={"requests": [{"image": {"content": input_img},\
    "features": [{"type": "LABEL_DETECTION","maxResults": 5}]}]}
    return result_dict

# 2. Ask Google API to get annotations for the image
# [json_data]= [annotations] =
# - Pass the data to Google API and parse the result to return a dictionary of annotations
def get_annotations(data):

    response = requests.post("%s?key=%s" % (GOOGLE_CLOUD_VISION_URL, GOOGLE_API_KEY), \
    json.dumps(data), headers={'content-type': 'application/json'})

    annotations = json.loads(response.text)
    lst = []
    for i in annotations["responses"][0]["labelAnnotations"]:
        lst.append(i["description"])
    return lst

def get_recipes(data):
    ing_string = ""
    count = 0
    for ing in data['ingredients']:
        count += 1
        if count < len(data["ingredients"]):
            ing_string += (ing+"%2C")
        else:
            ing_string += ing

    payload = {"fillIngredients":"true", "ingredients":ing_string, "limitLicense":"false", \
    "number":data["number"], "ranking":data["ranking"]}

    header = {'X-Mashape-Key': FOOD_API_KEY, 'Accept': 'application/json'}

    response = requests.get(FOOD_API_URL, params = payload, headers=header)
    recipes = json.loads(response.text)
    return recipes

def get_analyzed_recipe_info(recipe_id):
    payload = {"stepBreakdown":"false"}
    header = {'X-Mashape-Key': FOOD_API_KEY, 'Accept': 'application/json'}
    response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"+recipe_id+"/analyzedInstructions", \
    params = payload, headers=header)

    info = json.loads(response.text)
    return info

def get_recipe_info(recipe_id):
    payload = {"includeNutrition":"true"}
    header = {'X-Mashape-Key': FOOD_API_KEY, 'Accept': 'application/json'}
    response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"+recipe_id+"/information", \
    params = payload, headers=header)

    info = json.loads(response.text)
    return info

# #GET Summarize Recipe
# def get_recipe_summary(recipe_id):
