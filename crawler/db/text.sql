CREATE DATABASE text;

USE text;

CREATE TABLE `Files` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `full_name` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `FilesText` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `fileId` int,
  `rawText` longtext,
  `cleanText` longtext,
  `sentence` longtext,
  `words` longtext,
  `created_at` timestamp
);

ALTER TABLE `FilesText` ADD FOREIGN KEY (`fileId`) REFERENCES `Files` (`id`);

INSERT INTO text.Files (full_name) VALUES ('manual_ps5');
INSERT INTO text.Files (full_name) VALUES ('artigo');