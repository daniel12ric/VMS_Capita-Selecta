from flask import Blueprint, jsonify, request, render_template,session, redirect, url_for, flash
from controller.vendor_control import VendorModel, akunColl
from controller.order_control import OrderModel
from config import r

vendor_bp = Blueprint("vendor", __name__)
vendor_model = VendorModel()
order_model = OrderModel()

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

def is_vendor():
    session_id = session.get('session_id')
    if session_id:
        current_username = r.get(session_id).decode('utf-8')
        user_data = akunColl.find_one({'username': current_username})
        return user_data and user_data['roleid'] == 'vendor'
    return False


@vendor_bp.route("/add-vendor", methods=["GET", "POST"])
def vendor_create():
    if not check_login() or not is_admin():
        return redirect('/')
    session_id = session.get('session_id')
    username = r.get(session_id).decode('utf-8')
    if request.method == "POST":
        result = vendor_model.create(username)
        if result.get("success"):
            flash("Vendor berhasil ditambahkan!", "success")
            return redirect(url_for("vendor_bp.vendor_admin"))
        else:
            flash(result.get("message", "Gagal menambahkan Vendor"), "danger")
    return render_template("add-vendor.html", action="create")

@vendor_bp.route("/vendor_admin", methods=["GET"])
def vendor_admin():
    if not check_login() or not is_admin():
        return redirect('/')
    vendor = vendor_model.get_all()
    return render_template("vendor_admin.html", vendor=vendor)

@vendor_bp.route("/get-vendor", methods=["GET"])
def get_vendor():
    if not check_login():
        return redirect('/')
    try:
        vendors = vendor_model.get_all()
        for vendor in vendors:
            vendor["_id"] = str(vendor["_id"])
        return jsonify(vendors), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vendor_bp.route("/edit-vendor/<vendor_id>", methods=["GET", "POST"])
def update_vendor(vendor_id):
    if not check_login() or not is_admin():
        return redirect('/')

    if request.method == "GET":
        vendor = vendor_model.find_one(vendor_id)
        if not vendor:
            flash("Vendor not found", "danger")
            return render_template("edit-vendor.html", action="update", vendor=vendor)
    
        bank_list = vendor_model.get_bank()
        
        return render_template("edit-vendor.html", vendor=vendor, bank_list=bank_list)

    if request.method == "POST":
        try:
            session_id = session.get('session_id')
            username = r.get(session_id).decode('utf-8')

            supporting_equipment = []
            i = 0
            while request.form.get(f"supportingEquipment[{i}][toolType]"):
                equipment = {
                    "toolType": request.form.get(f"supportingEquipment[{i}][toolType]"),
                    "count": request.form.get(f"supportingEquipment[{i}][count]"),
                    "merk": request.form.get(f"supportingEquipment[{i}][merk]"),
                    "condition": request.form.get(f"supportingEquipment[{i}][condition]"),
                }
                supporting_equipment.append(equipment)
                i += 1

            pic = []
            i = 0
            while request.form.get(f"pic[{i}][username]"):
                infoPic = {
                    "username": request.form.get(f"pic[{i}][username]"),
                    "name": request.form.get(f"pic[{i}][name]"),
                    "email": request.form.get(f"pic[{i}][email]"),
                    "noTelp": request.form.get(f"pic[{i}][noTelp]"),
                }
                pic.append(infoPic)
                i += 1

            account_bank = []
            i = 0
            while request.form.get(f"accountBank[{i}][bankCode]"):
                infoBank = {
                    "bankCode": request.form.get(f"accountBank[{i}][bankCode]"),
                    "bankName": request.form.get(f"accountBank[{i}][bankName]"),
                    "accountNumber": request.form.get(f"accountBank[{i}][accountNumber]"),
                    "accountName": request.form.get(f"accountBank[{i}][accountName]"),
                }
                account_bank.append(infoBank)
                i += 1

            update_data = {
                "partnerType": request.form.get('partnerType'),
                "vendorName": request.form.get('vendorName'),
                "unitUsaha": request.form.get('unitUsaha'),
                "address": request.form.get('address'),
                "country": request.form.get('country'),
                "province": request.form.get('province'),
                "noTelp": request.form.get('noTelp'),
                "emailCompany": request.form.get('emailCompany'),
                "website": request.form.get('website'),
                "noNPWP": request.form.get('noNPWP'),
                "activeStatus": request.form.get('activeStatus'),
                "supportingEquipment": supporting_equipment,
                "pic": pic,
                "accountBank": account_bank
            }

            result = vendor_model.update(vendor_id, update_data, username)
            vendor = vendor_model.find_one(vendor_id)
            if result.get("success"):
                flash("Vendor berhasil diperbarui!", "success")
            else:
                flash(result.get("message", "Gagal memperbarui vendor"), "danger")

            return redirect(url_for("vendor_bp.vendor_admin"))

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return render_template("edit-vendor.html", action="update", vendor=vendor)


@vendor_bp.route("/delete-vendor/<vendor_id>", methods=["DELETE"])
def delete_vendor(vendor_id):
    if not check_login() or not is_admin():
        return redirect('/')
    try:
        result = vendor_model.delete(vendor_id)
        if result["success"]:
            return jsonify({"deleted_count": 1}), 200
        else:
            return jsonify({"deleted_count": 0, "message": result["message"]}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@vendor_bp.route('/vendor')
def vendor_user():
    if not check_login():
        return redirect('/')
    vendor = vendor_model.get_all()
    return render_template('vendor.html',vendor=vendor)

@vendor_bp.route('/vendordor')
def vendor_vendor():
    if not check_login():
        return redirect('/')
    vendor = vendor_model.get_all()
    return render_template('vendor2.html',vendor=vendor)

@vendor_bp.route('/pesanan')
def vendor_pesan():
    if not check_login()or not is_vendor():
        return redirect('/')
    order = order_model.get_all()
    return render_template('pesan_vendor.html', order=order)

#
@vendor_bp.route('/pesanan_admin')
def admin_pesan():
    if not check_login()or not is_admin():
        return redirect('/')
    order = order_model.get_all()
    return render_template('pesan_admin.html', order=order)

#
@vendor_bp.route("/get-bank-list", methods=["GET"])
def get_bank():
    if not check_login() or not is_admin():
        return redirect('/')
    try:
        bank_list = vendor_model.get_bank()
        return jsonify(bank_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@vendor_bp.route("/get-order", methods=["GET"])
def get_order():
    if not check_login() or not is_vendor():
        return redirect('/')
    try:
        order_list = order_model.get_all()
        return jsonify(order_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@vendor_bp.route("/get-orderr", methods=["GET"])
def get_orderr():
    if not check_login() or not is_admin():
        return redirect('/')
    try:
        order_list = order_model.get_all()
        return jsonify(order_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@vendor_bp.route("/add-order", methods=["GET", "POST"])
def order_create():
    if not check_login() or not is_vendor():
        return redirect('/')
    session_id = session.get('session_id')
    username = r.get(session_id).decode('utf-8')
    if request.method == "POST":
        resultt = order_model.create(username)
        if resultt.get("success"):
            flash("Order berhasil ditambahkan!", "success")
            return redirect(url_for("vendor_bp.vendor_pesan"))
        else:
            flash(resultt.get("message", "Gagal menambahkan Order"), "danger")
    return render_template("add-order.html", action="create")

@vendor_bp.route('/vendors')
def vendors():
    if not check_login():
        return redirect('/login')
    users = list(akunColl.find())
    session_id = session.get('session_id')
    current_user = r.get(session_id).decode('utf-8')
    return render_template('index3.html',  users=users, username=current_user.upper())