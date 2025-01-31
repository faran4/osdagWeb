import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchMaterials, setSelectedGrade, setSelectedConnector, setSelectedBeamGrade } from "../../../redux/features/materialSlice";

const Materials = () => {
  const { data: materials, loading, error, selectedGrade } = useSelector(
    (state) => state.materials
  );
  const dispatch = useDispatch();

  // Fetch materials when the component mounts
  useEffect(() => {
    dispatch(fetchMaterials());
  }, [dispatch]);

  // Set the default selected grade to the second material's grade when materials are available
  useEffect(() => {
    if (materials && materials.length > 1 && !selectedGrade) {
      dispatch(setSelectedGrade(materials[1].Grade)); // Set to second object's grade
      dispatch(setSelectedConnector(materials[1].Grade)); // Set to second object's grade
      dispatch(setSelectedBeamGrade(materials[1].Grade)); // Set to second object's grade
    }
  }, [materials, selectedGrade, dispatch]);

  const handleGradeChange = (e) => {
    dispatch(setSelectedGrade(e.target.value)); // Dispatch selected grade to the Redux store
    dispatch(setSelectedConnector(e.target.value)); // Reset the selected connector
    dispatch(setSelectedBeamGrade(e.target.value)); // Reset the selected
  };

  if (loading) return <p>Loading materials...</p>;
  if (error) return <p>Error loading materials.</p>;

  return (
    <select
      className="form-input form-input-dropdown"
      value={selectedGrade} // Bind the selected grade from Redux store
      onChange={handleGradeChange}
      required
    >
      {materials.map((material, index) => (
        <option key={index} value={material.Grade}>
          {material.Grade}
        </option>
      ))}
    </select>
  );
};

export default Materials;
