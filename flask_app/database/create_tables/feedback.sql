-- Table to store website visitor feedback and comments
CREATE TABLE IF NOT EXISTS `feedback` (
    `comment_id`   int(11)      NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for feedback entry',
    `name`         varchar(100) NOT NULL               COMMENT 'Name of person providing feedback',
    `email`        varchar(255) NOT NULL               COMMENT 'Email address for contact',
    `comment`      text         NOT NULL               COMMENT 'Feedback content',
    `created_at`   timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Time feedback was submitted',
    `is_displayed` boolean      NOT NULL DEFAULT TRUE   COMMENT 'Whether to display this feedback',
    PRIMARY KEY (`comment_id`),
    -- Adding indexes for common queries
    INDEX `idx_feedback_date` (`created_at`),
    INDEX `idx_feedback_display` (`is_displayed`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4
COMMENT='Website visitor feedback and testimonials';
