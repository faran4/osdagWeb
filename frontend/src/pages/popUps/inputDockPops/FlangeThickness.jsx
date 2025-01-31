import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  setAvailableFlangeThickness,
  setSelectedFlangeThickness,
  setSelectFlangeThicknessValue,
} from "../../../redux/features/CommonInputSlice";
import CustomisedPopup from "../../customised/customisedPopUp";

const FlangeThickness = () => {
  const dispatch = useDispatch();

  // Redux state selectors
  const {
    flangeThicknessAvailable,
    flangeThicknessSelected,
    selectFlangeThicknessValue,
  } = useSelector((state) => state.commonInputs);

  // Local state for modal visibility
  const [isFlangeThicknessOpen, setIsFlangeThicknessOpen] = useState(false);

  // Callback function to handle updates to the 'available' array
  const handleAvailableChange = (updatedAvailable) => {
    dispatch(setAvailableFlangeThickness(updatedAvailable));
    console.log("Updated Available Array:", updatedAvailable);
  };

  // Callback function to handle updates to the 'selected' array
  const handleSelectedChange = (updatedSelected) => {
    dispatch(setSelectedFlangeThickness(updatedSelected));
    console.log("Updated Selected Array:", updatedSelected);
  };

  const handleSelectChange = (event) => {
    const value = event.target.value;
    dispatch(setSelectFlangeThicknessValue(value));

    if (value === "Customized") {
      setIsFlangeThicknessOpen(true);
    }
  };

  const handleCustomisedSubmit = (value) => {
    setIsFlangeThicknessOpen(false); // Close the popup
  };

  return (
    <>
      <label className="form-label">
        Thickness (mm)
        <select
          className="form-input"
          value={selectFlangeThicknessValue}
          onChange={handleSelectChange} // Handle selection change
        >
          <option>All</option>
          <option>Customized</option>
        </select>
      </label>

      {/* Customised PopUp */}
      {isFlangeThicknessOpen && (
        <CustomisedPopup
          isOpen={isFlangeThicknessOpen}
          onClose={() => setIsFlangeThicknessOpen(false)}
          onSubmit={handleCustomisedSubmit} // Handle popup submission
          onChangeAvailable={handleAvailableChange}
          onChangeSelected={handleSelectedChange}
          availableProp={flangeThicknessAvailable}
          selectedProp={flangeThicknessSelected}
        />
      )}
    </>
  );
};

export default FlangeThickness;
