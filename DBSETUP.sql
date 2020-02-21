-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`user` ;

CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `userID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(45) NULL,
  PRIMARY KEY (`userID`),
  UNIQUE INDEX `userID_UNIQUE` (`userID` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Developers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Developers` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Developers` (
  `devID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_userID` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`devID`),
  INDEX `fk_Developers_user_idx` (`user_userID` ASC) VISIBLE,
  CONSTRAINT `fk_Developers_user`
    FOREIGN KEY (`user_userID`)
    REFERENCES `mydb`.`user` (`userID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`gameMaster`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`gameMaster` ;

CREATE TABLE IF NOT EXISTS `mydb`.`gameMaster` (
  `GMID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_userID` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`GMID`),
  INDEX `fk_gameMaster_user1_idx` (`user_userID` ASC) VISIBLE,
  CONSTRAINT `fk_gameMaster_user1`
    FOREIGN KEY (`user_userID`)
    REFERENCES `mydb`.`user` (`userID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Routes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Routes` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Routes` (
  `routeID` INT ZEROFILL NOT NULL,
  `Node` VARCHAR(45) NOT NULL,
  `NodeID` INT NOT NULL,
  `RouteName` VARCHAR(45) NOT NULL,
  `gameMaster_GMID` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`routeID`),
  UNIQUE INDEX `routeID_UNIQUE` (`routeID` ASC) VISIBLE,
  INDEX `fk_Routes_gameMaster1_idx` (`gameMaster_GMID` ASC) VISIBLE,
  CONSTRAINT `fk_Routes_gameMaster1`
    FOREIGN KEY (`gameMaster_GMID`)
    REFERENCES `mydb`.`gameMaster` (`GMID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Photos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Photos` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Photos` (
  `PhotoPath` VARCHAR(300) NOT NULL,
  `gameMaster_GMID` INT UNSIGNED NOT NULL,
  `Routes_routeID` INT ZEROFILL NOT NULL,
  PRIMARY KEY (`PhotoPath`, `gameMaster_GMID`, `Routes_routeID`),
  INDEX `fk_Photos_gameMaster1_idx` (`gameMaster_GMID` ASC) VISIBLE,
  INDEX `fk_Photos_Routes1_idx` (`Routes_routeID` ASC) VISIBLE,
  CONSTRAINT `fk_Photos_gameMaster1`
    FOREIGN KEY (`gameMaster_GMID`)
    REFERENCES `mydb`.`gameMaster` (`GMID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Photos_Routes1`
    FOREIGN KEY (`Routes_routeID`)
    REFERENCES `mydb`.`Routes` (`routeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Hints`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Hints` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Hints` (
  `HintText` VARCHAR(100) NOT NULL,
  `HintNo` INT NOT NULL,
  `Routes_routeID` INT ZEROFILL NOT NULL,
  `Routs_NodeID` INT NOT NULL,
  PRIMARY KEY (`HintText`),
  INDEX `fk_Hints_Routes1_idx` (`Routes_routeID` ASC) VISIBLE,
  CONSTRAINT `fk_Hints_Routes1`
    FOREIGN KEY (`Routes_routeID`)
    REFERENCES `mydb`.`Routes` (`routeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Players`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Players` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Players` (
  `playerID` INT NOT NULL AUTO_INCREMENT,
  `user_userID` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`playerID`),
  UNIQUE INDEX `playerID_UNIQUE` (`playerID` ASC) VISIBLE,
  INDEX `fk_Players_user1_idx` (`user_userID` ASC) VISIBLE,
  CONSTRAINT `fk_Players_user1`
    FOREIGN KEY (`user_userID`)
    REFERENCES `mydb`.`user` (`userID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Groups`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Groups` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Groups` (
  `GroupID` INT NOT NULL AUTO_INCREMENT,
  `GroupName` VARCHAR(45) NOT NULL,
  `Players_playerID` INT NOT NULL,
  PRIMARY KEY (`GroupID`),
  UNIQUE INDEX `GroupID_UNIQUE` (`GroupID` ASC) VISIBLE,
  INDEX `fk_Groups_Players1_idx` (`Players_playerID` ASC) VISIBLE,
  CONSTRAINT `fk_Groups_Players1`
    FOREIGN KEY (`Players_playerID`)
    REFERENCES `mydb`.`Players` (`playerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
