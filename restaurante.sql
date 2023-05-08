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

 Date: 08/05/2023 16:04:56
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
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, 'Hamburguesa', 'Carne, lechuga, tomate, cebolla y queso', 10.00);
INSERT INTO `menu` VALUES (2, 'Pizza', 'Masa, salsa de tomate, queso y pepperoni', 12.00);
INSERT INTO `menu` VALUES (3, 'Ensalada', 'Lechuga, tomate, pepino y aderezo', 8.00);
INSERT INTO `menu` VALUES (4, 'Refresco', 'Coca Cola, Sprite, Fanta', 3.00);

-- ----------------------------
-- Table structure for mesas
-- ----------------------------
DROP TABLE IF EXISTS `mesas`;
CREATE TABLE `mesas`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mesas
-- ----------------------------
INSERT INTO `mesas` VALUES (1, 'Mesa 1');
INSERT INTO `mesas` VALUES (2, 'Mesa 2');
INSERT INTO `mesas` VALUES (3, 'Mesa 3');
INSERT INTO `mesas` VALUES (4, 'Mesa 4');

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `table_id` int NOT NULL,
  `menu_id` int NOT NULL,
  `quantity` int NOT NULL,
  `status` enum('pending','completed') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'pending',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `table_id`(`table_id`) USING BTREE,
  INDEX `menu_id`(`menu_id`) USING BTREE,
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `mesas` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES (13, 1, 1, 2, 'pending');
INSERT INTO `orders` VALUES (14, 1, 2, 1, 'pending');
INSERT INTO `orders` VALUES (15, 2, 3, 3, 'completed');
INSERT INTO `orders` VALUES (16, 3, 2, 2, 'completed');
INSERT INTO `orders` VALUES (17, 4, 1, 1, 'pending');
INSERT INTO `orders` VALUES (18, 4, 4, 4, 'pending');

SET FOREIGN_KEY_CHECKS = 1;
