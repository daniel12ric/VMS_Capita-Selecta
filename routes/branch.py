from flask import Blueprint, jsonify, request, render_template,session, redirect, url_for, flash
from controller.branch_control import BranchModel, akunColl
from config import r

branch_bp = Blueprint("branch", __name__)
branch_model = BranchModel()

def check_login():
    session_id = session.get('session_id')
    if session_id and r.get(session_id):
        return True
    else:
        return False
def is_admin():
    session_id = session.get('session_id')
    if session_id:
        current_username = r.get(session_id).decode('utf-8')
        user_data = akunColl.find_one({'username': current_username})
        return user_data and user_data['roleid'] == 'admin'
    return False      

@branch_bp.route("/add-branch", methods=["GET", "POST"])
def branch_create():
    if not check_login() or not is_admin():
        return redirect('/')
    session_id = session.get('session_id')
    username = r.get(session_id).decode('utf-8')
    if request.method == "POST":
        result = branch_model.create(username)
        if result.get("success"):
            flash("Branch berhasil ditambahkan!", "success")
            return redirect(url_for("branch.branch_admin"))
        else:
            flash(result.get("message", "Gagal menambahkan Branch"), "danger")
    return render_template("add-branch.html", action="create")

@branch_bp.route("/branch_admin", methods=["GET"])
def branch_admin():
    if not check_login() or not is_admin():
        return redirect('/')
    branch = branch_model.get_all()
    return render_template("branch_admin.html", branch=branch)

@branch_bp.route("/get-branch", methods=["GET"])
def get_branch():
    if not check_login():
        return redirect('/')
    try:
        branchs = branch_model.get_all()
        for branch in branchs:
            branch["_id"] = str(branch["_id"])
        return jsonify(branchs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@branch_bp.route("/edit-branch/<branch_id>", methods=["GET", "POST"])
def update_branch(branch_id):
    if not check_login() or not is_admin():
        return redirect('/')
    if request.method == "GET":
        branch = branch_model.find_one({"_id": (branch_id)})
        return render_template("edit-branch.html", action="update", branch=branch)

    if request.method == "POST":
        try:
            session_id = session.get('session_id')
            username = r.get(session_id).decode('utf-8')

            update_data = {
                "BranchName": request.form.get("BranchName"),
                "activeStatus": request.form.get("activeStatus")
            }
            result = branch_model.update(branch_id, update_data, username)
            if result.get("success"):
                flash("Branch berhasil ditambahkan!", "success")
            return redirect(url_for("branch.branch_admin"))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template("edit-branch.html", action="update", branch=branch)

@branch_bp.route("/delete-branch/<branch_id>", methods=["DELETE"])
def delete_branch(branch_id):
    if not check_login() or not is_admin():
        return redirect('/')
    try:
        result = branch_model.delete(branch_id)
        if result["success"]:
            return jsonify({"deleted_count": 1}), 200
        else:
            return jsonify({"deleted_count": 0, "message": result["message"]}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@branch_bp.route('/branch')
def branch_user():
    if not check_login():
        return redirect('/')
    return render_template('branch.html')

@branch_bp.route('/branchdor')
def branch_vendor():
    if not check_login():
        return redirect('/')
    return render_template('branch2.html')

@branch_bp.route('/branchs')
def branchs():
    if not check_login():
        return redirect('/login')
    users = list(akunColl.find())
    session_id = session.get('session_id')
    current_user = r.get(session_id).decode('utf-8')
    return render_template('index2.html',  users=users, username=current_user.upper())