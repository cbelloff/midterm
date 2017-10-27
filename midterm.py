
from flask import Flask, request, render_template, make_response, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html')

@app.route('/')
def home_page():
    return redirect(url_for('cookie'))

# This route is a good example
@app.route('/user/<name>')
def hello_user(name):
   return '<h1>Hello {0}</h1>'.format(name)


@app.route('/form',methods= ['POST','GET'])
def enter_data():
    return render_template("age.html")

class SmuckersForm(FlaskForm):
    name= StringField('Enter your name if you want the link to the Williard Scott Birthday form', validators=[Required()])
    submit= SubmitField('Submit')

@app.route('/result',methods = ['POST', 'GET'])
def res():
    simpleForm=SmuckersForm()
    if request.method == 'GET':
        cookie_value=request.cookies.get('redirected')
        result = request.args
        name = result.get('name')
        birth = result.get('birthday')
        year=birth[:4]
        curr = result.get('current')
        curryear=curr[:4]
        new= 100 - (int(curryear) - int(year))
        neww=str(new)
        data = {
            'result_string':neww,
            'name':name,
            'age':new,
            'cookie':cookie_value
        }
        response = make_response(render_template("result.html",result = data, form=simpleForm))  
        return response

@app.route('/result2',methods= ['GET', 'POST'])
def result2():
    form=SmuckersForm(request.form)
    print (form.name.data)
    if request.method== 'POST' and form.validate_on_submit():
        name=form.name.data
        x= "{0}, get ready to be on-air to celebrate this huge milestone!".format(name)
        return render_template("random.html", result = x)
    flash('You clicked submit without entering your name! Try again!')
    return redirect(url_for('enter_data'))

        
@app.route('/set_cookie')
def cookie():
    redirect_to_form = redirect('/form')
    response = make_response(redirect_to_form )  
    response.set_cookie('redirected',value='True')
    return response

@app.route('/cakes')
def cakes():
    return render_template("cakes.html")    


if __name__ == '__main__':
    app.run()


    #done