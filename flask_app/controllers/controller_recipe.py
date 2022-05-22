from flask_app import app
from flask import render_template, redirect, session, request

from flask_app.models import model_recipe, model_user

@app.route('/recipe/new')
def recipe_new():
    context = {
        'user': model_user.User.get_one({'id': session['uuid']})
    }
    return render_template('recipe_new.html', **context)

@app.route('/recipe/create', methods=['POST'])
def recipe_create():
    # validate
    if not model_recipe.Recipe.validate(request.form):
        return redirect('/recipe/new')
    # need to add user_id
    data = {
        **request.form,
        'user_id': session['uuid']
        
    }
    
    # add to database
    model_recipe.Recipe.create(data)
    return redirect('/')


@app.route('/recipe/<int:id>')
def recipe_show(id):
    context = {
        'user': model_user.User.get_one({'id': session['uuid']}),
        'recipe': model_recipe.Recipe.get_one({'id':id})
    }
    return render_template('recipe_show.html', **context)

@app.route('/recipe/<int:id>/edit')
def recipe_edit(id):
    recipe = model_recipe.Recipe.get_one({'id': id})
    if recipe.user_id != session['uuid']:
        return redirect('/')
    context = {
        'user': model_user.User.get_one({'id': session['uuid']}),
        'recipe': model_recipe.Recipe.get_one({'id':id})
    }
    return render_template('recipe_edit.html', **context)


@app.route('/recipe/<int:id>/update', methods=['POST'])
def recipe_update(id):
    recipe = model_recipe.Recipe.get_one({'id': id})
    if recipe.user_id != session['uuid']:
        return redirect('/')
    #validate
    if not model_recipe.Recipe.validate(request.form):
        return redirect(f'/recipe/{id}/edit')

    data = {
        **request.form,
        'id': id
    }
    model_recipe.Recipe.update_one(data)
    return redirect('/')


@app.route('/recipe/<int:id>/delete')
def recipe_delete(id):
    model_recipe.Recipe.delete_one({'id': id})
    return redirect('/')