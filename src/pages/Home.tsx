import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { supabase } from '../lib/supabase';

interface Scooter {
  id: number;
  name: string;
  model: string;
  hourly_rate: number;
  daily_rate: number;
  image_url: string;
  status: string;
}

export default function Home() {
  const [scooters, setScooters] = useState<Scooter[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchScooters() {
      const { data, error } = await supabase
        .from('scooters')
        .select('*')
        .eq('status', 'available');

      if (error) {
        console.error('Error fetching scooters:', error);
        return;
      }

      setScooters(data);
      setLoading(false);
    }

    fetchScooters();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Available Scooters</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {scooters.map((scooter) => (
          <div key={scooter.id} className="bg-white rounded-lg shadow-md overflow-hidden">
            <img
              src={scooter.image_url}
              alt={scooter.name}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <h2 className="text-xl font-semibold mb-2">{scooter.name}</h2>
              <p className="text-gray-600 mb-2">{scooter.model}</p>
              <div className="flex justify-between items-center mb-4">
                <span className="text-gray-600">
                  ${scooter.hourly_rate}/hour
                </span>
                <span className="text-gray-600">
                  ${scooter.daily_rate}/day
                </span>
              </div>
              <Link
                to={`/scooter/${scooter.id}`}
                className="block w-full bg-blue-500 text-white text-center py-2 rounded-md hover:bg-blue-600"
              >
                View Details
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}