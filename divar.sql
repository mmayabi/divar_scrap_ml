CREATE TABLE `buyapartment` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `price` int(11) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `metraj` int(11) DEFAULT NULL,
  `sakht` int(11) DEFAULT NULL,
  `otagh` int(11) DEFAULT NULL,
  `asansor` tinyint(1) DEFAULT NULL,
  `parking` tinyint(1) DEFAULT NULL,
  `anbari` tinyint(1) DEFAULT NULL,
  `floor` int(11) DEFAULT NULL,
  `link` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
