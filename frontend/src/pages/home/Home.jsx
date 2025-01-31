import React from "react";
import Sidebar from "./Sidebar";
import Startpage from "./Startpage";
import { Outlet } from "react-router-dom";

const Home = () => {
  return (
    <div className="w-screen h-screen flex p-3 bg-gray-100">
      <div className="w-1/5 mr-3">
        <Sidebar />
      </div>
      <div className="w-4/5">
        <Outlet />
      </div>
    </div>
  );
};

export default Home;
