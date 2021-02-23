from flask import Flask, render_template, request,session, redirect, url_for, g
import model

app = Flask(__name__)
app.secret_key='mybekbosecretkey'

username=''
user=model.check_users()
admin_username=''

@app.before_request
def before_request():
    g.username=None
    g.admin_username=None
    if 'username' in session:
        g.username=session['username']
    if 'admin_username' in session:
        g.admin_username=session['admin_username']


@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        g.user=session['username']
        return redirect('dashboard')
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html') 

@app.route('/terms_of_use', methods=['GET'])
def terms_of_use():
    return render_template('terms_of_use.html') 

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html') 


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        if request.method=='POST':
            name=request.form['username']
            password=request.form['password']
            password=password.replace("'","''")
            if "'" in name or '"' in name:
                error_message="User is not allowed! Try again!"
                return render_template('signup.html', message=error_message)
            else:
                message=model.signup(name, password)
                return render_template('signup.html', message=message)
        else:
            return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        session.pop('username', None)
        username=request.form['username']
        password= request.form['password']
        username=username.replace("'","''")
        password=password.replace("'","''")
        password_check=model.check_password(username)
        if password==password_check:
            session['username']= request.form['username']
            return redirect(url_for('dashboard'))
        else:
            error_message='Oops, login failed!'
            return render_template('login.html',message=error_message)
    else:
        return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method=='POST':
        listname=request.form['listname']
        created_by=session['username']
        username=session['username']
        lists=model.get_lists(username)
        if listname !='' :
            list_add=model.list_add(listname, created_by)
            if list_add=='':
                lists=model.get_lists(username)
                return render_template('dashboard.html', username=username, list_items=lists)
            else:
                return render_template('dashboard.html', username=username, list_eror=list_add,list_items=lists)
        else:
            return render_template('dashboard.html', username=username, list_eror="Your task is empty",list_items=lists)
    else:
        if 'username' in session:
            username=session['username']
            lists=model.get_lists(username)
            return render_template('dashboard.html', username=username,list_items=lists)
        else:
            return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('dashboard')) 

@app.route('/logout/admin', methods=['GET'])
def admin_logout():
    if 'admin_username' in session:
        session.pop('admin_username', None)
        return redirect(url_for('admin_login'))
    else:
        return render_template('admin_login.html')


@app.route('/list/delete/<int:id>', methods=['GET'])
def deleteList(id):
    if 'username' in session:
        username = session['username']
        list_name_for_database = id
        model.deleteList(list_name_for_database, username)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/list/done/<int:id>', methods=['GET'])
def doneList(id):
    if 'username' in session:
        username = session['username']
        done = id
        model.doneList(done, username)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/delete_all/<string:username>', methods=['GET'])
def deleteAllLists(username):
    if 'username' in session:
        username = session['username']
        model.deleteAllLists( username)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/list/change/<int:id>', methods=['GET'])
def changeList(id):
    if 'username' in session:
        username = session['username']
        print(request.json)
        #model.changeList(id,new_name)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_username' in session:
        return redirect(url_for('admin_dashboard'))
    else:
        if request.method=='POST':
            admin_name=request.form['admin_username']
            password=request.form['password']
            admin_name=admin_name.replace("'","''")
            password=password.replace("'","''")
            password_db=model.check_admin(admin_name)
            if password==password_db:
                session['admin_username']= request.form['admin_username']
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('admin_login.html', message='Qate bar')
        else:
             return render_template('admin_login.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin_username' in session:
        total_users=model.get_total_users()
        total_users_24=model.get_total_users_24()
        total_lists=model.get_total_lists()
        total_lists_24=model.get_total_lists_24()
        total_users_all=model.get_total_users_all()
        total_users_24_all=model.get_total_users_24_all()
        total_lists_all=model.get_total_lists_all()
        total_lists_24_all=model.get_total_lists_24_all()
        admin_username=session['admin_username']
        return render_template('admin_dashboard.html',admin_username=admin_username,
        total_lists_24=total_lists_24,total_users=total_users,
        total_lists=total_lists,total_users_24=total_users_24,
        total_lists_24_all=total_lists_24_all,total_users_all=total_users_all,
        total_lists_all=total_lists_all,total_users_24_all=total_users_24_all)
    else:
        return render_template('admin_login.html')



if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

