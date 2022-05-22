from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

from flask_app.models import model_user

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def create(cls, data:dict) -> int:
        query = "INSERT INTO recipes (recipe_name, description, instructions, date_made, under_thirty, user_id) VALUES (%(recipe_name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_thirty)s,%(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM recipes;"
        return connectToMySQL(DATABASE).query_db(query)
        if results:
            all_recipes = []
            for recipe in results:
                all_recipes.append(cls(recipe))
            return all_recipes
        return False

    # update   
    @classmethod
    def update_one(cls, data:dict) -> None:
        query = "UPDATE recipes SET recipe_name = %(recipe_name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_thirty = %(under_thirty)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # delete 
    @classmethod
    def delete_one(cls, data:dict) -> None:
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data:dict) -> bool:
        is_valid = True

        if len(data['recipe_name']) < 2:
            is_valid = False
            flash('Field is required', 'err_recipe_name')

        if len(data['description']) < 3:
            is_valid = False
            flash('Field is required', 'err_recipe_description')

        if len(data['instructions']) < 3:
            is_valid = False
            flash('Field is required', 'err_recipe_instructions')

        if len(data['date_made']) < 1:
            is_valid = False
            flash('Field is required', 'err_recipe_date_made_on')

        return is_valid
