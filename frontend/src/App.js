import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useState } from 'react';

function App() {
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [leaderboard, setLeaderboard] = useState([]);
  const [amount, setAmount] = useState('');

  // Function to handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:7000/api/transactions', {
        user_name: name,
        message,
        amount: parseFloat(amount)
      });
      console.log('Transaction successful:', response.data);
      fetchLeaderboard(); // Update the leaderboard
    } catch (error) {
      console.error('Error making transaction:', error);
    }
  };

  // Function to fetch the leaderboard from the API
  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:7000/api/leaderboard');
      setLeaderboard(response.data['leaderboard']);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    }
  };

  // Effect to load the leaderboard when the component mounts
  useEffect(() => {
    fetchLeaderboard();
  }, []);

  return (
    <div className="container">
      <h1 className="text-center my-4">Pay2Win</h1>
      <form onSubmit={handleSubmit} className="p-3 mb-4 bg-white rounded shadow-sm">
        <div className="mb-3">
          <label htmlFor="name" className="form-label">Your Name</label>
          <input
            type="text"
            id="name"
            className="form-control"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="message" className="form-label">Optional Message</label>
          <input
            type="text"
            id="message"
            className="form-control"
            placeholder="Enter a message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="amount" className="form-label">Amount</label>
          <input
            type="number"
            id="amount"
            className="form-control"
            placeholder="Enter amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100">Pay and Play</button>
      </form>

      <h2 className="text-center">Leaderboard</h2>
      <ul className="list-group">
        {leaderboard.map((entry, index) => (
          <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
            {entry.name}
            <span>${entry.amount}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
