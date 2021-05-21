from flask import Blueprint, request, render_template


blueprint = Blueprint('hello', __name__)


@blueprint.route('/', methods=['GET'])
def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    return render_template('hello_world.html', title='Flask App')
