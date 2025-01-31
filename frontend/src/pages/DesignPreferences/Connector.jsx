import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { setSelectedConnector } from "../../redux/features/materialSlice";

const Connector = () => {
  const {
    data: materials,
    selectedConnector,
    ultimateStrength,
    yieldStrength20mm,
    yieldStrength40mm,
    yieldStrengthGreater40mm,
    loading,
    error,
  } = useSelector((state) => state.materials);
  const dispatch = useDispatch();

  const handleConnectorChange = (e) => {
    dispatch(setSelectedConnector(e.target.value));
  };

  if (loading) return <p>Loading materials...</p>;
  if (error) return <p>Error loading materials.</p>;

  return (
    <div className="flex flex-col gap-4 h-[66vh] mb-1">
      <div className="flex justify-between w-full gap-10">
        <div className="flex flex-col w-1/3">
          <p className="font-semibold text-lg mb-1">Inputs</p>

          {/* Material Selection Dropdown */}
          <div className="flex items-center justify-between mb-3">
            <label className="text-md">Material *</label>
            <select
              className="w-[33%] overflow-hidden text-md border border-gray-400 rounded px-1 py-0.5"
              value={selectedConnector} // Show the correct selection
              onChange={handleConnectorChange}
            >
              <option value="">Select Material</option>
              {materials.map((material, index) => (
                <option key={index} value={material.Grade}>
                  {material.Grade}
                </option>
              ))}
            </select>
          </div>

          {/* Material Properties Display */}
          <div className="flex items-center justify-between mb-2">
            <label className="text-md">Ultimate Strength, Fu (MPa)</label>
            <input
              type="text"
              value={ultimateStrength}
              readOnly
              className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
            />
          </div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-md">Yield Strength, Fy (MPa) (0-20mm)</label>
            <input
              type="text"
              value={yieldStrength20mm}
              readOnly
              className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
            />
          </div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-md">
              Yield Strength, Fy (MPa) (20-40mm)
            </label>
            <input
              type="text"
              value={yieldStrength40mm}
              readOnly
              className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
            />
          </div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-md">
              Yield Strength, Fy (MPa) {"( >40mm )"}
            </label>
            <input
              type="text"
              value={yieldStrengthGreater40mm}
              readOnly
              className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Connector;
