"""Data handling file"""
class TempRecipes:
    """Recipe class"""
    __all_recipes = []
    def __init__(self):
        """Initialise class"""
        recipe_data = {}
        self.__all_recipes.append(recipe_data)
    def set_recipe(self, id, title, ingredients, steps, create_date, created_by):
        """Set the recipe variables"""
        recipe_data = {}
        recipe_data['id'] = id
        recipe_data['title'] = title
        recipe_data['ingredients'] = ingredients
        recipe_data['steps'] = steps
        recipe_data['create_date'] = create_date
        recipe_data['created_by'] = created_by
        self.__all_recipes = []
        self.__all_recipes.append(recipe_data)
    
    def get_recipes(self):
        """Get recipes"""
        return self.__all_recipes

class TempUser:
    """User class"""
    __all_users = []
    __user_data = {} 

    def __init__(self):
        """Initialise class"""
        user_data = {}
        self.__all_users.append(user_data)

    def set_user(self, id, name, username, email, password):
        """Set user"""
        self.__user_data['id'] = id
        self.__user_data['name'] = name
        self.__user_data['username'] = username
        self.__user_data['email'] = email
        self.__user_data['password'] = password
        self.__all_users.append(self.__user_data)

    def get_users(self):
        """Get Users"""
        return self.__all_users


    temp_users = TempUser()
    for user in users.items:
        temp_users.set_user(user.id, user.name, user.username, user.email, user.password)
        output = temp_users.get_users()

    return jsonify({'Users':output})