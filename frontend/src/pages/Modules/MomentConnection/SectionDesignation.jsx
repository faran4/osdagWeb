import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchBeams, setSelectedBeam } from "../../../redux/features/beamSlice";

const SectionDesignation = () => {
  const { data: beams, loading, error, selectedBeam } = useSelector(
    (state) => state.beams
  );
  const dispatch = useDispatch();
  // Fetch beams data when component mounts
  useEffect(() => {
    dispatch(fetchBeams());
  }, [dispatch]);

  // Handle change in beam selection
  const handleBeamChange = (e) => {
    const selectedDesignation = e.target.value;
    dispatch(setSelectedBeam(selectedDesignation)); // Dispatch the selected beam to Redux
  };

  // If data is still loading, show a loading message
  if (loading) return <p>Loading beams...</p>;
  // If there is an error, show an error message
  if (error) return <p>Error loading beams.</p>;

  return (
    <select
      className="form-input form-input-dropdown"
      value={selectedBeam} // Bind the selected beam from Redux store
      onChange={handleBeamChange}
      required
    >
      <option value="">Select Designation</option> {/* Default "Select Designation" option */}
      {beams.map((beam, index) => (
        <option key={index} value={beam.Designation} className="form-input-dropdown">
          {beam.Designation}
        </option>
      ))}
    </select>
  );
};

export default SectionDesignation;
