import React, { useEffect, useState } from "react";
import { parallelBeam, slopeBeam } from "../../assets/assets";
import { fetchBeams, setSelectedBeam, setTypeBeam } from "../../redux/features/beamSlice";
import { useDispatch, useSelector } from "react-redux";
import { setSelectedBeamGrade } from "../../redux/features/materialSlice";

const BeamSection = () => {
  // Access the state from Redux store
  const {
    data: beams,
    loading,
    error,
    selectedBeam,
    beamProperties,
    modulusOfElasticity,
    modulusOfRigidity,
    poissonsRatio,
    thermalExpansionCoefficient,
    typeBeam
  } = useSelector((state) => state.beams);

  const {
    data: materials,
    selectedBeamGrade,
    loading1,
    error1,
    ultimateStrengthMaterial,
    yieldStrength20mmMaterial,
  } = useSelector((state) => state.materials);

  const [selectImage, setSelectImage] = useState(slopeBeam);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchBeams());
  }, [dispatch]);

  useEffect(() => {
    const firstWord = selectedBeam?.split(" ")[0] || ""; 
    if (firstWord.length === 2) {
      setSelectImage(slopeBeam);
    } else if (firstWord.length === 3) {
      setSelectImage(parallelBeam);
    }
  }, [selectedBeam]);

  const handleBeamGradeChange = (e) => {
    dispatch(setSelectedBeamGrade(e.target.value));
  };

  return (
    <div className="mx-3 h-[84%] border border-gray-400 overflow-hidden cursor-default">
      <div className="m-2 p-3 border border-gray-400 h-[90%] overflow-y-auto custom-scrollbar">
        <div className="w-full h-max-full gap-4">
          <div className="w-full flex h-auto gap-4">
            {/* Left Section */}
            <div className="w-2/3 flex gap-12">
              {/* Mechanical Properties */}
              <div className="w-full flex flex-col">
                <div className="flex items-center justify-between mb-2">
                  <label className="text-md">Designation</label>
                  <input
                    type="text"
                    readOnly
                    value={selectedBeam || ""}
                    className="w-[30%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                  />
                </div>
                <h2 className="text-lg font-semibold mb-3">
                  Mechanical Properties
                </h2>
                <div className="flex flex-col">
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Material *</label>
                    <select
                      className="w-[33%] text-md border border-gray-500 rounded px-1 py-0.5"
                      value={selectedBeamGrade} // Bind the selected grade from Redux store
                      onChange={handleBeamGradeChange}
                      required
                    >
                      {materials.map((material, index) => (
                        <option key={index} value={material.Grade}>
                          {material.Grade}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      Ultimate Strength, Fu (MPa)
                    </label>
                    <input
                      readOnly
                      type="number"
                      value={ultimateStrengthMaterial}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Yield Strength, Fy (MPa)</label>
                    <input
                      readOnly
                      type="number"
                      value={yieldStrength20mmMaterial}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      Modulus of Elasticity, E (GPa)
                    </label>
                    <input
                      readOnly
                      type="number"
                      defaultValue={modulusOfElasticity}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      Modulus of Rigidity, G (GPa)
                    </label>
                    <input
                      readOnly
                      type="number"
                      defaultValue={modulusOfRigidity}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Poisson's Ratio, v</label>
                    <input
                      readOnly
                      type="number"
                      defaultValue={poissonsRatio}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      Thermal Expansion Coefficient
                    </label>
                    <input
                      readOnly
                      type="number"
                      defaultValue={thermalExpansionCoefficient}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Type</label>
                    <select className="w-[33%] text-md border border-gray-500 rounded px-1 py-0.5"
                    value={typeBeam}
                    onChange={(e) => dispatch(setTypeBeam(e.target.value))}                  
                    >
                      <option>Rolled</option>
                      <option>Welded</option>
                    </select>
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Source</label>
                    <input
                      type="text"
                      readOnly
                      value={beamProperties.source || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                </div>
              </div>

              {/* Dimensions */}
              <div className="flex flex-col w-full">
                <h2 className="text-lg font-semibold mb-4">Dimensions</h2>
                <div className="flex flex-col">
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Depth, D (mm)*</label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.D || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Flange Width, B (mm)*</label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.B || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Flange Thickness, T (mm)*</label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.T || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Web Thickness, t (mm)*</label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.tw || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Flange Slope, a (deg.)*</label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.FlangeSlope || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Root Radius, R1 (mm)*</label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.R1 || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Toe Radius, R2 (mm)*</label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.R2 || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                </div>

                {/* Section Properties */}
                <div className="flex flex-col">
                  <h2 className="text-lg font-semibold mb-4">
                    Section Properties
                  </h2>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">Mass, M (kg/m)</label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.Mass || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      Sectional Area, a (cm<sup>2</sup>)
                    </label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.Area || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      2nd Moment of Area, I<sub>z</sub> (cm<sup>4</sup>)
                    </label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.Iz || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      2nd Moment of Area, I<sub>v</sub> (cm<sup>4</sup>)
                    </label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.Iy || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      Radius of Gyration, r<sub>z</sub> (cm)
                    </label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.rz || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      Radius of Gyration, r<sub>v</sub> (cm)
                    </label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.ry || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      Elastic Modulus, Z<sub>z</sub> (cm<sup>3</sup>)
                    </label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.Zz || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-md">
                      Elastic Modulus, Z<sub>y</sub> (cm<sup>3</sup>)
                    </label>
                    <input
                      type="number"
                      readOnly
                      value={beamProperties.Zy || ""}
                      className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Right Section */}
            <div className="w-1/3 ml-10">
              <div className="w-full h-auto flex flex-col items-center mb-4">
                <img
                  src={selectImage}
                  alt=""
                  className="w-[80%] object-contain border border-black"
                />
              </div>
              <h2 className="text-lg font-semibold mb-4">Section Properties</h2>
              <div className="flex items-center justify-between mb-2">
                <label className="text-md">
                  Plastic Modulus, Z<sub>pz</sub> (cm<sup>3</sup>)
                </label>
                <input
                  type="number"
                  readOnly
                  value={beamProperties.Zpz || ""}
                  className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                />
              </div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-md">
                  Plastic Modulus, Z<sub>pv</sub> (cm<sup>3</sup>)
                </label>
                <input
                  type="number"
                  readOnly
                  value={beamProperties.Zpy || ""}
                  className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                />
              </div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-md">
                  Torsion Constant, I<sub>t</sub> (cm<sup>4</sup>)
                </label>
                <input
                  type="number"
                  readOnly
                  value={beamProperties.It || ""}
                  className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                />
              </div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-md">
                  Warping Constant, I<sub>w</sub> (cm<sup>6</sup>)
                </label>
                <input
                  type="number"
                  readOnly
                  value={beamProperties.Iw || ""}
                  className="w-[33%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Footer Buttons */}
      <div className="w-full cursor-default flex justify-around items-center p-2">
        <button className="w-[14%] greenGrade font-thin px-3 py-1 bg-gray-300 border border-yellow-200 rounded-md">
          Add
        </button>
        <button className="w-[14%] greenGrade font-thin px-3 py-1 bg-gray-300 border border-yellow-200 rounded-md">
          Clear
        </button>
        <button className="w-[14%] greenGrade font-thin px-3 py-1 bg-gray-300 border border-yellow-200 rounded-md">
          Import xlsx file
        </button>
        <button className="w-[14%] greenGrade font-thin px-3 py-1 bg-gray-300 border border-yellow-200 rounded-md">
          Download xlsx file
        </button>
      </div>
    </div>
  );
};

export default BeamSection;
