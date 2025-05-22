import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import { supabase } from '../lib/supabase';
import { useAuth } from '../hooks/useAuth';

interface Scooter {
  id: number;
  name: string;
  model: string;
  description: string;
  hourly_rate: number;
  daily_rate: number;
  image_url: string;
  status: string;
}

export default function ScooterDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [scooter, setScooter] = useState<Scooter | null>(null);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchScooter() {
      const { data, error } = await supabase
        .from('scooters')
        .select('*')
        .eq('id', id)
        .single();

      if (error) {
        console.error('Error fetching scooter:', error);
        return;
      }

      setScooter(data);
      setLoading(false);
    }

    fetchScooter();
  }, [id]);

  const handleBooking = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!user) {
      navigate('/login');
      return;
    }

    try {
      const { data, error } = await supabase
        .from('bookings')
        .insert([
          {
            scooter_id: id,
            user_id: user.id,
            start_date: startDate,
            end_date: endDate,
            status: 'pending',
            total_amount: calculateTotalAmount(),
          },
        ])
        .select()
        .single();

      if (error) throw error;

      navigate(`/bookings`);
    } catch (error: any) {
      setError(error.message);
    }
  };

  const calculateTotalAmount = () => {
    if (!scooter || !startDate || !endDate) return 0;

    const start = new Date(startDate);
    const end = new Date(endDate);
    const hours = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);
    const remainingHours = hours % 24;

    return days * scooter.daily_rate + remainingHours * scooter.hourly_rate;
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!scooter) {
    return <div>Scooter not found</div>;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <img
          src={scooter.image_url}
          alt={scooter.name}
          className="w-full h-64 object-cover"
        />
        <div className="p-6">
          <h1 className="text-3xl font-bold mb-4">{scooter.name}</h1>
          <p className="text-gray-600 mb-4">{scooter.description}</p>
          
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <h3 className="font-semibold">Model</h3>
              <p>{scooter.model}</p>
            </div>
            <div>
              <h3 className="font-semibold">Rates</h3>
              <p>${scooter.hourly_rate}/hour</p>
              <p>${scooter.daily_rate}/day</p>
            </div>
          </div>

          {error && (
            <div className="bg-red-100 text-red-700 p-4 rounded-md mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleBooking} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Start Date and Time
              </label>
              <input
                type="datetime-local"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                min={format(new Date(), "yyyy-MM-dd'T'HH:mm")}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                End Date and Time
              </label>
              <input
                type="datetime-local"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                min={startDate}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>

            {startDate && endDate && (
              <div className="bg-gray-50 p-4 rounded-md">
                <h3 className="font-semibold">Total Amount</h3>
                <p className="text-2xl">${calculateTotalAmount()}</p>
              </div>
            )}

            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Book Now
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}