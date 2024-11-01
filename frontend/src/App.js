import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useState } from 'react';
import { FaExternalLinkAlt } from 'react-icons/fa'; // Import an external link icon

function App() {
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [amount, setAmount] = useState('');
  const [leaderboard, setLeaderboard] = useState([]);
  const [network, setNetwork] = useState('eth_mainnet');
  const [blockchainAddress, setBlockchainAddress] = useState('');
  const [transactionMessage, setTransactionMessage] = useState('');

  // Function to handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:7001/api/transactions', {
        user_name: name,
        message,
        amount: parseFloat(amount),
        blockchain_network: network
      });
      console.log('Transaction successful:', response.data);
      
      // Set the blockchain address and message
      setBlockchainAddress(response.data.blockchain_address);
      setTransactionMessage(`Send your crypto to the following address: ${response.data.blockchain_address}`);
      
      fetchLeaderboard(); // Update the leaderboard
    } catch (error) {
      console.error('Error making transaction:', error);
    }
  };

  // Function to fetch the leaderboard from the API
  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:7001/api/leaderboard');
      setLeaderboard(response.data);
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
        <div className="mb-3">
          <label htmlFor="network" className="form-label">Select Blockchain Network</label>
          <select
            id="network"
            className="form-select"
            value={network}
            onChange={(e) => setNetwork(e.target.value)}
            required
          >
            <option value="eth_mainnet">Ethereum Mainnet</option>
            <option value="eth_sepolia">Ethereum Sepolia</option>
            <option value="bitcoin_mainnet">Bitcoin Mainnet</option>
            <option value="bitcoin_testnet">Bitcoin Testnet</option>
            <option value="fiat">FIAT</option>
          </select>
        </div>
        <button type="submit" className="btn btn-primary w-100">Pay and Play</button>
      </form>

      {blockchainAddress && (
        <div className="alert alert-info">
          {transactionMessage}
        </div>
      )}

      <h2 className="text-center">Leaderboard</h2>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>User</th>
            <th>Message</th>
            <th>Amount</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((entry, index) => (
            <tr key={index}>
              <td>{entry.user_name}</td>
              <td>{entry.message}</td>
              <td>${entry.amount}</td>
              <td>
                <a href={`${entry.tracking_url}`} target="_blank" rel="noopener noreferrer">
                  <FaExternalLinkAlt />
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
