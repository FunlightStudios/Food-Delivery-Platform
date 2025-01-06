-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Erstellungszeit: 06. Jan 2025 um 04:49
-- Server-Version: 8.0.40
-- PHP-Version: 8.3.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `swisseat`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `cart`
--

CREATE TABLE `cart` (
  `id` tinyint NOT NULL,
  `user_id` tinyint DEFAULT NULL,
  `restaurant_id` tinyint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Daten für Tabelle `cart`
--

INSERT INTO `cart` (`id`, `user_id`, `restaurant_id`) VALUES
(2, 5, 2),
(3, 2, 2);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `cart_item`
--

CREATE TABLE `cart_item` (
  `id` tinyint NOT NULL,
  `cart_id` tinyint DEFAULT NULL,
  `menu_item_id` tinyint DEFAULT NULL,
  `quantity` tinyint DEFAULT NULL,
  `price` decimal(3,1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Daten für Tabelle `cart_item`
--

INSERT INTO `cart_item` (`id`, `cart_id`, `menu_item_id`, `quantity`, `price`) VALUES
(2, 2, 4, 2, 2.5),
(3, 2, 2, 3, 10.5),
(4, 2, 3, 1, 8.5),
(23, 3, 5, 2, 2.5),
(26, 3, 3, 2, 8.5);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `cms_site_infos`
--

CREATE TABLE `cms_site_infos` (
  `id` int NOT NULL,
  `variable` varchar(200) DEFAULT NULL,
  `content` varchar(250) DEFAULT NULL,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Daten für Tabelle `cms_site_infos`
--

INSERT INTO `cms_site_infos` (`id`, `variable`, `content`, `updated_at`) VALUES
(1, 'brandname', 'SwissEat', '2025-01-03 15:00:53'),
(2, 'company', 'SwissEat GmbH', '2025-01-03 15:00:53'),
(3, 'mail_info', 'info@swisseat.ch', '2025-01-04 01:22:57'),
(4, 'mail_support', 'support@swisseat.ch', '2025-01-04 01:22:57'),
(5, 'mail_webadmin', 'it@swisseat.ch', '2025-01-04 01:24:52'),
(6, 'tel_support', '+41771231212', '2025-01-04 01:24:52'),
(7, 'address', 'Orpundstrasse 12, 2504 Biel, Schweiz', '2025-01-04 01:57:18'),
(9, 'features_title', 'Warum SwissEat?', '2025-01-04 02:03:00'),
(10, 'features_icon_1', 'fas fa-utensils', '2025-01-04 02:03:00'),
(11, 'features_title_1', 'Faire Bedingungen', '2025-01-04 02:08:30'),
(12, 'features_content_1', 'Restaurants profitieren von fairen Bedingungen. Erfahren Sie mehr unter', '2025-01-04 02:08:30'),
(13, 'features_icon_2', 'fas fa-truck', '2025-01-04 02:08:30'),
(14, 'features_title_2', 'Restaurants liefern', '2025-01-04 02:08:30'),
(15, 'features_content_2', 'Die Restaurants liefern selbst und können so Lieferrouten deutlich besser planen', '2025-01-04 02:08:30'),
(16, 'features_icon_3', 'fas fa-star', '2025-01-04 02:08:30'),
(17, 'features_title_3', 'Top Bewertungen', '2025-01-04 02:08:30'),
(18, 'features_content_3', 'Von unseren zufriedenen Kunden und Restaurants', '2025-01-04 02:08:30'),
(19, 'footer_info_title', 'Über SwissEat', '2025-01-04 02:34:36'),
(20, 'footer_info_content', 'Ihre vertrauenswürdige Plattform für Essenslieferungen und Fairen Bedingungen für Restaurants in der Schweiz.', '2025-01-04 02:34:36');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `menu_item`
--

CREATE TABLE `menu_item` (
  `id` tinyint NOT NULL,
  `name` varchar(16) DEFAULT NULL,
  `description` varchar(18) DEFAULT NULL,
  `price` decimal(3,1) DEFAULT NULL,
  `category` varchar(13) DEFAULT NULL,
  `restaurant_id` tinyint DEFAULT NULL,
  `is_available` tinyint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Daten für Tabelle `menu_item`
--

INSERT INTO `menu_item` (`id`, `name`, `description`, `price`, `category`, `restaurant_id`, `is_available`) VALUES
(1, 'Test', '', 34.0, 'hauptgerichte', 1, 1),
(2, 'Pizza Margaritta', 'Premium Margaritta', 10.5, 'hauptgerichte', 2, 1),
(3, 'Cesar Salat', '', 8.5, 'vorspeisen', 2, 1),
(4, 'Ice Tea 1L', 'M-Classic Citrone', 2.5, 'getranke', 2, 1),
(5, 'Ice Tea 1L', 'M-Classic Peach', 2.5, 'getranke', 2, 1),
(6, 'Coca-Cola 33cl', 'Dose', 2.0, 'getranke', 2, 1),
(7, 'Coca-Cola 0.5l', 'Flasche', 3.2, 'getranke', 2, 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `order`
--

CREATE TABLE `order` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `restaurant_id` int DEFAULT NULL,
  `status` varchar(7) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `delivered_at` datetime DEFAULT NULL,
  `cancelled_at` datetime DEFAULT NULL,
  `delivery_address` varchar(255) DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `payment_method` varchar(10) DEFAULT NULL,
  `date_ordered` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Daten für Tabelle `order`
--

INSERT INTO `order` (`id`, `user_id`, `restaurant_id`, `status`, `created_at`, `delivered_at`, `cancelled_at`, `delivery_address`, `total_amount`, `payment_method`, `date_ordered`) VALUES
(1, 2, 2, 'pending', '2025-01-02 00:00:00', NULL, NULL, 'Jurastrasse 9, 2552 Orpund', 49.20, 'twint', '2024-01-01 12:00:00'),
(2, 2, 2, 'pending', '2025-01-02 00:00:00', NULL, NULL, 'Jurastrasse 9, 2552 Orpund', 23.00, 'cash', '2024-01-01 12:00:00'),
(3, 2, 2, 'pending', '2025-01-03 00:46:32', NULL, NULL, 'Jurastrasse 9, 2552 Orpund', 126.50, 'cash', '2025-01-03 00:42:30');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `order_item`
--

CREATE TABLE `order_item` (
  `id` tinyint NOT NULL,
  `order_id` tinyint DEFAULT NULL,
  `menu_item_id` tinyint DEFAULT NULL,
  `quantity` tinyint DEFAULT NULL,
  `price_at_time` decimal(3,1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Daten für Tabelle `order_item`
--

INSERT INTO `order_item` (`id`, `order_id`, `menu_item_id`, `quantity`, `price_at_time`) VALUES
(1, 1, 7, 1, 3.2),
(2, 1, 4, 7, 2.5),
(3, 1, 2, 2, 10.5),
(4, 1, 5, 1, 2.5),
(5, 2, 4, 2, 2.5),
(6, 2, 5, 1, 2.5),
(7, 2, 2, 1, 10.5),
(8, 3, 4, 9, 2.5),
(9, 3, 2, 1, 10.5),
(10, 3, 2, 1, 10.5),
(11, 3, 2, 1, 10.5),
(12, 3, 5, 1, 2.5),
(13, 3, 2, 1, 10.5),
(14, 3, 2, 1, 10.5),
(15, 3, 2, 1, 10.5),
(16, 3, 2, 1, 10.5),
(17, 3, 2, 1, 10.5),
(18, 3, 2, 1, 10.5),
(19, 3, 6, 1, 2.0);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `restaurant`
--

CREATE TABLE `restaurant` (
  `id` tinyint NOT NULL,
  `name` varchar(13) DEFAULT NULL,
  `description` varchar(140) DEFAULT NULL,
  `address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cuisine_type` varchar(12) DEFAULT NULL,
  `rating` decimal(2,1) DEFAULT NULL,
  `delivery_time` tinyint DEFAULT NULL,
  `minimum_order` decimal(3,1) DEFAULT NULL,
  `delivery_fee` decimal(2,1) DEFAULT NULL,
  `accepts_cash` tinyint DEFAULT NULL,
  `accepts_twint` tinyint DEFAULT NULL,
  `accepts_paypal` tinyint DEFAULT NULL,
  `is_active` tinyint DEFAULT NULL,
  `owner_id` tinyint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Daten für Tabelle `restaurant`
--

INSERT INTO `restaurant` (`id`, `name`, `description`, `address`, `cuisine_type`, `rating`, `delivery_time`, `minimum_order`, `delivery_fee`, `accepts_cash`, `accepts_twint`, `accepts_paypal`, `is_active`, `owner_id`) VALUES
(1, 'Tonis Pzzeria', 'Test', 'Hauptstrasse 83, 2552 Orpund', 'italienisch', 0.0, 15, 15.0, 5.0, 1, 1, 1, 1, 1),
(2, 'Pizza Bienna', 'Fleischdeklaration\r\nPoulet: Brasilien\r\nRindfleisch: Schweiz\r\nTruthahn: Frankreich\r\nSchinken: Frankreich\r\nLachs: Norwegen\r\nCrevetten: Vietnam', 'Geyisriedweg 2, 2504 Biel', 'italienisch', 0.0, 30, 15.0, 5.0, 1, 1, 1, 1, 3),
(3, 'KüBBan', '', 'Altstadt 2, 2502 Biel', 'amerikanisch', 0.0, 45, 15.0, 5.0, 1, 1, 1, 1, 4),
(4, 'Test', 'wq', 'Geyisriedwerrrrrg 2, 2504 Biel', 'italienisch', 0.0, 3, 0.0, 0.0, 1, 1, 1, 0, 5);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `review`
--

CREATE TABLE `review` (
  `id` int NOT NULL,
  `content` varchar(0) DEFAULT NULL,
  `rating` varchar(0) DEFAULT NULL,
  `date_posted` varchar(0) DEFAULT NULL,
  `user_id` varchar(0) DEFAULT NULL,
  `restaurant_id` varchar(0) DEFAULT NULL,
  `order_id` varchar(0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `user`
--

CREATE TABLE `user` (
  `id` int NOT NULL,
  `username` varchar(14) DEFAULT NULL,
  `email` varchar(18) DEFAULT NULL,
  `password` varchar(60) DEFAULT NULL,
  `role` varchar(16) DEFAULT NULL,
  `address` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `phone` varchar(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Daten für Tabelle `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`, `role`, `address`, `phone`) VALUES
(1, 'Tonis Pizzeria', 'owner@example.com', '$2b$12$JcL5cZUmANMegEkcNWr7C.g0Grd3Tmz5cc5047kX4Ls7L8rS/Y5MG', 'restaurant_owner', 'Examplestr. 01, 2345 Example City', '+4112312312'),
(2, 'Jerry', 'user@example.com', '$2b$12$rB4Dovu40T/EZ/LYp2JqzuqnYXP1mlcgFNyzkpeXGIi/qyox5iNkq', 'customer', 'Examplestr. 01, 2345 Example City', '+4112312312'),
(3, 'Mett Pizza', 'owner1@example.com', '$2b$12$ZggqQpDL8FGPDMI0ALQ4dexq6RuAqKKGEuxw/ECCNmZKKIc/smvzK', 'restaurant_owner', 'Examplestr. 01, 2345 Example City', '+4112312312'),
(4, 'KüBBan', 'owner2@example.com', '$2b$12$LWliYnYU0dQgBRdpzywXzeoxcHVEev9VWQzuVN9nGQ5xqbjcQOV5S', 'restaurant_owner', 'Examplestr. 01, 2345 Example City', '+4112312312'),
(5, '444', 'owner3@example.com', '$2b$12$JO12Aijb9.rDYMDQHwdab.5WdR98EZnai5KBN1PSH8kCrESAMMtWC', 'restaurant_owner', 'Examplestr. 01, 2345 Example City', '+4112312312');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `user_address`
--

CREATE TABLE `user_address` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(100) NOT NULL,
  `zipcode` varchar(20) NOT NULL,
  `country` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Daten für Tabelle `user_address`
--

INSERT INTO `user_address` (`id`, `user_id`, `street`, `city`, `zipcode`, `country`) VALUES
(1, 1, 'Examplestr. 01', 'Example City', '2345', 'Switzerland'),
(2, 2, 'Example City', 'Example City', '2345', 'Switzerland'),
(3, 3, 'Example City', 'Example City', '2345', 'Switzerland'),
(4, 4, 'Example City', 'Example City', '2345', 'Switzerland'),
(5, 5, 'Example City', 'Example City', '2345', 'Switzerland');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `cart_item`
--
ALTER TABLE `cart_item`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `cms_site_infos`
--
ALTER TABLE `cms_site_infos`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `menu_item`
--
ALTER TABLE `menu_item`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `order_item`
--
ALTER TABLE `order_item`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `restaurant`
--
ALTER TABLE `restaurant`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `user_address`
--
ALTER TABLE `user_address`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `cart`
--
ALTER TABLE `cart`
  MODIFY `id` tinyint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT für Tabelle `cart_item`
--
ALTER TABLE `cart_item`
  MODIFY `id` tinyint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT für Tabelle `cms_site_infos`
--
ALTER TABLE `cms_site_infos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT für Tabelle `menu_item`
--
ALTER TABLE `menu_item`
  MODIFY `id` tinyint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT für Tabelle `order`
--
ALTER TABLE `order`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT für Tabelle `order_item`
--
ALTER TABLE `order_item`
  MODIFY `id` tinyint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT für Tabelle `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `id` tinyint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT für Tabelle `review`
--
ALTER TABLE `review`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT für Tabelle `user_address`
--
ALTER TABLE `user_address`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `user_address`
--
ALTER TABLE `user_address`
  ADD CONSTRAINT `user_address_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
