/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 100427
 Source Host           : localhost:3306
 Source Schema         : restaurante

 Target Server Type    : MySQL
 Target Server Version : 100427
 File Encoding         : 65001

 Date: 16/05/2023 17:58:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `price` decimal(8, 2) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, 'Hamburguesa', 'Carne, lechuga, tomate, cebolla y queso', 10.00);
INSERT INTO `menu` VALUES (2, 'Pizza', 'Masa, salsa de tomate, queso y pepperoni', 12.00);
INSERT INTO `menu` VALUES (3, 'Ensalada', 'Lechuga, tomate, pepino y aderezo', 8.00);
INSERT INTO `menu` VALUES (4, 'Refresco', 'Coca Cola, Sprite, Fanta', 3.00);

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `table_id` int NOT NULL,
  `reservation_id` int NOT NULL,
  `menu_id` int NOT NULL,
  `quantity` int NOT NULL,
  `status` enum('pending','completed') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'pending',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `table_id`(`table_id`) USING BTREE,
  INDEX `menu_id`(`menu_id`) USING BTREE,
  INDEX `reservation_id`(`reservation_id`) USING BTREE,
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `tables` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`reservation_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES (1, 1, 1, 1, 10, 'pending');
INSERT INTO `orders` VALUES (2, 2, 2, 2, 2, 'pending');

-- ----------------------------
-- Table structure for reservations
-- ----------------------------
DROP TABLE IF EXISTS `reservations`;
CREATE TABLE `reservations`  (
  `reservation_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `table_id` int NULL DEFAULT NULL,
  `comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `reservation_date` date NULL DEFAULT NULL,
  `start_time` time(0) NULL DEFAULT NULL,
  `end_time` time(0) NULL DEFAULT NULL,
  `status` enum('open','close') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`reservation_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `table_id`(`table_id`) USING BTREE,
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`table_id`) REFERENCES `tables` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reservations
-- ----------------------------
INSERT INTO `reservations` VALUES (1, NULL, 1, 'test', '2023-05-16', '15:15:40', '15:17:53', 'close');
INSERT INTO `reservations` VALUES (2, NULL, 2, 'test', '2023-05-16', '15:16:21', NULL, 'open');
INSERT INTO `reservations` VALUES (3, NULL, 1, 'test', '2023-05-16', '15:18:00', NULL, 'open');

-- ----------------------------
-- Table structure for tables
-- ----------------------------
DROP TABLE IF EXISTS `tables`;
CREATE TABLE `tables`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` enum('close','open') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tables
-- ----------------------------
INSERT INTO `tables` VALUES (1, 'Mesa 1', 'open');
INSERT INTO `tables` VALUES (2, 'Mesa 2', 'open');
INSERT INTO `tables` VALUES (3, 'Mesa 3', 'close');
INSERT INTO `tables` VALUES (4, 'Mesa 4', 'close');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` int NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `user_type` enum('customer','employee') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'John Doe', 'johndoe@example.com', '+1 555-123-4567', '123 Main St, Anytown USA', 'employee');
INSERT INTO `users` VALUES (2, 'Jane Smith', 'janesmith@example.com', '+1 555-987-6543', '456 Elm St, Anytown USA', 'employee');
INSERT INTO `users` VALUES (3, 'Bob Johnson', 'bobjohnson@example.com', '+1 555-555-1212', '789 Maple St, Anytown USA', 'employee');

SET FOREIGN_KEY_CHECKS = 1;
