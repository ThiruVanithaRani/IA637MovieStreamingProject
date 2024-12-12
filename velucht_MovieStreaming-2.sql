-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Dec 12, 2024 at 12:58 AM
-- Server version: 8.0.34
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `velucht_MovieStreaming`
--

-- --------------------------------------------------------

--
-- Table structure for table `Movies`
--

CREATE TABLE `Movies` (
  `MovieID` int NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Description` text,
  `Genre` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Movies`
--

INSERT INTO `Movies` (`MovieID`, `Title`, `Description`, `Genre`) VALUES
(1, 'GanapathyBackiam', 'how grandparents Thatha Ganapathy and paati Backiam take care of their grandchildren Vanitha', 'Family'),
(2, 'Ghilli', 'Vijay saving dhanalaxmi from Muthupandi', 'Action'),
(3, 'Kandhan karunai', 'Lord Murugan\'s care and settai', 'Devotional'),
(6, 'GuruWedsThiru', 'Guru and Thiru\'s life journey from Kottaimedu to Dubai to America', 'Family Entertainment'),
(8, 'Kungfu panda2', 'Dragon Warrior Po saving people from Villians with his friends', 'Animation'),
(9, 'Hotel Transylvania', 'A father vampire taking care of his daughter who married a human boy', 'Animation'),
(11, 'Soorarai Potru', 'Maaran started an airline and wants non-rich people also fly', 'Motivation'),
(15, 'Transformers', 'Aliens protecting humans as robotic cars', 'animation'),
(18, 'Amaran', 'An Army Man and his Family\'s Story', 'Emotional Motivational'),
(19, 'Avengers', 'Superheroes saving the world from villains', 'Fantasy');

-- --------------------------------------------------------

--
-- Table structure for table `MovieStreamingPlatforms`
--

CREATE TABLE `MovieStreamingPlatforms` (
  `ID` int NOT NULL,
  `MovieID` int NOT NULL,
  `PlatformID` int NOT NULL,
  `StartDate` date NOT NULL,
  `EndDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `MovieStreamingPlatforms`
--

INSERT INTO `MovieStreamingPlatforms` (`ID`, `MovieID`, `PlatformID`, `StartDate`, `EndDate`) VALUES
(1, 1, 4, '2024-10-25', '2025-01-30'),
(2, 2, 4, '2024-12-14', '2025-05-16'),
(3, 3, 1, '2025-04-19', '2025-08-15'),
(4, 6, 3, '2024-12-14', '2025-04-18'),
(5, 8, 3, '2024-12-29', '2025-11-22'),
(6, 9, 1, '2024-12-22', '2025-08-29'),
(7, 11, 4, '2025-07-25', '2026-01-29'),
(8, 15, 2, '2025-08-22', '2026-04-16'),
(10, 18, 4, '2024-12-07', '2025-09-20'),
(11, 19, 4, '2024-12-14', '2025-07-19'),
(12, 15, 3, '2024-12-08', '2024-12-21');

-- --------------------------------------------------------

--
-- Table structure for table `StreamingPlatforms`
--

CREATE TABLE `StreamingPlatforms` (
  `PlatformID` int NOT NULL,
  `PlatformName` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `StreamingPlatforms`
--

INSERT INTO `StreamingPlatforms` (`PlatformID`, `PlatformName`) VALUES
(1, 'Netflix'),
(2, 'Hulu'),
(3, 'Disney+'),
(4, 'Amazon Prime');

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `UserID` int NOT NULL,
  `UserName` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `UserType` enum('admin','user') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`UserID`, `UserName`, `Password`, `UserType`) VALUES
(1, 'admin', 'abda260dc78e2fdef997cccce1be6a0c', 'admin'),
(2, 'user1', '0d7740c8e2cf9e3c6320f4d702cc8354', 'user'),
(3, 'user2', '34e497556df68dd71d832219d3de4771', 'user'),
(4, 'user3', '780725bfff0d39b1cc9d9b81dfe07641', 'user'),
(5, 'user4', 'cbc0d20bec760816981886cd686db4fd', 'user'),
(6, 'user5', '3bb3a0bf6bd3c902eb07f07a14f348ee', 'user'),
(7, 'user6', '9ee46766111a5a36a9386642e668aece', 'user'),
(10, 'user7', '989cb2b9cb7c1c368c5a5743b52649f0', 'user'),
(11, 'user8', 'userpass8', 'user'),
(12, 'user9', 'userpass9', 'user'),
(13, 'user10', 'userpass10', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `WatchedMovies`
--

CREATE TABLE `WatchedMovies` (
  `ID` int NOT NULL,
  `UserID` int NOT NULL,
  `MovieID` int NOT NULL,
  `Rating` int DEFAULT NULL,
  `Comment` text,
  `Timestamp` datetime DEFAULT CURRENT_TIMESTAMP
) ;

--
-- Dumping data for table `WatchedMovies`
--

INSERT INTO `WatchedMovies` (`ID`, `UserID`, `MovieID`, `Rating`, `Comment`, `Timestamp`) VALUES
(1, 2, 1, 5, 'Feel Good Movie', '2024-12-11 09:18:53'),
(2, 2, 8, 4, 'Funny movie to watch with kids', '2024-12-11 09:18:53'),
(3, 2, 6, 5, 'It is a feel good movie with a lot of fun and mixed emotions', '2024-12-11 09:18:53'),
(5, 2, 11, 5, 'Such an Inspirational movie', '2024-12-11 09:18:53'),
(6, 4, 3, 5, 'i love murugan', '2024-12-11 09:18:53'),
(7, 4, 1, 3, 'Good movie', '2024-12-11 09:18:53'),
(8, 2, 2, 5, 'Fun Filled movie', '2024-12-11 09:18:53'),
(9, 2, 9, 2, 'good', '2024-12-11 09:18:53'),
(10, 3, 9, 3, 'good', '2024-12-11 09:18:53'),
(11, 3, 15, 3, 'good', '2024-12-11 09:18:53'),
(12, 4, 11, 3, '', '2024-12-11 09:18:53'),
(13, 4, 3, 1, '', '2024-12-11 09:18:53'),
(14, 4, 6, 3, '', '2024-12-11 09:18:53'),
(15, 4, 6, 5, '', '2024-12-11 09:18:53'),
(16, 4, 1, 5, '', '2024-12-11 09:18:53'),
(18, 2, 2, 3, 'average movie', '2024-12-11 09:18:53'),
(20, 5, 1, 5, 'good movie', '2024-12-11 09:45:02'),
(21, 2, 18, 1, 'okay', '2024-12-11 12:00:45'),
(22, 2, 19, 4, 'good', '2024-12-11 12:01:00'),
(23, 2, 18, 5, 'good', '2024-12-11 12:01:09'),
(24, 4, 8, 1, 'boring', '2024-12-11 12:35:03'),
(25, 7, 9, 3, 'good one', '2024-12-11 12:53:47'),
(26, 4, 2, 4, 'good', '2024-12-11 13:25:32'),
(27, 4, 2, 3, 'okay', '2024-12-11 13:34:31'),
(28, 10, 19, 2, 'not interesting', '2024-12-11 13:35:38'),
(29, 10, 1, 5, 'good', '2024-12-11 13:59:48'),
(30, 10, 1, 5, 'good', '2024-12-11 14:01:03'),
(31, 2, 11, 4, 'bbfnfhm', '2024-12-11 20:36:47'),
(32, 3, 18, 5, 'Too good', '2024-12-12 00:02:01'),
(33, 3, 19, 3, 'Average Movie', '2024-12-12 00:03:34'),
(34, 10, 1, 5, 'good', '2024-12-12 00:36:32'),
(35, 4, 2, 3, 'good', '2024-12-12 00:51:33'),
(36, 2, 3, 3, 'good', '2024-12-12 00:54:58');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Movies`
--
ALTER TABLE `Movies`
  ADD PRIMARY KEY (`MovieID`);

--
-- Indexes for table `MovieStreamingPlatforms`
--
ALTER TABLE `MovieStreamingPlatforms`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `PlatformID` (`PlatformID`),
  ADD KEY `MovieStreamingPlatforms_ibfk_1` (`MovieID`);

--
-- Indexes for table `StreamingPlatforms`
--
ALTER TABLE `StreamingPlatforms`
  ADD PRIMARY KEY (`PlatformID`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`UserID`);

--
-- Indexes for table `WatchedMovies`
--
ALTER TABLE `WatchedMovies`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `UserID` (`UserID`),
  ADD KEY `WatchedMovies_ibfk_2` (`MovieID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Movies`
--
ALTER TABLE `Movies`
  MODIFY `MovieID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `MovieStreamingPlatforms`
--
ALTER TABLE `MovieStreamingPlatforms`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `StreamingPlatforms`
--
ALTER TABLE `StreamingPlatforms`
  MODIFY `PlatformID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `UserID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `WatchedMovies`
--
ALTER TABLE `WatchedMovies`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `MovieStreamingPlatforms`
--
ALTER TABLE `MovieStreamingPlatforms`
  ADD CONSTRAINT `MovieStreamingPlatforms_ibfk_1` FOREIGN KEY (`MovieID`) REFERENCES `Movies` (`MovieID`),
  ADD CONSTRAINT `MovieStreamingPlatforms_ibfk_2` FOREIGN KEY (`PlatformID`) REFERENCES `StreamingPlatforms` (`PlatformID`);

--
-- Constraints for table `WatchedMovies`
--
ALTER TABLE `WatchedMovies`
  ADD CONSTRAINT `WatchedMovies_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `Users` (`UserID`),
  ADD CONSTRAINT `WatchedMovies_ibfk_2` FOREIGN KEY (`MovieID`) REFERENCES `Movies` (`MovieID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
