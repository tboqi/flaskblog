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
CREATE DATABASE /*!32312 IF NOT EXISTS*/`flaskblog2` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `flaskblog2`;

/*Table structure for table `auth_permission_routers` */

DROP TABLE IF EXISTS `auth_permission_routers`;

CREATE TABLE `auth_permission_routers` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `permission_id` int(10) unsigned NOT NULL,
  `is_menu` enum('N','Y') NOT NULL DEFAULT 'N',
  `router` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `auth_permission_routers` */

/*Table structure for table `auth_permissions` */

DROP TABLE IF EXISTS `auth_permissions`;

CREATE TABLE `auth_permissions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `auth_permissions` */

/*Table structure for table `auth_role_permission_ln` */

DROP TABLE IF EXISTS `auth_role_permission_ln`;

CREATE TABLE `auth_role_permission_ln` (
  `permission_id` int(10) unsigned NOT NULL,
  `role_id` int(10) unsigned NOT NULL,
  KEY `userId` (`permission_id`),
  KEY `roleId` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `auth_role_permission_ln` */

insert  into `auth_role_permission_ln`(`permission_id`,`role_id`) values (1,1);
insert  into `auth_role_permission_ln`(`permission_id`,`role_id`) values (2,1);

/*Table structure for table `auth_roles` */

DROP TABLE IF EXISTS `auth_roles`;

CREATE TABLE `auth_roles` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `auth_roles` */

insert  into `auth_roles`(`id`,`name`,`description`) values (1,'superuser','超级管理员');

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
insert  into `auth_users`(`id`,`name`,`email`,`password`,`active`,`created_at`,`role_id`) values (2,'test2','test2','$pbkdf2-sha512$25000$7F1rTUlJ6R3j/D.H8F7L.Q$NlPv6BuuxcGnCmS6yDxB0cexXrlxh5WPYTXtV9QX8usm7AqEviVJxbZDn8XsYvNM0AiAggsExkBRxYKmEWQWFw','true','2017-12-20 10:00:00',0);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
