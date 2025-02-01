import React, { useState } from "react";
import { window_close } from "../../assets/assets";

const CustomisedPopup = ({
  isOpen,
  onClose,
  onSubmit,
  onChangeAvailable, // Callback to update the 'available' array in the parent
  onChangeSelected, // Callback to update the 'selected' array in the parent
  availableProp = [8, 10, 12, 14, 16], // Default props for 'available'
  selectedProp = [18, 20, 22, 24, 27, 30, 33, 36, 39, 42, 45, 48, 52, 56, 60, 64], // Default props for 'selected'
}) => {
  const [available, setAvailable] = useState(availableProp);
  const [selected, setSelected] = useState(selectedProp);
  const [selectedAvailable, setSelectedAvailable] = useState([]);
  const [selectedSelected, setSelectedSelected] = useState([]);

  const updateAvailable = (newAvailable) => {
    setAvailable(newAvailable);
    onChangeAvailable && onChangeAvailable(newAvailable); // Send updated 'available' to the parent
  };

  const updateSelected = (newSelected) => {
    setSelected(newSelected);
    onChangeSelected && onChangeSelected(newSelected); // Send updated 'selected' to the parent
  };

  const toggleSelection = (item, selectedList, setSelectedList) => {
    if (selectedList.includes(item)) {
      setSelectedList(selectedList.filter((val) => val !== item));
    } else {
      setSelectedList([...selectedList, item]);
    }
  };

  const shiftAllToRight = () => {
    updateSelected([...selected, ...available].sort((a, b) => a - b));
    updateAvailable([]);
    setSelectedAvailable([]);
  };

  const shiftToRight = () => {
    if (selectedAvailable.length > 0) {
      updateSelected([...selected, ...selectedAvailable].sort((a, b) => a - b));
      updateAvailable(
        available.filter((val) => !selectedAvailable.includes(val))
      );
      setSelectedAvailable([]);
    }
  };

  const shiftToLeft = () => {
    if (selectedSelected.length > 0) {
      updateAvailable([...available, ...selectedSelected].sort((a, b) => a - b));
      updateSelected(
        selected.filter((val) => !selectedSelected.includes(val))
      );
      setSelectedSelected([]);
    }
  };

  const shiftAllToLeft = () => {
    updateAvailable([...available, ...selected].sort((a, b) => a - b));
    updateSelected([]);
    setSelectedSelected([]);
  };

  const handleSubmit = () => {
    if (selected.length > 0) {
      onSubmit(selected); // Pass the first selected value to the parent
    } else {
      alert("No value selected!");
    }
  };

  return (
    <div
      className={`fixed inset-0 bg-black bg-opacity-50 z-[1000] flex justify-center items-center transition-opacity ${
        isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
      }`}
    >
      <div className="w-[90%] md:w-[60%] lg:w-[30%] h-[60%] bg-white rounded-lg shadow-lg">
        <div className="p-4 w-full h-full">
          <div className="flex justify-between items-center mb-4 border-b pb-2">
            <h3 className="text-lg font-thin">Customized</h3>
            <button type="button" onClick={onClose}>
              <img
                src={window_close}
                alt="Close"
                className="w-4 cursor-pointer"
              />
            </button>
          </div>
          <div className="w-full h-2/3 flex flex-col md:flex-row justify-around items-center gap-6">
            {/* Available List */}
            <div className="w-1/3 h-full">
              <h4 className="text-lg font-medium mb-2">Available:</h4>
              <ul className="border border-gray-300 rounded-lg p-2 h-full overflow-y-auto custom-scrollbar bg-gray-50">
                {available.map((item) => (
                  <li
                    key={item}
                    onClick={() =>
                      toggleSelection(item, selectedAvailable, setSelectedAvailable)
                    }
                    className={`p-2 mb-1 rounded cursor-pointer text-center ${
                      selectedAvailable.includes(item)
                        ? "bg-blue-400"
                        : "bg-white hover:bg-gray-100"
                    }`}
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            {/* Buttons */}
            <div className="flex flex-col gap-2">
              <button
                type="button"
                onClick={shiftAllToRight}
                className="report-button grade w-24"
              >
                {">>"}
              </button>
              <button
                type="button"
                onClick={shiftToRight}
                className="report-button grade w-24"
              >
                {">"}
              </button>
              <button
                type="button"
                onClick={shiftToLeft}
                className="report-button grade w-24"
              >
                {"<"}
              </button>
              <button
                type="button"
                onClick={shiftAllToLeft}
                className="report-button grade w-24"
              >
                {"<<"}
              </button>
            </div>

            {/* Selected List */}
            <div className="w-1/3 h-full">
              <h4 className="text-lg font-medium mb-2">Selected:</h4>
              <ul className="border border-gray-300 rounded-lg p-2 h-full overflow-y-auto custom-scrollbar bg-gray-50">
                {selected.map((item) => (
                  <li
                    key={item}
                    onClick={() =>
                      toggleSelection(item, selectedSelected, setSelectedSelected)
                    }
                    className={`p-2 mb-1 rounded cursor-pointer text-center ${
                      selectedSelected.includes(item)
                        ? "bg-blue-400"
                        : "bg-white hover:bg-gray-100"
                    }`}
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="mt-16 text-center">
            <button
              type="button"
              onClick={handleSubmit}
              className="report-button grade w-40"
            >
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomisedPopup;
