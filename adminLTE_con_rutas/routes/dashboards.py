from flask import Blueprint, render_template

dashboard1_bp = Blueprint('dashboard1', __name__)
@dashboard1_bp.route('/index2.html')
def dashboard1():
    return render_template("index2.html")
dashboard2_bp = Blueprint('dashboard2', __name__)
@dashboard2_bp.route('/index3.html')
def dashboard2():
    return render_template("index3.html")