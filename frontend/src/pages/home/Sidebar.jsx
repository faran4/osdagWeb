import React, { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Modules } from "../../assets/assets";

const Sidebar = () => {
  const location = useLocation();
  const [activeIndex, setActiveIndex] = useState(null);

  // Set the activeIndex based on the saved state in localStorage or URL
  useEffect(() => {
    const currentPath = location.pathname;

    if (currentPath === "/") {
      // If on the homepage, no button should be active
      setActiveIndex(null);
      localStorage.removeItem("activeIndex"); // Clear activeIndex from localStorage
    } else {
      const savedIndex = localStorage.getItem("activeIndex");
      if (savedIndex) {
        setActiveIndex(parseInt(savedIndex, 10));
      } else {
        // Handle active state based on the current path
        const moduleIndex = Modules.findIndex(
          (module) =>
            `/${module.toLowerCase().replace(/ /g, "-")}` === currentPath
        );
        setActiveIndex(moduleIndex);
      }
    }
  }, [location]);

  const handleClick = (index) => {
    setActiveIndex(index);
    localStorage.setItem("activeIndex", index); // Save active index to localStorage
  };

  return (
    <>
      <div className="sidebar h-[93vh] px-12 py-10">
        {Modules.map((module, index) => (
          <Link
            key={index}
            to={`/${module.toLowerCase().replace(/ /g, "-")}`}
            className="block"
          >
            <button
              className={`sidebar-button w-full my-6 px-4 rounded ${
                activeIndex === index ? "active" : ""
              }`}
              onClick={() => handleClick(index)}
            >
              {module}
            </button>
          </Link>
        ))}
      </div>
      <div className="w-full flex items-center space-x-2 h-[4vh] my-1">
        <select className="w-[70%] p-1 rounded bg-white text-black border border-gray-400">
          <option>Help</option>
          <option>Video Tutorials</option>
          <option>Ask Us a Question</option>
          <option>Check for Update</option>
          <option>About Osdag</option>
        </select>
        <div className="dark-mode-toggle">
          Dark Mode
          <label className="switch">
            <input type="checkbox" />
            <span className="slider"></span>
          </label>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
