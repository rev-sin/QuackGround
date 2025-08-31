import { create } from 'zustand';

export const useWeb3Store = create((set) => ({
  account: null,
  setAccount: (account) => set({ account }),
}));