# snapfood_api
- snapfood_api is a simple wrapper API that uses Google Cloud Vision API and the Food API by Spoonacular. 
- It provides the backend for the mobile app "SnapFood", which allows users to snap pictures of their ingredients and to instantly receive a list of recipes.

# Implementation
- Used Google Cloud Vision API to take perform image recognition on user-inputted images of ingredients.  
- Used Spponacular's Food API to search for at most recipes that correspond to this ingredient.
- Used Flask as a framework, and deployed the app on Kubernetes.
