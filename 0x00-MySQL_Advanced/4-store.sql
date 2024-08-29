-- This script creates a trigger that decreases the quantity of an item
-- in the items table after a new order is added to the orders table.

-- This is a delimiter
DELIMITER //

CREATE TRIGGER update_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;

//

DELIMITER ;
