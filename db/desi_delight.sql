--
-- Table structure for table `menu_items`
--

DROP TABLE IF EXISTS menu_items;
CREATE TABLE menu_items (
  item_id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  description VARCHAR(1000),
  price DECIMAL(10,2),
  category VARCHAR(100),  -- New category column
  image_url VARCHAR(255)
);

INSERT INTO menu_items (name, description, price, category, image_url) VALUES 
('Biryani', 'A hearty serving of Sindhi Biryani topped with two tender chicken pieces.', 400, 'main dish', 'https://media.istockphoto.com/id/1453499717/photo/chicken-biryani-or-biriyani-served-in-plate-isolated-on-table-top-view-indian-spicy-food.jpg?s=612x612&w=0&k=20&c=tBMCVZt7CW0KRBqkRg-MDySzxMiQqzUamGU9IHnH13Q='),
('Nihari', 'A rich and flavorful plate of Beef Nihari served with two pieces of chicken.', 400, 'main dish', 'https://img.freepik.com/premium-photo/spicy-beef-nihari-served-plate-isolated-background-top-view-indian-pakistani-desi-food_689047-3097.jpg'),
('Daal Makhni', 'Creamy Daal Makhni, perfect for a comforting meal.', 300, 'main dish', 'https://5.imimg.com/data5/SELLER/Default/2023/9/345465731/JQ/IR/EX/91848690/ready-to-eat-dal-makhani.jpg'),
('Chicken Karahi', 'Generous portion of Chicken Karahi, cooked to perfection.', 600, 'main dish', 'https://hinzcooking.com/wp-content/uploads/2020/12/chicken-karahi-recipe.jpg'),
('Rasmalai', 'Delicate rasmalai served with three sweet dumplings in creamy milk.', 200, 'sweet', 'https://premiumsweets.ca/wp-content/uploads/2023/10/1612796724-1024x769.jpg'),
('Naan', 'Warm, freshly baked naan bread.', 30, 'add on', 'https://thebusybaker.ca/wp-content/uploads/2022/02/homemade-naan-bread-fb-ig-4-scaled.jpg'),
('Paratha', 'Flaky and layered lachedar paratha.', 50, 'add on', 'https://rookiewithacookie.com/wp-content/uploads/2020/05/IMG_2570.jpg'),
('Soft Drink', 'Chilled bottle of Pepsi to quench your thirst.', 75, 'drink', 'https://cdn.mafrservices.com/sys-master-root/hc5/hef/51636415332382/332818_main.jpg?im=Resize=1700'),
('Lassi', 'Refreshing glass of chilled lassi, perfect for any meal.', 100, 'drink', 'https://assets.bonappetit.com/photos/60ef61ef7009278ef6bad579/master/pass/Lassi.jpg');

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
