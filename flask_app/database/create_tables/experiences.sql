CREATE TABLE IF NOT EXISTS `experiences` (
`experience_id`     int(11)       NOT NULL AUTO_INCREMENT  COMMENT 'The experience id',
`position_id`       int(11)       NOT NULL                COMMENT 'FK: The position id',
`name`              varchar(255)  NOT NULL                COMMENT 'Name of the experience',
`description`       text          DEFAULT NULL            COMMENT 'Description of the experience',
`hyperlink`         varchar(255)  DEFAULT NULL            COMMENT 'Link to learn more about the experience',
`start_date`        date          DEFAULT NULL            COMMENT 'Start date of the experience',
`end_date`          date          DEFAULT NULL            COMMENT 'End date of the experience',
PRIMARY KEY (`experience_id`),
FOREIGN KEY (`position_id`) REFERENCES `positions`(`position_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Experiences associated with positions';
