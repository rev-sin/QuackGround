import React from "react";
import Hom1 from "./components/Hom1";
import Home from "./components/Home";
import Nav from "./components/Nav";

const page = () => {
  return (
    <div>
      <Nav />
      <Hom1 />
      <Home />
    </div>
  );
};

export default page;
