CREATE TABLE IF NOT EXISTS `skills` (
`skill_id`          int(11)       NOT NULL AUTO_INCREMENT  COMMENT 'The skill id',
`experience_id`     int(11)       NOT NULL                COMMENT 'FK: The experience id',
`name`              varchar(255)  NOT NULL                COMMENT 'Name of the skill',
`skill_level`       int(11)       NOT NULL                COMMENT 'Skill level (1-10)',
PRIMARY KEY (`skill_id`),
FOREIGN KEY (`experience_id`) REFERENCES `experiences`(`experience_id`),
CHECK (`skill_level` >= 1 AND `skill_level` <= 10)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Skills associated with experiences';
