from flask import render_template, request, redirect, session, url_for,Flask
import hashlib
import uuid
from config import r,salted, secret_key
from db.connection import DB as db

from routes.bank import bank_bp
from routes.branch import branch_bp
from routes.vendor import vendor_bp
from routes.akun import akun_bp


akunColl = db.akunColl
bankColl = db.bankColl
branchColl = db.branchColl
vendorColl = db.vendorColl

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = secret_key

app.register_blueprint(vendor_bp)
app.register_blueprint(branch_bp)
app.register_blueprint(bank_bp)
app.register_blueprint(akun_bp)

def check_login():
    session_id = session.get('session_id')
    if session_id and r.get(session_id):
        return True
    else:
        return False    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if akunColl.find_one({'username': username}):
            return render_template('404.html')
        password += salted
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        new_user = {
            'username': username,
            'password': hashed_password,
            'roleid': 'user' 
        }
        akunColl.insert_one(new_user)
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/landing')
def landing():
    if not check_login():
        return redirect('/')
    session_id = session.get('session_id')
    current_user = r.get(session_id).decode('utf-8')
    user_data = akunColl.find_one({'username': current_user})
    user_role = user_data['roleid']
    return render_template('landing.html',user_role=user_role)

@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password += salted
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        userData= akunColl.find_one({'username' : username , 'password' : hashed_password})
        if userData:
            session_id= str(uuid.uuid4())
            r.set(session_id, username)
            session['session_id'] = session_id
            if userData['roleid'] == 'admin':
                return redirect(url_for('akun.admin'))
            elif userData['roleid'] == 'user':
                return redirect(url_for('akun.user'))
            elif userData['roleid'] == 'vendor':
                return redirect(url_for('vendor.vendors'))
            elif userData['roleid'] == 'branch':
                return redirect(url_for('branch.branchs'))
        else:
            return render_template('404.html')
    return render_template('login.html')
    
@app.route('/')
def clear_session():
    session_id = session.get('session_id')
    if session_id:
        r.delete(session_id)
        session.pop('session_id', None)
    return redirect('/login')

@app.route('/logout')
def logout():
    session_id = session.get('session_id')
    if session_id :
        r.delete(session_id)
        session.pop('session_id', None)
    return redirect('/login')

# if __name__ == "__main__" :
#     app.run(debug=True)