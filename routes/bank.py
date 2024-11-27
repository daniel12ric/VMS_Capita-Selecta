from flask import Blueprint, jsonify, request, render_template,session, redirect, url_for, flash
from controller.bank_control import BankModel, akunColl
from config import r

bank_bp = Blueprint("bank", __name__)
bank_model = BankModel()

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

@bank_bp.route("/add-bank", methods=["GET", "POST"])
def bank_create():
    if not check_login() or not is_admin():
        return redirect('/')
    session_id = session.get('session_id')
    username = r.get(session_id).decode('utf-8')
    if request.method == "POST":
        result = bank_model.create(username)
        if result.get("success"):
            flash("Bank berhasil ditambahkan!", "success")
            return redirect(url_for("bank.bank_admin"))
        else:
            flash(result.get("message", "Gagal menambahkan Bank"), "danger")
    return render_template("add-bank.html", action="create")

@bank_bp.route("/bank_admin", methods=["GET"])
def bank_admin():
    if not check_login() or not is_admin():
        return redirect('/')
    banks = bank_model.get_all()
    return render_template("banks_admin.html", banks=banks)

@bank_bp.route("/get-bank", methods=["GET"])
def get_banks():
    if not check_login():
        return redirect('/')
    try:
        banks = bank_model.get_all()
        for bank in banks:
            bank["_id"] = str(bank["_id"])
        return jsonify(banks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bank_bp.route("/edit-bank/<bank_id>", methods=["GET", "POST"])
def update_bank(bank_id):
    if not check_login() or not is_admin():
        return redirect('/')
    if request.method == "GET":
        bank = bank_model.find_one({"_id": (bank_id)})
        return render_template("edit-bank.html", action="update", bank=bank)

    if request.method == "POST":
        try:
            session_id = session.get('session_id')
            username = r.get(session_id).decode('utf-8')

            update_data = {
                "bankDesc": request.form.get("bankDesc"),
                "activeStatus": request.form.get("activeStatus")
            }
            result = bank_model.update(bank_id, update_data, username)
            if result.get("success"):
                flash("Bank berhasil ditambahkan!", "success")
            return redirect(url_for("bank.bank_admin"))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template("edit-bank.html", action="update", bank=bank)

@bank_bp.route("/delete-bank/<bank_id>", methods=["DELETE"])
def delete_bank(bank_id):
    if not check_login() or not is_admin():
        return redirect('/')
    try:
        result = bank_model.delete(bank_id)
        if result["success"]:
            return jsonify({"deleted_count": 1}), 200
        else:
            return jsonify({"deleted_count": 0, "message": result["message"]}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bank_bp.route('/bank')
def bank_user():
    if not check_login():
        return redirect('/')
    return render_template('banks.html')

@bank_bp.route('/bankdor')
def bank_vendor():
    if not check_login():
        return redirect('/')
    return render_template('banks2.html')