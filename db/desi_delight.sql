--
-- Table structure for table `menu_items`
--

DROP TABLE IF EXISTS menu_items;
CREATE TABLE menu_items (
  item_id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  description VARCHAR(1000),
  price DECIMAL(10,2)
);

-- Inserting data into the menu_items table
INSERT INTO menu_items (name, description, price) VALUES 
('Biryani', 'One large plate of Sindhi Biryani with 2 chicken pieces.', 400),
('Nihari', 'One large plate of Beef Nihari with 2 chicken pieces.', 400),
('Daal Makhni', 'One large plate of Daal Makhni', 300),
('Chicken Karahi', 'One large plate full of Chicken Karahi', 600),
('Rasmalai', 'One bowl of rasmalai with 3 dumplings', 200),
('Naan', 'Fresh Naan', 30),
('Paratha', 'Lachedar Paratha', 50),
('Soft Drink', 'Bottle of Pepsi', 75),
('Lassi', 'Glass of Fresh Chilled Lassi', 100);

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  order_id SERIAL PRIMARY KEY,
  bill DECIMAL(10,2), 
  status VARCHAR(255) CHECK (status IN ('cooking','delivering','delivered'))
);

-- Inserting data into the orders table
INSERT INTO orders (bill, status) VALUES 
(1400, 'cooking'),
(1300, 'delivering'),
(535, 'delivered');

--
-- Table structure for table `orders_details`
--

DROP TABLE IF EXISTS orders_details;
CREATE TABLE orders_details (
  order_id INT NOT NULL,
  item_id INT NOT NULL,
  quantity INT,
  total_price DECIMAL(10,2),
  PRIMARY KEY (order_id, item_id),
  FOREIGN KEY (item_id) REFERENCES menu_items(item_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Inserting data into the orders_details table
INSERT INTO orders_details (order_id, item_id, quantity, total_price) VALUES 
(1, 1, 2, 800),(1, 3, 1, 600),
(2, 4, 3, 600),(2, 6, 2, 100),(2, 3, 1, 600),
(3, 2, 1, 400),(3, 5, 2, 60),(3, 7, 1, 75);

-- Function to get price for an item
DROP FUNCTION IF EXISTS get_price_for_item;
CREATE FUNCTION get_price_for_item(p_item_name VARCHAR(255)) 
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql AS $$
DECLARE
    v_price DECIMAL(10,2);
BEGIN
    -- Check if the item_name exists in the menu_items table
    SELECT price INTO v_price
    FROM menu_items
    WHERE name = p_item_name;
    IF FOUND THEN
        RETURN v_price;
    ELSE
        -- Invalid item_name, return -1
        RETURN -1;
    END IF;
END;
$$;

-- Function to get id for an item
DROP FUNCTION IF EXISTS get_id_for_item;
CREATE FUNCTION get_id_for_item(p_item_name VARCHAR(255)) 
RETURNS INT
LANGUAGE plpgsql AS $$
DECLARE
    r_item_id INT;
BEGIN
    -- Check if the item_name exists in the menu_items table
    SELECT item_id INTO r_item_id
    FROM menu_items
    WHERE name = p_item_name;
    IF FOUND THEN
        RETURN r_item_id;
    ELSE
        -- Invalid item_name, return -1
        RETURN -1;
    END IF;
END;
$$;
