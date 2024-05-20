USE master
GO
-- Uncomment the ALTER DATABASE statement below to set the database to SINGLE_USER mode if the drop database command fails because the database is in use.
-- ALTER DATABASE DatabaseName SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
-- Drop the database if it exists
IF EXISTS (
  SELECT name
FROM sys.databases
WHERE name = N'DU_LICH_NINH_BINH'
)
DROP DATABASE DU_LICH_NINH_BINH
GO

-- Create a new database called 'DU_LICH_NINH_NINH'
-- Connect to the 'master' database to run this snippet
USE master
GO
-- Create the new database if it does not exist already
IF NOT EXISTS (
    SELECT name
FROM sys.databases
WHERE name = N'DU_LICH_NINH_BINH'
)
CREATE DATABASE DU_LICH_NINH_BINH
GO

USE DU_LICH_NINH_BINH
GO

-- Tạo bảng Place
CREATE TABLE Place (
  PlaceCode INT PRIMARY KEY,
  PlaceName VARCHAR(255),
  DESCRIPTION_ VARCHAR(255),
  TourismType VARCHAR(255),
  Place_Image VARCHAR(255)
);
-- Tạo bảng Transport
CREATE TABLE Transport (
  TransportCode INT PRIMARY KEY,
  TransportType VARCHAR(255),
  MaxPassengerCount INT
);

-- Tạo bảng Service
CREATE TABLE Service (
  ServiceCode INT PRIMARY KEY,
  ServiceName VARCHAR(255),
  ServiceType VARCHAR(255)
);
-- Tạo bảng Tag
CREATE TABLE Tag (
  TagCode INT PRIMARY KEY,
  TagName VARCHAR(255),
  DESCRIPTION_ VARCHAR(255),
  RelatedTourList TEXT,
);
-- Tạo bảng Tour
CREATE TABLE Tour (
  TourCode INT PRIMARY KEY,
  TourName VARCHAR(255),
  DESCRIPTION_ VARCHAR(255),
  DestinationCode INT,
  StopCode INT,
  Duration INT,
  TourPrice DECIMAL(10,2),
  VehicleCode INT,
  ServiceCode INT,
  TagCode INT,
  FOREIGN KEY (TagCode) REFERENCES Tag(TagCode),
  FOREIGN KEY (DestinationCode) REFERENCES Place(PlaceCode),
  FOREIGN KEY (StopCode) REFERENCES Place(PlaceCode),
  FOREIGN KEY (VehicleCode) REFERENCES Transport(TransportCode),
  FOREIGN KEY (ServiceCode) REFERENCES Service(ServiceCode)
);
-- Tạo bảng trung gian TourTag
CREATE TABLE TourTag (
  TourCode INT,
  TagCode INT,
  FOREIGN KEY (TourCode) REFERENCES Tour(TourCode),
  FOREIGN KEY (TagCode) REFERENCES Tag(TagCode)
);


-- Tạo bảng Customer
CREATE TABLE Customer (
  CustomerCode INT PRIMARY KEY,
  CustomerName VARCHAR(255),
  DateOfBirth DATE,
  Customer_Addrees VARCHAR(255),
  PhoneNumber VARCHAR(20),
  Email VARCHAR(255),
  IDCard VARCHAR(20)
);

-- Tạo bảng Hotel
CREATE TABLE Hotel (
  HotelCode INT PRIMARY KEY,
  HotelName VARCHAR(255),
  Customer_Hotel VARCHAR(255),
  PhoneNumber VARCHAR(20),
  DESCRIPTION_ VARCHAR(255),
  Rating DECIMAL(3,2),

);
-- Tạo bảng Booking
CREATE TABLE Booking (
  BookingCode INT PRIMARY KEY,
  CustomerCode INT,
  TourCode INT,
  PassengerCount INT,
  BookingDate DATE,
  PaymentStatus VARCHAR(255),
  HotelCode INT,
  FOREIGN KEY (HotelCode) REFERENCES Hotel(HotelCode),
  FOREIGN KEY (CustomerCode) REFERENCES Customer(CustomerCode),
  FOREIGN KEY (TourCode) REFERENCES Tour(TourCode)
);

-- Tạo bảng Invoice
CREATE TABLE Invoice (
  InvoiceCode INT PRIMARY KEY,
  CustomerCode INT,
  PaymentMethod VARCHAR(255),
  Price DECIMAL(10,2),
  Tax DECIMAL(10,2),
  Invoice_Date DATE,
  FOREIGN KEY (CustomerCode) REFERENCES Customer(CustomerCode)
);

-- Tạo bảng Employee
CREATE TABLE Employee (
  EmployeeID INT PRIMARY KEY,
  EmployeeName VARCHAR(255),
  Position VARCHAR(255),
  PhoneNumber VARCHAR(20),
  Email VARCHAR(255),
  EmPloyee_BookingCode INT,
  EmPloyee_InvoiceCode INT,
  FOREIGN KEY (EmPloyee_BookingCode) REFERENCES Booking(BookingCode),
  FOREIGN KEY (EmPloyee_InvoiceCode) REFERENCES Invoice(InvoiceCode)
);





-- Tạo bảng Searching
CREATE TABLE Searching (
  SearchCode INT PRIMARY KEY,
  CustomerCode INT,
  SearchKeyword VARCHAR(255),
  SearchDate DATE,
  FOREIGN KEY (CustomerCode) REFERENCES Customer(CustomerCode)
);

-- Tạo bảng Rating
CREATE TABLE Rating (
  RatingCode INT PRIMARY KEY,
  TourCode INT,
  CustomerCode INT,
  RatingScore DECIMAL(3,2),
  Comment VARCHAR(255),
  RatingDate DATE,
  FOREIGN KEY (TourCode) REFERENCES Tour(TourCode),
  FOREIGN KEY (CustomerCode) REFERENCES Customer(CustomerCode)
);



-- Tạo bảng Promotion
CREATE TABLE Promotion (
  PromotionCode INT PRIMARY KEY,
  TourCode INT,
  Discount DECIMAL(5,2),
  StartDate DATE,
  EndDate DATE,
  ApplicableConditions VARCHAR(255),
  FOREIGN KEY (TourCode) REFERENCES Tour(TourCode)
);
