import React from 'react'
import Home from './components/Home'
import Hom1 from './components/Hom1'
import Nav from './components/Nav'
import WalletLogin from './components/WalletLogin';

const page = () => {
  return (
    <div>
      <Nav/>
      <h1>Web3 Authentication in Next.js</h1>
      <WalletLogin />
      <Hom1/>
      <Home/>
    </div>
  )
}

export default page
