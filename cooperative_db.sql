-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 22, 2024 at 08:26 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cooperative_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `booking_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `booking_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `booking_status` varchar(255) NOT NULL,
  `note` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`booking_id`, `user_id`, `booking_time`, `booking_status`, `note`) VALUES
(79, 1, '2024-09-22 18:26:09', 'กำลังยืม', 'รายละเอียดการจอง'),
(82, 1, '2024-09-21 12:32:19', 'จอง', 'รายละเอียดการจอง'),
(83, 1, '2024-09-21 12:32:49', 'จอง', 'รายละเอียดการจอง'),
(84, 1, '2024-09-22 14:34:25', 'คืนครบ', 'รายละเอียดการจอง');

-- --------------------------------------------------------

--
-- Table structure for table `booking_detail`
--

CREATE TABLE `booking_detail` (
  `booking_detail_id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `place_equipment_id` int(11) NOT NULL,
  `booking_quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking_detail`
--

INSERT INTO `booking_detail` (`booking_detail_id`, `booking_id`, `place_equipment_id`, `booking_quantity`) VALUES
(47, 79, 1, 100),
(48, 79, 2, 200),
(49, 82, 2, 1),
(50, 83, 2, 1),
(51, 83, 1, 5),
(52, 83, 1, 1),
(53, 84, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `equipment`
--

CREATE TABLE `equipment` (
  `equipment_id` int(11) NOT NULL,
  `equipment_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `equipment`
--

INSERT INTO `equipment` (`equipment_id`, `equipment_name`) VALUES
(1, 'บอล'),
(2, 'บาส'),
(3, 'ไม้ปิงปอง'),
(4, 'ลูกปิงปอง'),
(5, 'ไม้เทนนิส'),
(6, 'ลูกเทนนิส'),
(7, 'ตะกร้อ'),
(8, 'ลูกวอลเลย์');

-- --------------------------------------------------------

--
-- Table structure for table `place`
--

CREATE TABLE `place` (
  `place_id` int(11) NOT NULL,
  `place_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `place`
--

INSERT INTO `place` (`place_id`, `place_name`) VALUES
(1, 'สนามกีฬา1'),
(2, 'สนามกีฬา2'),
(3, 'สนามกีฬา3'),
(4, 'สนามกีฬา4');

-- --------------------------------------------------------

--
-- Table structure for table `place_equipment`
--

CREATE TABLE `place_equipment` (
  `place_equipment_id` int(11) NOT NULL,
  `place_id` int(11) NOT NULL,
  `equipment_id` int(11) NOT NULL,
  `stock` int(11) NOT NULL,
  `available_stock` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `place_equipment`
--

INSERT INTO `place_equipment` (`place_equipment_id`, `place_id`, `equipment_id`, `stock`, `available_stock`) VALUES
(1, 1, 1, 10, 30),
(2, 1, 2, 15, 55),
(3, 1, 7, 10, 10),
(4, 1, 8, 15, 15),
(5, 4, 4, 20, 20),
(6, 4, 8, 99, 99),
(7, 4, 8, 99, 99),
(8, 4, 8, 7, 7),
(9, 4, 8, 22, 22),
(10, 4, 8, 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `returning`
--

CREATE TABLE `returning` (
  `returning_id` int(11) NOT NULL,
  `booking_detail_id` int(11) NOT NULL,
  `returning_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `returning_quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `returning`
--

INSERT INTO `returning` (`returning_id`, `booking_detail_id`, `returning_time`, `returning_quantity`) VALUES
(1, 47, '2024-09-21 17:30:32', 1),
(2, 48, '2024-09-21 17:30:32', 5),
(3, 50, '2024-09-22 03:36:15', 1),
(4, 51, '2024-09-22 03:36:15', 5),
(5, 52, '2024-09-22 03:36:15', 1),
(6, 50, '2024-09-22 03:36:17', 1),
(7, 51, '2024-09-22 03:36:17', 5),
(8, 52, '2024-09-22 03:36:17', 1),
(9, 53, '2024-09-22 08:50:46', 1),
(10, 50, '2024-09-22 08:55:15', 1),
(11, 51, '2024-09-22 08:55:15', 5),
(12, 52, '2024-09-22 08:55:15', 1),
(13, 53, '2024-09-22 13:11:12', 1),
(14, 53, '2024-09-22 13:12:39', 1),
(15, 53, '2024-09-22 13:19:23', 1),
(16, 53, '2024-09-22 13:22:15', 1),
(17, 53, '2024-09-22 13:22:23', 1),
(18, 53, '2024-09-22 13:23:48', 1),
(19, 53, '2024-09-22 13:24:00', 1),
(20, 53, '2024-09-22 13:33:10', 1),
(21, 53, '2024-09-22 13:33:16', 1),
(22, 53, '2024-09-22 13:33:18', 1),
(23, 53, '2024-09-22 13:33:19', 1),
(24, 53, '2024-09-22 13:33:19', 1),
(25, 53, '2024-09-22 13:33:20', 1),
(26, 53, '2024-09-22 13:33:20', 1),
(27, 53, '2024-09-22 13:33:21', 1),
(28, 53, '2024-09-22 13:34:21', 1),
(29, 53, '2024-09-22 13:34:23', 1),
(30, 53, '2024-09-22 13:34:24', 1),
(31, 53, '2024-09-22 13:37:30', 1),
(32, 53, '2024-09-22 13:46:17', 1),
(33, 53, '2024-09-22 13:49:26', 1),
(34, 53, '2024-09-22 13:49:32', 1),
(35, 53, '2024-09-22 13:49:36', 1),
(36, 53, '2024-09-22 14:14:13', 1),
(37, 53, '2024-09-22 14:33:35', 1),
(38, 53, '2024-09-22 14:34:25', 1),
(39, 47, '2024-09-22 17:55:13', 5),
(40, 48, '2024-09-22 17:55:13', 10),
(41, 47, '2024-09-22 17:55:57', 5),
(42, 48, '2024-09-22 17:55:57', 10),
(43, 47, '2024-09-22 17:56:39', 5),
(44, 48, '2024-09-22 17:56:39', 10),
(45, 47, '2024-09-22 17:56:57', 5),
(46, 48, '2024-09-22 17:56:57', 10);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `password` text NOT NULL,
  `sername` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `tell` varchar(10) NOT NULL,
  `role` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `user_name`, `password`, `sername`, `lastname`, `tell`, `role`) VALUES
(1, 'bigshow', '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5', 'big', 'show', '0954567894', 'user'),
(2, 'thar', '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5', 'th', 'ar', '0856472364', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `booking_detail`
--
ALTER TABLE `booking_detail`
  ADD PRIMARY KEY (`booking_detail_id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `place_equipment_id` (`place_equipment_id`);

--
-- Indexes for table `equipment`
--
ALTER TABLE `equipment`
  ADD PRIMARY KEY (`equipment_id`);

--
-- Indexes for table `place`
--
ALTER TABLE `place`
  ADD PRIMARY KEY (`place_id`);

--
-- Indexes for table `place_equipment`
--
ALTER TABLE `place_equipment`
  ADD PRIMARY KEY (`place_equipment_id`),
  ADD KEY `place_id` (`place_id`),
  ADD KEY `equipment_id` (`equipment_id`);

--
-- Indexes for table `returning`
--
ALTER TABLE `returning`
  ADD PRIMARY KEY (`returning_id`),
  ADD KEY `booking_id` (`booking_detail_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `booking_detail`
--
ALTER TABLE `booking_detail`
  MODIFY `booking_detail_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `equipment`
--
ALTER TABLE `equipment`
  MODIFY `equipment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `place`
--
ALTER TABLE `place`
  MODIFY `place_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `place_equipment`
--
ALTER TABLE `place_equipment`
  MODIFY `place_equipment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `returning`
--
ALTER TABLE `returning`
  MODIFY `returning_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `booking_detail`
--
ALTER TABLE `booking_detail`
  ADD CONSTRAINT `booking_detail_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `booking` (`booking_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `booking_detail_ibfk_2` FOREIGN KEY (`place_equipment_id`) REFERENCES `place_equipment` (`place_equipment_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `place_equipment`
--
ALTER TABLE `place_equipment`
  ADD CONSTRAINT `place_equipment_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `place` (`place_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `place_equipment_ibfk_2` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `returning`
--
ALTER TABLE `returning`
  ADD CONSTRAINT `returning_ibfk_1` FOREIGN KEY (`booking_detail_id`) REFERENCES `booking_detail` (`booking_detail_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
