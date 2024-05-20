CREATE DATABASE DULICH
GO
USE DULICH_TEST
-- TẠO BẢNG TourDuLich
CREATE TABLE TourDuLich (
    Matour INT PRIMARY KEY,
    Tentour NVARCHAR(255),
    Diemden NVARCHAR(255),
    Diemdung NVARCHAR(255),
    Thoigian DATE,
    Giatour DECIMAL(10, 2),
    Danhsachdiadiem TEXT,
    Makhachsan INT,
    FOREIGN KEY (Makhachsan) REFERENCES KhachSan(Makhachsan)
);
-- TẠO BẢNG  DiaDiemDuLich
CREATE TABLE DiaDiemDuLich (
    Madiadiem INT PRIMARY KEY,
    Tendiadiem NVARCHAR(255),
    Loaihinhdulich NVARCHAR(100)
);
-- TẠO BẢNG KhachHang
CREATE TABLE KhachHang (
    MaKH INT PRIMARY KEY,
    TenKH NVARCHAR(255),
    Ngaysinh DATE,
    Diachi NVARCHAR(255),
    SDT NVARCHAR(20),
    Email NVARCHAR(100),
    CCCD NVARCHAR(20)
);
-- TẠO BẢNG DatTour
CREATE TABLE DatTour (
    Madattour INT PRIMARY KEY,
    MaKH INT,
    Matour INT,
    Soluongkhach INT,
    Ngaydat DATE,
    Trangthai NVARCHAR(50),
    FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH),
    FOREIGN KEY (Matour) REFERENCES TourDuLich(Matour),
);
-- TẠO BẢNG HoaDon
CREATE TABLE HoaDon (
    Mahoadon INT PRIMARY KEY,
    MaKH INT,
    Giatien DECIMAL(10, 2),
    Thue DECIMAL(5, 2),
    Ngay DATE,
    FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH)
);
-- TẠO BẢNG LichSuTimKiem
CREATE TABLE LichSuTimKiem (
    Matimkiem INT PRIMARY KEY,
    Matour INT,
    MaKH INT,
    Tukhoa NVARCHAR(255),
    Ngaytimkiem DATE,
    FOREIGN KEY (Matour) REFERENCES TourDuLich(Matour),
    FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH)
);
-- TẠO BẢNG DanhGia
CREATE TABLE DanhGia (
    Madanhgia INT PRIMARY KEY,
    Matour INT,
    MaKH INT,
    Diemdanhgia DECIMAL(3, 1),
    Binhluan TEXT,
    Ngaydanhgia DATE,
    FOREIGN KEY (Matour) REFERENCES TourDuLich(Matour),
    FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH)
);
-- TẠO BẢNG Tag
CREATE TABLE Tag (
    Matag INT PRIMARY KEY,
    Tentag NVARCHAR(255),
    Mota TEXT,
    Danhsachtour TEXT
);
-- TẠO BẢNG UuDai
CREATE TABLE UuDai (
    Mauudai INT PRIMARY KEY,
    Matour INT,
    Giamgia DECIMAL(5, 2),
    Ngaybatdau DATE,
    Ngayketthuc DATE,
    Dieukienapdung NVARCHAR(255),
    FOREIGN KEY (Matour) REFERENCES TourDuLich(Matour)
);
-- TẠO BẢNG KhachSan
CREATE TABLE KhachSan (
    Makhachsan INT PRIMARY KEY,
    Tenkhachsan NVARCHAR(255),
    Diachikhachsan NVARCHAR(255),
    SDTkhachsan NVARCHAR(20)
);
-- TẠO BẢNG ChiTietTour_DiaDiem
CREATE TABLE ChiTietTour_DiaDiem (
    Matour INT,
    Madiadiem INT,
    Mota TEXT,
    Hinhanh NVARCHAR(255),
    Thoiluong INT,
    PRIMARY KEY (Matour, Madiadiem),
    FOREIGN KEY (Matour) REFERENCES TourDuLich(Matour),
    FOREIGN KEY (Madiadiem) REFERENCES DiaDiemDuLich(Madiadiem)
);
-- TẠO BẢNG DeXuat
CREATE TABLE DeXuat (
    Matour INT,
    Matag INT,
    Thinhhanh NVARCHAR(255),
    PRIMARY KEY (Matour, Matag),
    FOREIGN KEY (Matour) REFERENCES TourDuLich(Matour),
    FOREIGN KEY (Matag) REFERENCES Tag(Matag)
);
-- TẠO BẢNG ApDung
CREATE TABLE ApDung (
    Matour INT,
    Mauudai INT,
    PRIMARY KEY (Matour, Mauudai),
    FOREIGN KEY (Matour) REFERENCES TourDuLich(Matour),
    FOREIGN KEY (Mauudai) REFERENCES UuDai(Mauudai)
);











