import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  setAvailablePropertyClasses,
  setSelectedPropertyClasses,
  setSelectPropertyValue,
} from "../../../redux/features/CommonInputSlice"; // Adjust the path as needed
import CustomisedPopup from "../../customised/customisedPopUp";

const BoltPropertyClass = () => {
  // Access state from Redux
  const {
    propertyClassAvailable,
    propertyClassSelected,
    selectPropertyValue,
  } = useSelector((state) => state.commonInputs);
  const dispatch = useDispatch();

  // Toggle state for customized popup
  const [isPropertyClassOpen, setIsPropertyClassOpen] = useState(false);

  // Handle the available array updates
  const handleAvailableChange = (updatedAvailable) => {
    dispatch(setAvailablePropertyClasses(updatedAvailable));
    console.log("Updated Available Array:", updatedAvailable);
  };

  // Handle the selected array updates
  const handleSelectedChange = (updatedSelected) => {
    dispatch(setSelectedPropertyClasses(updatedSelected));
    console.log("Updated Selected Array:", updatedSelected);
  };

  // Handle dropdown change (e.g., All or Customized)
  const handleSelectChange = (event) => {
    const value = event.target.value;
    dispatch(setSelectPropertyValue(value));

    if (value === "Customized") {
      setIsPropertyClassOpen((prev) => !prev);
    }
  };

  // Handle form submission from the customized popup
  const handleCustomisedSubmit = (value) => {
    setIsPropertyClassOpen(false); // Close the popup
    console.log("Property Class Value:", value);
  };

  return (
    <>
      <label className="form-label">
        Property Class
        <select
          className="form-input"
          value={selectPropertyValue} // Use the value from the Redux store for the dropdown
          onChange={handleSelectChange}
        >
          <option>All</option>
          <option>Customized</option>
        </select>
      </label>

      {/* Customised PopUp */}
      {isPropertyClassOpen && (
        <CustomisedPopup
          isOpen={isPropertyClassOpen}
          onClose={() => setIsPropertyClassOpen((prev) => !prev)}
          onSubmit={handleCustomisedSubmit}
          onChangeAvailable={handleAvailableChange}
          onChangeSelected={handleSelectedChange}
          availableProp={propertyClassAvailable}
          selectedProp={propertyClassSelected}
        />
      )}
    </>
  );
};

export default BoltPropertyClass;
