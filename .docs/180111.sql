/*
SQLyog Professional v12.08 (64 bit)
MySQL - 5.7.18-log : Database - flaskblog2
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`flaskblog2` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `flaskblog2`;

/*Table structure for table `article_categories` */

DROP TABLE IF EXISTS `article_categories`;

CREATE TABLE `article_categories` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

/*Data for the table `article_categories` */

insert  into `article_categories`(`id`,`name`) values (6,'dfgdfg');

/*Table structure for table `articles` */

DROP TABLE IF EXISTS `articles`;

CREATE TABLE `articles` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `author_id` int(10) unsigned NOT NULL,
  `category_id` int(10) unsigned NOT NULL,
  `tags` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cid` (`category_id`),
  CONSTRAINT `cid` FOREIGN KEY (`category_id`) REFERENCES `article_categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `articles` */

insert  into `articles`(`id`,`title`,`content`,`created_at`,`updated_at`,`author_id`,`category_id`,`tags`) values (1,'斯蒂芬森的','<p>斯蒂芬斯蒂芬斯蒂芬森</p>\r\n','2018-01-11 11:19:22','2018-01-11 11:19:22',2,6,',斯蒂芬森,');

/*Table structure for table `auth_permissions` */

DROP TABLE IF EXISTS `auth_permissions`;

CREATE TABLE `auth_permissions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

/*Data for the table `auth_permissions` */

insert  into `auth_permissions`(`id`,`name`) values (1,'管理员管理权限');
insert  into `auth_permissions`(`id`,`name`) values (2,'文章管理');
insert  into `auth_permissions`(`id`,`name`) values (3,'系统管理');
insert  into `auth_permissions`(`id`,`name`) values (4,'后台基础页面');

/*Table structure for table `auth_role_permission_ln` */

DROP TABLE IF EXISTS `auth_role_permission_ln`;

CREATE TABLE `auth_role_permission_ln` (
  `permission_id` int(10) unsigned NOT NULL,
  `role_id` int(10) unsigned NOT NULL,
  KEY `userId` (`permission_id`),
  KEY `roleId` (`role_id`),
  CONSTRAINT `pid` FOREIGN KEY (`permission_id`) REFERENCES `auth_permissions` (`id`),
  CONSTRAINT `rid` FOREIGN KEY (`role_id`) REFERENCES `auth_roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `auth_role_permission_ln` */

insert  into `auth_role_permission_ln`(`permission_id`,`role_id`) values (1,1);
insert  into `auth_role_permission_ln`(`permission_id`,`role_id`) values (2,1);
insert  into `auth_role_permission_ln`(`permission_id`,`role_id`) values (4,1);
insert  into `auth_role_permission_ln`(`permission_id`,`role_id`) values (3,1);

/*Table structure for table `auth_roles` */

DROP TABLE IF EXISTS `auth_roles`;

CREATE TABLE `auth_roles` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `auth_roles` */

insert  into `auth_roles`(`id`,`name`,`description`) values (1,'超级管理员','超级管理员');

/*Table structure for table `auth_routers` */

DROP TABLE IF EXISTS `auth_routers`;

CREATE TABLE `auth_routers` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `permission_id` int(10) unsigned NOT NULL,
  `category` enum('menu','not menu') NOT NULL DEFAULT 'not menu',
  `router` varchar(100) NOT NULL,
  `parent_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

/*Data for the table `auth_routers` */

insert  into `auth_routers`(`id`,`name`,`permission_id`,`category`,`router`,`parent_id`) values (1,'角色列表',1,'menu','/admin/role',6);
insert  into `auth_routers`(`id`,`name`,`permission_id`,`category`,`router`,`parent_id`) values (2,'管理员列表',1,'menu','/admin/user',6);
insert  into `auth_routers`(`id`,`name`,`permission_id`,`category`,`router`,`parent_id`) values (3,'权限列表',1,'menu','/admin/permission',6);
insert  into `auth_routers`(`id`,`name`,`permission_id`,`category`,`router`,`parent_id`) values (4,'路由列表',1,'menu','/admin/router',9);
insert  into `auth_routers`(`id`,`name`,`permission_id`,`category`,`router`,`parent_id`) values (6,'管理员管理',1,'menu','/admin/auth/*',0);
insert  into `auth_routers`(`id`,`name`,`permission_id`,`category`,`router`,`parent_id`) values (9,'文章列表',2,'menu','/admin/article',10);
insert  into `auth_routers`(`id`,`name`,`permission_id`,`category`,`router`,`parent_id`) values (10,'文章管理',2,'menu','/admin/article/*',0);
insert  into `auth_routers`(`id`,`name`,`permission_id`,`category`,`router`,`parent_id`) values (11,'/admin/',4,'not menu','/admin/',0);
insert  into `auth_routers`(`id`,`name`,`permission_id`,`category`,`router`,`parent_id`) values (12,'/admin/welcome',4,'not menu','/admin/welcome',0);

/*Table structure for table `auth_users` */

DROP TABLE IF EXISTS `auth_users`;

CREATE TABLE `auth_users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `active` enum('true','false') NOT NULL DEFAULT 'true',
  `created_at` datetime NOT NULL,
  `role_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `auth_users` */

insert  into `auth_users`(`id`,`name`,`email`,`password`,`active`,`created_at`,`role_id`) values (1,'test1','test1','$pbkdf2-sha512$25000$5vy/N2bMec9Z650zJiQkpA$C2HmzcwKNJTDoUa/M4v/DIUnM1pkX4mn1XlSoVEbwqrvRQddSF.XVkeqi0uXXOOUjPFVu2vGqSZSUaYoXbEI/w','true','2017-12-21 09:53:57',1);
insert  into `auth_users`(`id`,`name`,`email`,`password`,`active`,`created_at`,`role_id`) values (2,'admin','admin','$pbkdf2-sha512$25000$P6c0RkgJwbhXqjVmbM1Ziw$0V.q7Nn6aGmYtboK1Py7Z4Oq0mI4t/btvKU0Ix3LOLdtNrf7IkvxAFErsv7LmKJXsjCT14MC8KlE03ki2Eeu5g','true','2017-12-28 14:57:02',1);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
