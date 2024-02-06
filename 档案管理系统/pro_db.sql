create DATABASE `pro_pro`;
use `pro_pro`;
DROP TABLE IF EXISTS admin;
CREATE TABLE `admin` (
  `admin_id` varchar(20) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` varchar(20) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS user_info;
CREATE TABLE `user_info` (
  `user_id` varchar(20) NOT NULL,
  `姓名` varchar(20) DEFAULT NULL,
  `性别` varchar(5) DEFAULT NULL,
  `年龄` int DEFAULT NULL,
  `所属班级` varchar(10) DEFAULT NULL,
  `毕业去向` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `user_info_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO admin(admin_id,password) VALUES('admin','a123'),('admin1','b123'),('admin2','c123'),('admin3','d123'),('admin4','e123');

INSERT INTO `user`(user_id,password) VALUES('cp','cp666'),('cyf','cyf666'),('cyl','cyl666'),('dsc','dsc666'),('ghw','ghw666'),('hjl','hjl666'),('jst','jst666'),('lm','lm666'),('ls','ls666'),('syq','syq666'),('wq','wq666'),('ww','ww666'),('wxm','wxm666'),('wyf','wyf666'),('xlq','xlq666'),('zdh','zdh666'),('zh','zh666'),('zjr','zjr666'),('zs','zs666'),('zsj','zsj666'),('zxh','zxh666'),('zxx','zxx666');
INSERT INTO user_info(user_id,姓名,性别,年龄,所属班级,毕业去向) VALUES('cp','陈鹏','男',21,'电信2001','就业'),('dsc','邓森晁','男',21,'电信2002','考研'),('ghw','关昊文','男',21,'电信2003','就业'),('wyf','王宇菲','女',21,'电信2001','就业'),('xlq','徐力强','男',21,'电信2002','就业'),('zjr','曾静如','女',21,'电信2003','考研'),('zsj','翟偲杰','男',21,'电信2001','考研');
