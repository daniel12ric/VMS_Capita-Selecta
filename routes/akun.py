from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from controller.akun_control import AkunModel, akunColl
from config import r

akun_bp = Blueprint('akun', __name__)
akun_model = AkunModel()


def check_login():
    session_id = session.get('session_id')
    if session_id and r.get(session_id):
        return True
    return False

def is_admin():
    session_id = session.get('session_id')
    if session_id:
        current_username = r.get(session_id).decode('utf-8')
        user_data = akunColl.find_one({'username': current_username})
        return user_data and user_data['roleid'] == 'admin'
    return False

@akun_bp.route('/manage_akun', methods=['GET'])
def manage_akun():
    if not check_login() or not is_admin():
        return redirect('/')
    akun = akun_model.get_all()
    return render_template("user-admin.html", akun=akun)


@akun_bp.route("/get-akun", methods=["GET"])
def get_akun():
    if not check_login() or not is_admin():
        return redirect('/')
    try:
        akunn = akun_model.get_all()
        for akun in akunn:
            akun["username"] = str(akun["username"])
        return jsonify({"data": akunn})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@akun_bp.route("/edit-akun/<username>", methods=["GET", "POST"])
def edit_akun(username):
    if not check_login() or not is_admin():
        return redirect('/')
    
    if username == "admin":
        flash("Akun 'admin' tidak bisa diedit.", "danger")
        return redirect(url_for("akun.manage_akun")) 
    
    if request.method == "GET":
        try:
            akun = akun_model.get_all()
            selected_akun = next((a for a in akun if a['username'] == username), None)
            if not selected_akun:
                return redirect(url_for("akun_bp.manage_akun")) 
            return render_template("edit-akun.html", akun=selected_akun)
        except Exception as e:
            return redirect(url_for("akun_bp.manage_akun")) 

    if request.method == "POST":
        try:
            new_role = request.form.get("roleid")
            result = akun_model.update_role(username, new_role)
            if result.get("success"):
                return redirect(url_for("akun.manage_akun"))
            else:
                return redirect(url_for("akun_bp.edit_akun", username=username)) 
        except Exception as e:
            return redirect(url_for("akun.edit_akun", username=username)) 

@akun_bp.route('/delete-akun/<username>', methods=['POST'])
def delete_akun(username):
    if not check_login() or not is_admin():
        return redirect('/')
    if username == "admin":
        flash("Akun 'admin' tidak bisa dihapus.", "danger")
        return redirect(url_for("akun.manage_akun")) 
        
    result = akun_model.delete(username)
    if result["success"]:
        flash(result["message"], "success")
    else:
        flash(result["message"], "danger")

    return redirect(url_for('akun_bp.get_all_akun'))

@akun_bp.route('/admin', methods=['GET'])
def admin():
    if not check_login() or not is_admin():
        return redirect('/login')
    users = list(akunColl.find())
    session_id = session.get('session_id')
    current_user = r.get(session_id).decode('utf-8')
    return render_template('index.html',  users=users, username=current_user.upper())
    
@akun_bp.route('/user')
def user():
    if not check_login():
        return redirect('/login')
    users = list(akunColl.find())
    session_id = session.get('session_id')
    current_user = r.get(session_id).decode('utf-8')
    return render_template('index2.html',  users=users, username=current_user.upper())