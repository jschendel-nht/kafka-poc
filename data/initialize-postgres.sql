CREATE SCHEMA IF NOT EXISTS member;

CREATE TABLE IF NOT EXISTS member.name (
  profile_id text NOT NULL,
  first_name text NOT NULL,
  last_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS member.address (
  profile_id text NOT NULL,
  address_line_1 text NOT NULL,
  address_line_2 text,
  city text,
  state text,
  zip_code text
);

INSERT INTO member.name VALUES 
  ('A001', 'John', 'Doe'), 
  ('A002', 'Jane', 'Doe');

INSERT INTO member.address VALUES 
  ('A001', '123 Main St', 'Unit 4', 'Denver', 'CO', '80218'), 
  ('A002', '123 Main St', 'Unit 5', 'Denver', 'CO', '80218');
