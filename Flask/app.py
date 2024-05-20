from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Thay thế với thông tin kết nối của bạn
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@LAPTOP-7M70QQFR\SQLEXPRESS/DULICH_TEST?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
import pyodbc
app.config['SQLALCHEMY_DATABASE_URI'] = (
    r'mssql+pyodbc://@LAPTOP-7M70QQFR\SQLEXPRESS/DULICH_TEST?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Định nghĩa model KhachHang phản ánh bảng trong cơ sở dữ liệu
class KhachHang(db.Model):
    _tablename_ = 'KhachHang'
    MaKH = db.Column(db.Integer, primary_key=True)
    TenKH = db.Column(db.String(255), nullable=False)
    Ngaysinh = db.Column(db.Date, nullable=True)
    Diachi = db.Column(db.String(255), nullable=True)
    SDT = db.Column(db.String(20), nullable=True)
    Email = db.Column(db.String(100), nullable=False)
    CCCD = db.Column(db.String(20), nullable=True)
    passcode = db.Column(db.String(20), nullable=False)

# Route cho trang chủ
@app.route("/")
def index():
    return render_template("BTL_KTPMUD/index.html")

# Route cho chức năng đăng nhập
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = KhachHang.query.filter_by(Email=email).first()
        if user and check_password_hash(user.passcode, password):
            # Đăng nhập thành công, chuyển hướng đến trang chủ
            return redirect(url_for("index"))
        else:
            # Đăng nhập không thành công, hiển thị thông báo lỗi
            pass
    return render_template("BTL_KTPMUD/login.html")


# Khởi tạo cơ sở dữ liệu và tạo bảng
# @app.before_first_request()
def create_tables():
    db.create_all()

# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True)