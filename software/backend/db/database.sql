-- Script creación base de datos (no backend)

CREATE DATABASE `dpmodels`;
USE `dpmodels`;


CREATE TABLE `dpmodels`.`CROP_VALUE` (
  `crop` VARCHAR(200) NOT NULL,
  `kc` FLOAT NOT NULL COMMENT 'coeficiente único del cultivo',
  PRIMARY KEY (`CROP`));

CREATE TABLE `dpmodels`.`MODEL_TYPES` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(300) NULL COMMENT 'breve descripción de lo que implica el nuevo tipo de modelo',
  PRIMARY KEY (`ID`));

CREATE TABLE `dpmodels`.`MODELS` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` TEXT NULL COMMENT 'Breve descripción de los objetivos y finalidades del modelo',
  `type` INT NOT NULL,
  `location` VARCHAR(500) NOT NULL COMMENT 'Indica la localización del modelo en el servidor',
  PRIMARY KEY (`ID`),
  CONSTRAINT `FK_MODELS_TYPE`
    FOREIGN KEY (`TYPE`)
    REFERENCES `dpmodels`.`MODEL_TYPES` (`ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

