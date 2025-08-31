'use client';

import { connectWallet, signMessage } from '../utils/web3';
import { useWeb3Store } from '../store/web3Store';
import { useState } from 'react';

const WalletLogin = () => {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { account, setAccount } = useWeb3Store();

  const handleLogin = async () => {
    setLoading(true);
    setError('');
    try {
      const { signer, account } = await connectWallet();
      const message = 'Authenticate with Web3';
      const signature = await signMessage(signer, message);
      console.log('Signature:', signature); // For backend validation
      setAccount(account.address);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDisconnect = () => {
    setAccount(null);
    setError('');
  };

  return (
    <div>
      {account ? (
        <div>
          <p>Connected as: {account}</p>
          <button onClick={handleDisconnect} disabled={loading}>
            Disconnect Wallet
          </button>
        </div>
      ) : (
        <button onClick={handleLogin} disabled={loading}>
          {loading ? 'Connecting...' : 'Connect Wallet'}
        </button>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default WalletLogin;