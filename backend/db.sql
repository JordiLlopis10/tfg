CREATE DATABASE IF NOT EXISTS detalls;
USE detalls;

CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(30) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    imagen VARCHAR(255) NULL
);
CREATE TABLE IF NOT EXISTS pagos (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    productos VARCHAR(255) NOT NULL,
    ciudad VARCHAR(100),
    cp VARCHAR(10),
    provincia VARCHAR(100),
    total DECIMAL(10,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS reset_tokens (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  token VARCHAR(255) NOT NULL,
  expires_at DATETIME NOT NULL
);


-- Poblar la tabla de usuarios, para poder acceder a la ruta administrador y poder crear un nuevo usuario admin con la contraseña haseada
INSERT INTO users (email, password) VALUES
('llopisgodinojordi@gmail.com', 'valenciacf:)')

-- Poblar la tabla de productos
INSERT INTO productos (nombre, descripcion, precio, stock, imagen) VALUES
('Oso de peluche', 'Oso de peluche 20x10cm perfecto para niños pequeños', 18.00, 50, 'https://res.cloudinary.com/dmn0n4o5n/image/upload/v1749122910/oso_peluche_ihfp0m.png'),
