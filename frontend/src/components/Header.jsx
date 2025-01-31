import React, { useState, useEffect, useRef } from "react";
import File from "../pages/inputsNavbar/File";
import Edit from "../pages/inputsNavbar/Edit";
import Graphics from "../pages/inputsNavbar/Graphics";
import Database from "../pages/inputsNavbar/Database";
import Help from "../pages/inputsNavbar/Help";
import BoltDesign from "../pages/DesignPreferences/BoltDesign";

function Header() {
  const [openDropdown, setOpenDropdown] = useState(null); // Tracks the open dropdown
  const [isPopupOpen, setIsPopupOpen] = useState(false); // Tracks the popup state
  const dropdownRef = useRef(null);

  // Handles opening the dropdown on click
  const handleClick = (dropdown) => {
    if (!isPopupOpen) {
      setOpenDropdown((prev) => (prev === dropdown ? null : dropdown));
    }
  };

  // Handles switching between dropdowns on hover
  const handleMouseEnter = (dropdown) => {
    if (openDropdown && !isPopupOpen) {
      setOpenDropdown(dropdown);
    }
  };

  // Closes the dropdown when clicking outside
  const handleClickOutside = (event) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target)
    ) {
      setOpenDropdown(null);
    }
  };

  // Opens the popup and closes the dropdown
  const handleOpenPopup = () => {
    setIsPopupOpen(true); // Open the popup
    setOpenDropdown(null); // Close the dropdown
  };

  // Closes the popup
  const handleClosePopup = () => {
    setIsPopupOpen(false);
  };

  // Adds a click listener for closing the dropdown
  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="w-full" ref={dropdownRef}>
      <header className="bg-gray-300 text-black flex justify-start gap-4 pl-3">
        <div className="relative flex">
          {/* File Tab */}
          <div
            className="cursor-default pr-2 pl-2 hover:bg-blue-500"
            onMouseEnter={() => handleMouseEnter("File")}
            onClick={() => handleClick("File")}
          >
            File
          </div>
          {openDropdown === "File" && <File />}

          {/* Edit Tab */}
          <div
            className="cursor-default pr-2 pl-2 hover:bg-blue-500"
            onMouseEnter={() => handleMouseEnter("Edit")}
            onClick={() => handleClick("Edit")}
          >
            Edit
          </div>
          {openDropdown === "Edit" && (
            <Edit onOpenPopup={handleOpenPopup} />
          )}

          {/* Graphics Tab */}
          <div
            className="cursor-default pr-2 pl-2 hover:bg-blue-500"
            onMouseEnter={() => handleMouseEnter("Graphics")}
            onClick={() => handleClick("Graphics")}
          >
            Graphics
          </div>
          {openDropdown === "Graphics" && <Graphics />}

          {/* Database Tab */}
          <div
            className="cursor-default pr-2 pl-2 hover:bg-blue-500"
            onMouseEnter={() => handleMouseEnter("Database")}
            onClick={() => handleClick("Database")}
          >
            Database
          </div>
          {openDropdown === "Database" && <Database />}

          {/* Help Tab */}
          <div
            className="cursor-default pr-2 pl-2 hover:bg-blue-500"
            onMouseEnter={() => handleMouseEnter("Help")}
            onClick={() => handleClick("Help")}
          >
            Help
          </div>
          {openDropdown === "Help" && <Help />}
        </div>
      </header>
      {/* Popup is rendered outside the dropdown */}
      {isPopupOpen && <BoltDesign isOpen={isPopupOpen} onClose={handleClosePopup} />}
    </div>
  );
}

export default Header;
