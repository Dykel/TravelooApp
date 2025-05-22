/*
  # Initial schema setup for scooter rental application

  1. New Tables
    - `scooters`
      - Basic scooter information and availability
    - `bookings`
      - Booking records and status tracking
    
  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users
*/

-- Create scooters table
CREATE TABLE IF NOT EXISTS scooters (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  model text NOT NULL,
  description text,
  hourly_rate decimal(10,2) NOT NULL,
  daily_rate decimal(10,2) NOT NULL,
  image_url text,
  status text NOT NULL DEFAULT 'available',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create bookings table
CREATE TABLE IF NOT EXISTS bookings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  scooter_id uuid REFERENCES scooters(id),
  user_id uuid REFERENCES auth.users(id),
  start_date timestamptz NOT NULL,
  end_date timestamptz NOT NULL,
  status text NOT NULL DEFAULT 'pending',
  total_amount decimal(10,2) NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE scooters ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;

-- Scooter policies
CREATE POLICY "Scooters are viewable by everyone"
  ON scooters
  FOR SELECT
  TO public
  USING (true);

-- Booking policies
CREATE POLICY "Users can create their own bookings"
  ON bookings
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own bookings"
  ON bookings
  FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_scooters_updated_at
  BEFORE UPDATE ON scooters
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bookings_updated_at
  BEFORE UPDATE ON bookings
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();