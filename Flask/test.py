
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template, redirect, url_for, flash, session
import pyodbc
import random
# Thiết lập Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Thay thế bằng secret key của bạn

image_count = 6


# Connection string cho pyodbc
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=MSI\MSSQLSERVER01;"  # Thay thế bằng tên server của bạn
    "Database=thanhdoo;"  # Thay thế bằng tên database của bạn
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)
# Route cho chức năng đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                # Đảm bảo câu lệnh SQL phù hợp với cấu trúc cơ sở dữ liệu của bạn
                cursor.execute("SELECT * FROM KhachHang WHERE MaKH = ? AND Password = ?", (username, password))
                user = cursor.fetchone()
                if user:
                    session['logged_in'] = True
                    session['MaKH'] = user[0]  # Thay đổi chỉ số dựa vào cấu trúc bảng của bạn
                    return redirect(url_for('user'))
                else:
                    flash('Tên đăng nhập hoặc mật khẩu không chính xác!')
        except Exception as e:
            flash(f"Đã xảy ra lỗi: {e}")
    return render_template('BTL_KTPMUD/login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('MaKH', None)
    flash('Bạn đã đăng xuất thành công.')
    return redirect(url_for('login'))
# Route cho trang chủ
@app.route("/")
def index():
    return render_template("BTL_KTPMUD/index.html")
# Route cho chức năng đăng thanh toán



# Route cho chức năng đăng ký
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        connection_string = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=MSI\MSSQLSERVER01;"
            "Database=thanhdoo;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("""
        INSERT INTO KhachHang (MaKH, Email, Password) 
    VALUES (?, ?, ?)
""", (username, email, password))
                conn.commit()
                return render_template("BTL_KTPMUD/login.html")
                
        except pyodbc.Error as e:
            print(f"Đã xảy ra lỗi khi thêm người dùng mới: {e}")
            return f"Đã xảy ra lỗi: {e}"  # Hiển thị thông báo lỗi trên trang web
        
    return render_template("BTL_KTPMUD/signup.html")
@app.route('/')
def hello():
    if 'logged_in' in session:
        # Thay đổi thông điệp chào mừng dựa vào thông tin người dùng
        return f'Xin chào, {session["MaKH"]}!'
    else:
        return 'Xin chào! Vui lòng <a href="/login">đăng nhập</a> để tiếp tục.'
#route tìm kiếm
@app.route('/search_tour', methods=['GET', 'POST'])
def search_tour():
    if 'logged_in' in session:
        search_results = []
        if request.method == 'POST':
            search_query = request.form['search'].strip()  # Đảm bảo loại bỏ khoảng trắng
            if search_query:  # Kiểm tra xem chuỗi tìm kiếm có rỗng không
                try:
                    with pyodbc.connect(connection_string) as conn:
                        cursor = conn.cursor()
                        query = """
                        SELECT Matour, Tentour, Diemden, Diemdung, Thoigian, Giatour, Danhsachdiadiem, Makhachsan, Soluongnguoi
                        FROM TourDuLich
                        WHERE LOWER(Tentour) LIKE LOWER(?) OR LOWER(Diemden) LIKE LOWER(?) OR LOWER(Diemdung) LIKE LOWER(?)
                        """
                        search_pattern = f'%{search_query}%'
                        cursor.execute(query, search_pattern, search_pattern, search_pattern)
                        search_results = cursor.fetchall()
                        print(f"Search Results: {search_results}")  # Thêm dòng này để debug
                except Exception as e:
                    flash(f"Đã xảy ra lỗi khi tìm kiếm: {e}")
            else:
                flash("Vui lòng nhập từ khóa tìm kiếm.")
        return render_template('BTL_KTPMUD/search_tour.html', search_results=search_results,image_count=image_count)
    else:
        return redirect(url_for('login'))

@app.route('/bookings', methods=['GET', 'POST'])
@app.route('/bookings/<tour_id>', methods=['GET', 'POST'])
def bookings(tour_id=None):
    tourName = None
    matour = None
    if tour_id:
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Tentour FROM TourDuLich WHERE Matour = ?", tour_id)
                tour = cursor.fetchone()
                if tour:
                    tourName = tour[0]
                else:
                    flash('Không tìm thấy tour tương ứng. Vui lòng thử lại.')
                    return redirect(url_for('index'))
        except Exception as e:
            flash(f"Đã xảy ra lỗi khi truy vấn tên tour: {e}")
            return redirect(url_for('index'))
    if matour:
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Matour FROM TourDuLich WHERE Tentour = ?", tourName)
                tour_id = cursor.fetchone()
                if tour_id:
                    matour = tour_id[0]
                else:
                    flash('Không tìm thấy mã tour tương ứng. Vui lòng thử lại.')
                    return redirect(url_for('index'))
        except Exception as e:
            flash(f"Đã xảy ra lỗi khi truy vấn mã tour: {e}")
            return redirect(url_for('index'))

    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        cccd = request.form.get('cccd')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        customer_id = request.form.get('customer_id')
        try:
            # Establish a connection to SQL Server
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()

                # Check if the customer with the provided MaKH exists
                cursor.execute("SELECT COUNT(*) FROM KhachHang WHERE MaKH = ?", (customer_id,))
                customer_exists = cursor.fetchone()[0]

                if customer_exists > 0:
                    # Customer exists, update the TenKH with the provided name
                    cursor.execute("UPDATE KhachHang SET TenKH = ? WHERE MaKH = ?", (name, customer_id))
                    conn.commit()

                    # Generate a random value for Mahoadon
                    mahoadon = random.randint(0, 9999)

                    # Insert a new record into HoaDon table with the customer_id and generated Mahoadon
                    cursor.execute("INSERT INTO HoaDon (MaKH, Mahoadon) VALUES (?, ?)", (customer_id, mahoadon))
                    conn.commit()
                     # Generate a unique Madattour
                    madattour = random.randint(0, 999)
                     # Insert into HosoDatTour
                    cursor.execute(" INSERT INTO HosoDatTour (Madattour, MaKH, Matour)VALUES (?, ?,? )", (madattour, customer_id, matour))
                    conn.commit()

                    # Redirect or respond as needed (e.g., redirect to a success page)
                    return redirect(url_for('invoice'))
                else:
                    # Handle the case where the customer doesn't exist (optional)
                    return 'Customer does not exist. Booking failed.'

        except pyodbc.Error as e:
            return f'Error: {str(e)}'

        # The POST request handling logic goes here
        # ... (same as before)

    return render_template('BTL_KTPMUD/bookings.html', tour_name=tourName)

def get_invoice_data():
    # Thông tin kết nối SQL Server
    with pyodbc.connect(connection_string) as conn:

    # Truy vấn dữ liệu
        cursor = conn.cursor()
        cursor.execute("SELECT MaHoaDon, MaKH, Giatien, Thue, Ngay FROM HoaDon")
        result = cursor.fetchone()

    return result
@app.route('/invoice')
def invoice():
    data = get_invoice_data()
    if data:
        return render_template('BTL_KTPMUD/invoice.html', ma_hoa_don=data[0], ma_khach_hang=data[1], gia_tien=data[2], thue=data[3], ngay=data[4])
    else:
        return "Không có dữ liệu hóa đơn."

@app.route('/QRcode')
def qrcode():
    # Render trang QRcode.html khi người dùng nhấn vào nút "Thanh toán"
    return render_template('BTL_KTPMUD/QRcode.html')

def get_info_data():
    # Thông tin kết nối SQL Server
    with pyodbc.connect(connection_string) as conn:

    # Truy vấn dữ liệu
        cursor = conn.cursor()
        cursor.execute("SELECT MaKH, TenKH, Ngaysinh, Diachi, SDT, Email, CCCD FROM KhachHang")
        customer_info = cursor.fetchone()  # Lấy dữ liệu của người dùng

    return customer_info

@app.route('/info')
def info():
    info = get_info_data()
    if info:
        return render_template('BTL_KTPMUD/info.html', ma_khach_hang=info[0], ten_khach_hang=info[1],
                                ngay_sinh=info[2], dia_chi=info[3], SDT=info[4], Email = info[5], CCCD = info[6])

@app.route('/user')
def user():
    if 'logged_in' in session:
        # Thay đổi thông điệp chào mừng dựa vào thông tin người dùng
        return render_template("BTL_KTPMUD/user.html")

if __name__ == '__main__':
    app.run(debug=True)
