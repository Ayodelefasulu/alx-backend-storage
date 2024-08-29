-- This is a table_index_name index

-- Drop the index if it already exists
DROP INDEX IF EXISTS idx_name_first ON names;

-- Create an index on the first letter of the 'name' column
CREATE INDEX idx_name_first ON names (name(1));

