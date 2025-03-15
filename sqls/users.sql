-- 1. DBA
CREATE USER 'sac_dba'@'localhost' IDENTIFIED BY 'DBApassword';
GRANT ALL PRIVILEGES ON SAC.* TO 'sac_dba'@'localhost' WITH GRANT OPTION;

-- 2. View-Only
CREATE USER 'sac_viewer'@'localhost' IDENTIFIED BY 'ViewerPassword';
GRANT SELECT ON SAC.* TO 'sac_viewer'@'localhost';

-- 3. Admin
CREATE USER 'sac_admin'@'localhost' IDENTIFIED BY 'AdminPassword';
GRANT SELECT, INSERT, UPDATE, DELETE ON SAC.* TO 'sac_admin'@'localhost';