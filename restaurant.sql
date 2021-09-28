-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 28, 2021 at 02:17 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 8.0.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurant`
--

-- --------------------------------------------------------

--
-- Table structure for table `foods`
--

CREATE TABLE `foods` (
  `fid` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `ftype` varchar(20) NOT NULL,
  `fprice` float(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `foods`
--

INSERT INTO `foods` (`fid`, `fname`, `ftype`, `fprice`) VALUES
(1, 'Idli', 'veg', 30.00),
(2, 'Masala Dosa', 'veg', 50.00),
(3, 'Chicken Biriyani', 'nonveg', 250.00),
(4, 'Ice-Cream', 'veg', 25.00),
(5, 'Velvet Cake', 'nonveg', 400.00),
(6, 'Pizza', 'veg', 99.00),
(7, 'Burger', 'veg', 75.00),
(8, 'Fish Curry', 'nonveg', 190.00),
(9, 'Upma', 'veg', 49.00),
(10, 'Purota', 'nonveg', 96.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `mobile` bigint(15) NOT NULL,
  `password` varchar(100) NOT NULL,
  `orders` longtext NOT NULL,
  `balance` float(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `mobile`, `password`, `orders`, `balance`) VALUES
(0, 'Thinesh', 7784517654, 'thinesh', '', 0.00),
(1, 'admin', 1234567890, 'admin', 'None', 0.00);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
