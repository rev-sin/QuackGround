import { ethers } from 'ethers';

export const connectWallet = async () => {
  try {
    if (!window.ethereum) {
      throw new Error('MetaMask is not installed');
    }

    const provider = new ethers.BrowserProvider(window.ethereum);
    await window.ethereum.request({ method: 'eth_requestAccounts' });
    const accounts = await provider.listAccounts();
    const signer = await provider.getSigner();

    if (accounts.length === 0) {
      throw new Error('No accounts found. Please connect a wallet.');
    }

    return { provider, signer, account: accounts[0] };
  } catch (error) {
    console.error('Error connecting wallet:', error.message);
    throw error;
  }
};

export const signMessage = async (signer, message) => {
  try {
    const signature = await signer.signMessage(message);
    return signature;
  } catch (error) {
    console.error('Error signing message:', error.message);
    throw error;
  }
};