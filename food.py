from flask import Flask
from flask import request, jsonify
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.request import urlopen
import requests
import json
import cgi


app = Flask(__name__)

@app.route("/recipe", methods=["GET"])
def recipe():
    print ("in get request")
    searchQuery = request.args.get("search")
    print(searchQuery)

    searchURL = "http://allrecipes.com/search/results/"
    #query = "fish tacos"
    htmlQuery = cgi.escape(searchQuery)
    params = { 'wt': htmlQuery,
                       'sort': 're' }
    paramsURL = urlencode(params)
    fullURL = searchURL + "?" + paramsURL 

    print(fullURL)
    content = urlopen(fullURL)
    soup = BeautifulSoup(content, "lxml")

    print('a')
    result = soup.find(id="searchResultsApp")
    result = result.find("section")

    print('b')
    results = result.find_all("article", class_="grid-col--fixed-tiles")
    article = results[0]
    if len(article["class"]) > 1:
        article = results[1]

    #print(article)
    recipe = article.find("ar-save-item")
    recipeId = recipe["data-id"]
    recipeName = recipe["data-name"]
    imgURL = recipe["data-imageurl"]
    imgURL = imgURL[1:len(imgURL)-1]
    print(imgURL)
    #print(recipeId)
    #name = urlencode({'':recipeName})
    #name = name[4:len(name)-3]
    name = recipeName.replace(" ", "-")
    name = name.lower()
    name = name[1:len(name)-1]
    #print(name)
    apiURL = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/extract"
    recipeURL = "http://allrecipes.com/recipe/" + recipeId + "/" + name + "/"
    print(recipeURL)
    params = { 'forceExtraction' : 'false',
                       'url' : recipeURL }
    paramsURL = urlencode(params)
    fullURL = apiURL + "?" + paramsURL
    #print( fullURL)
    headers = { "X-Mashape-Key" : "S18mBl6ic7mshE268UpSDu4JPgRGp1YnVhHjsn71LviY0rlTVC"}


    r = requests.get(fullURL, headers=headers)
    print ('\nr')
    print(r.json())

    dishJson = r.json()

    title = dishJson['title']
    print(title)

    directions = dishJson['text'] 
    print(directions)
    directions = directions.split('        ')

    print('before ingredients')

    ingredients = dishJson['extendedIngredients']
    #print (ingredients)
    ingredientStrings = []
    for i in ingredients:
        ingredientStrings.append(i['originalString'])
        print(ingredientStrings)

    return jsonify({
        'title': title,
        'imgURL': imgURL,
        'directions': directions,
        'ingredients': ingredientStrings })




if __name__ == "__main__":
    app.run()
