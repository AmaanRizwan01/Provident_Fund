-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 20, 2025 at 03:13 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `provident_fund`
--

-- --------------------------------------------------------

--
-- Table structure for table `employeepersonalfile`
--

CREATE TABLE `employeepersonalfile` (
  `EmployeeID` int(11) NOT NULL,
  `EmpName` varchar(100) DEFAULT NULL,
  `Designation` varchar(50) DEFAULT NULL,
  `Department` varchar(50) DEFAULT NULL,
  `Grade` varchar(20) DEFAULT NULL,
  `CNIC` varchar(15) DEFAULT NULL,
  `DateOfAppointment` date DEFAULT NULL,
  `LengthOfServiceMonths` int(11) DEFAULT NULL,
  `CalculateProfit` char(1) DEFAULT NULL CHECK (`CalculateProfit` in ('Y','N'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employeepersonalfile`
--

INSERT INTO `employeepersonalfile` (`EmployeeID`, `EmpName`, `Designation`, `Department`, `Grade`, `CNIC`, `DateOfAppointment`, `LengthOfServiceMonths`, `CalculateProfit`) VALUES
(101, 'Ali Khan', 'Manager', 'HR', 'A1', '42101-1234567-1', '2015-06-15', 108, 'Y'),
(102, 'Sara Ahmed', 'Assistant Manager', 'Finance', 'B2', '42201-9876543-2', '2018-04-20', 72, 'N'),
(103, 'Usman Raza', 'Software Engineer', 'IT', 'C3', '42301-1112233-4', '2020-01-10', 48, 'Y');

-- --------------------------------------------------------

--
-- Table structure for table `employeeprovidentfile`
--

CREATE TABLE `employeeprovidentfile` (
  `TransactionID` int(11) NOT NULL,
  `EmployeeID` int(11) DEFAULT NULL,
  `LoanID` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `EmployeeContribution` decimal(15,2) DEFAULT NULL,
  `UniversityContribution` decimal(15,2) DEFAULT NULL,
  `AvailableFunds` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employeeprovidentfile`
--

INSERT INTO `employeeprovidentfile` (`TransactionID`, `EmployeeID`, `LoanID`, `Date`, `EmployeeContribution`, `UniversityContribution`, `AvailableFunds`) VALUES
(1, 101, NULL, '2024-01-01', 5000.00, 5000.00, 10000.00),
(2, 101, NULL, '2024-01-15', 6000.00, 6000.00, 22000.00),
(3, 101, 1, '2024-02-01', 0.00, 0.00, 2000.00),
(4, 102, 2, '2024-02-10', 0.00, 0.00, -7000.00),
(5, 103, NULL, '2024-01-10', 7000.00, 7000.00, 14000.00);

-- --------------------------------------------------------

--
-- Table structure for table `loan`
--

CREATE TABLE `loan` (
  `LoanID` int(11) NOT NULL,
  `EmployeeID` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `LoanAmount` decimal(15,2) DEFAULT NULL,
  `LoanRecoveryAmount` decimal(15,2) DEFAULT NULL,
  `Interest` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `loan`
--

INSERT INTO `loan` (`LoanID`, `EmployeeID`, `Date`, `LoanAmount`, `LoanRecoveryAmount`, `Interest`) VALUES
(1, 101, '2024-02-01', 20000.00, 5000.00, 2.50),
(2, 102, '2024-02-10', 15000.00, 3000.00, 3.00),
(3, 103, '2024-02-15', 25000.00, 4000.00, 2.80);

-- --------------------------------------------------------

--
-- Table structure for table `profit`
--

CREATE TABLE `profit` (
  `TransactionID` int(11) NOT NULL,
  `EmployeeID` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `ProfitAmount` decimal(15,2) DEFAULT NULL,
  `ProfitPercentage` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `profit`
--

INSERT INTO `profit` (`TransactionID`, `EmployeeID`, `Date`, `ProfitAmount`, `ProfitPercentage`) VALUES
(1, 101, '2024-03-01', 5000.00, 5.00),
(2, 102, '2024-03-05', 4000.00, 4.50),
(3, 103, '2024-03-10', 6000.00, 5.20);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `employeepersonalfile`
--
ALTER TABLE `employeepersonalfile`
  ADD PRIMARY KEY (`EmployeeID`),
  ADD UNIQUE KEY `CNIC` (`CNIC`);

--
-- Indexes for table `employeeprovidentfile`
--
ALTER TABLE `employeeprovidentfile`
  ADD PRIMARY KEY (`TransactionID`),
  ADD KEY `EmployeeID` (`EmployeeID`),
  ADD KEY `LoanID` (`LoanID`);

--
-- Indexes for table `loan`
--
ALTER TABLE `loan`
  ADD PRIMARY KEY (`LoanID`),
  ADD KEY `EmployeeID` (`EmployeeID`);

--
-- Indexes for table `profit`
--
ALTER TABLE `profit`
  ADD PRIMARY KEY (`TransactionID`),
  ADD KEY `EmployeeID` (`EmployeeID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `employeepersonalfile`
--
ALTER TABLE `employeepersonalfile`
  MODIFY `EmployeeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=104;

--
-- AUTO_INCREMENT for table `employeeprovidentfile`
--
ALTER TABLE `employeeprovidentfile`
  MODIFY `TransactionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `loan`
--
ALTER TABLE `loan`
  MODIFY `LoanID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `profit`
--
ALTER TABLE `profit`
  MODIFY `TransactionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `employeeprovidentfile`
--
ALTER TABLE `employeeprovidentfile`
  ADD CONSTRAINT `employeeprovidentfile_ibfk_1` FOREIGN KEY (`EmployeeID`) REFERENCES `employeepersonalfile` (`EmployeeID`) ON DELETE CASCADE,
  ADD CONSTRAINT `employeeprovidentfile_ibfk_2` FOREIGN KEY (`LoanID`) REFERENCES `loan` (`LoanID`) ON DELETE SET NULL;

--
-- Constraints for table `loan`
--
ALTER TABLE `loan`
  ADD CONSTRAINT `loan_ibfk_1` FOREIGN KEY (`EmployeeID`) REFERENCES `employeepersonalfile` (`EmployeeID`) ON DELETE CASCADE;

--
-- Constraints for table `profit`
--
ALTER TABLE `profit`
  ADD CONSTRAINT `profit_ibfk_1` FOREIGN KEY (`EmployeeID`) REFERENCES `employeepersonalfile` (`EmployeeID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
