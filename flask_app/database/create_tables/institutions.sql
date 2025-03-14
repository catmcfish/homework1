CREATE TABLE IF NOT EXISTS `institutions` (
    `inst_id`    int(11)      NOT NULL AUTO_INCREMENT COMMENT 'The organization id',
    `type`       varchar(100) NOT NULL                COMMENT 'Organization type, e.g. Academia, Industry, Government',
    `name`       varchar(100) NOT NULL                COMMENT 'The name of the organization',
    `department` varchar(100) DEFAULT NULL            COMMENT 'The name of the department or division',
    `address`    varchar(100) DEFAULT NULL            COMMENT 'The address of the institution',
    `city`       varchar(100) DEFAULT NULL            COMMENT 'The city of the institution',
    `state`      varchar(100) DEFAULT NULL            COMMENT 'The state of the institution',
    `zip`        varchar(10)  DEFAULT NULL            COMMENT 'The zip code of the institution',
    PRIMARY KEY (`inst_id`),
    INDEX `idx_inst_type` (`type`),
    INDEX `idx_inst_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Institutions I am affiliated with';