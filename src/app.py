from flask import Flask, request, jsonify
import functions as func


app = Flask(__name__)

# index page
@app.route('/', methods = ['GET'])
def index():
    return jsonify({"SnapFood API":"Hannah Lee(hl838)"})


# send images(in base64) in the request body to the server,
# and the list of recipes are shown in the browser
@app.route('/search', methods=['POST'])
def send_images():
    image_to_label = {}
    for key in request.form.keys():
        image = request.form[key]
        parsed_image = func.generate_img_json(image)
        annotations = func.get_annotations(parsed_image)
        image_to_label[key] = annotations
    return jsonify(image_to_label)

# Use ingredient names, the maximal number of recipes to return, and ranking in the request body
# ranking = Whether to maximize used ingredients (1) or minimize missing ingredients (2) first.
# to get the list of recipes
@app.route('/search', methods=['GET'])
def get_recipes():
    ingredient_list = request.args.getlist('ingredient')
    num_recipes = request.args.get("number")
    ranking = request.args.get("ranking")
    input_dict = {"ingredients": ingredient_list, "number": num_recipes, "ranking": ranking}
    recipes = func.get_recipes(input_dict)
    return jsonify(recipes)

# gets an analyzed breakdown of a recipe's instructions, given a recipe id
@app.route('/search/recipes', methods=['GET'])
def get_recipe_instructions():
    recipe_id = request.args.get("id")
    info = func.get_analyzed_recipe_info(recipe_id)
    return jsonify(info)

@app.route('/search/recipeinfo', methods=['GET'])
def get_recipe_info():
    recipe_id = request.args.get("id")
    info = func.get_recipe_info(recipe_id)
    return jsonify(info)
