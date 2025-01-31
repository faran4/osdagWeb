import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchBoltDiameters,
  setAvailableDiameters,
  setSelectedDiameters,
  setSelectValue,
} from "../../../redux/features/boltDiameterSlice";
import CustomisedPopup from "../../customised/customisedPopUp";

const BoltDiameter = () => {
  // Fetch data from Redux store
  const {
    data: boltDiameters,
    loading,
    error,
    selectedDiameters,
    availableDiameters,
    selectValue,
  } = useSelector((state) => state.boltDiameters);

  const [isCustomisedOpen, setIsCustomisedOpen] = useState(false);
  const dispatch = useDispatch();

  // Fetch bolt diameters on component mount
  useEffect(() => {
    dispatch(fetchBoltDiameters());
  }, [dispatch]);

  // Handle updates to 'available' array
  const handleAvailableChange = (updatedAvailable) => {
    dispatch(setAvailableDiameters(updatedAvailable));
    console.log("Updated Available Array:", updatedAvailable);
  };

  // Handle updates to 'selected' array
  const handleSelectedChange = (updatedSelected) => {
    dispatch(setSelectedDiameters(updatedSelected));
    console.log("Updated Selected Array:", updatedSelected);
  };

  // Handle selection change
  const handleSelectChange = (event) => {
    dispatch(setSelectValue(event.target.value));

    if (event.target.value === "Customized") {
      setIsCustomisedOpen(true);
    }
  };

  // Handle submission of customised popup
  const handleCustomisedSubmit = (value) => {
    console.log("Updated selectValue:", value);
    dispatch(setSelectedDiameters(value));
    setIsCustomisedOpen(false); // Close the popup
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error loading bolt diameters</p>;

  return (
    <>
      <label className="form-label">
        Diameter (mm)
        <select className="form-input" value={selectValue} onChange={handleSelectChange}>
          <option>All</option>
          <option>Customized</option>
        </select>
      </label>

      {/* Customised Popup */}
      {isCustomisedOpen && (
        <CustomisedPopup
          isOpen={isCustomisedOpen}
          onClose={() => setIsCustomisedOpen(false)}
          onSubmit={handleCustomisedSubmit}
          onChangeAvailable={handleAvailableChange}
          onChangeSelected={handleSelectedChange}
          availableProp={availableDiameters}
          selectedProp={selectedDiameters}
        />
      )}
    </>
  );
};

export default BoltDiameter;
