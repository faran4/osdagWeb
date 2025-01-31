import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  setAvailableWebThickness,
  setSelectedWebThickness,
  setSelectWebThicknessValue,
} from "../../../redux/features/CommonInputSlice";
import CustomisedPopup from "../../customised/customisedPopUp";

const WebSpliceThickness = () => {
  const dispatch = useDispatch();

  // Redux state
  const webThicknessAvailable = useSelector((state) => state.commonInputs.webThicknessAvailable);
  const webThicknessSelected = useSelector((state) => state.commonInputs.webThicknessSelected);
  const selectWebThicknessValue = useSelector((state) => state.commonInputs.selectWebThicknessValue);

  const [isWebThicknessOpen, setIsWebThicknessOpen] = useState(false);

  // Handle dropdown change
  const handleSelectChange = (event) => {
    const value = event.target.value;
    dispatch(setSelectWebThicknessValue(value));
    if (value === "Customized") {
      setIsWebThicknessOpen(true);
    }
  };

  // Handle popup submission
  const handleCustomisedSubmit = (value) => {
    setIsWebThicknessOpen(false);
  };

  // Handle updates to available and selected lists
  const handleAvailableChange = (updatedAvailable) => {
    dispatch(setAvailableWebThickness(updatedAvailable));
  };

  const handleSelectedChange = (updatedSelected) => {
    dispatch(setSelectedWebThickness(updatedSelected));
  };

  return (
    <>
      <label className="form-label">
        Thickness (mm) *
        <select className="form-input" value={selectWebThicknessValue} onChange={handleSelectChange} required>
          <option>All</option>
          <option>Customized</option>
        </select>
      </label>

      {/* Customised PopUp */}
      {isWebThicknessOpen && (
        <CustomisedPopup
          isOpen={isWebThicknessOpen}
          onClose={() => setIsWebThicknessOpen(false)}
          onSubmit={handleCustomisedSubmit}
          onChangeAvailable={handleAvailableChange}
          onChangeSelected={handleSelectedChange}
          availableProp={webThicknessAvailable}
          selectedProp={webThicknessSelected}
        />
      )}
    </>
  );
};

export default WebSpliceThickness;
