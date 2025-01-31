import React, { useState } from "react";
import { window_close } from "../../assets/assets";
import Detailing from "./Detailing";
import Design from "./Design";
import Connector from "./Connector";
import BeamSection from "./BeamSection";
import { useDispatch, useSelector } from "react-redux";
import {
  resetInputs,
  setHoleType,
  setSlipFactor,
  setType,
} from "../../redux/features/defaultSlice";

const BoltDesign = ({ onClose, isOpen }) => {
  const [activeTab, setActiveTab] = useState("bolt");
  const { holeType, slipFactor, type } = useSelector((state) => state.default);
  const dispatch = useDispatch();

  return (
    <div
      className={`popup-overlay ${
        isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
      }`}
    >
      <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-[55%] w-[70%] h-[85vh] bg-white rounded-lg shadow-lg">
        <div className="bg-white w-full h-full shadow-lg rounded-md">
          {/* Header */}
          <div className="flex justify-between items-center p-2 bg-gray-100 border-b mb-6">
            <h2 className="text-xl font-thin">Design Preference</h2>
            <button onClick={onClose}>
              <img
                src={window_close}
                alt="Close"
                className="w-4 mr-2 cursor-pointer"
              />
            </button>
          </div>

          {/* Tabs */}
          <div className="flex mx-3">
            {["Beam Section *", "Connector", "Bolt", "Detailing", "Design"].map(
              (tab) => (
                <button
                  key={tab}
                  className={`w-[10%] greenGrade cursor-default relative font-thin px-3 py-1 bg-gray-300 border border-yellow-200 rounded-sm ${
                    activeTab === tab.toLowerCase()
                      ? "border-none -translate-y-1"
                      : ""
                  }`}
                  onClick={() => setActiveTab(tab.toLowerCase())}
                >
                  {tab}
                  {/* Bottom Highlight */}
                  {activeTab === tab.toLowerCase() && (
                    <div className="absolute bottom-0 left-0 w-full h-[10%] bg-red-300 rounded-b-sm"></div>
                  )}
                </button>
              )
            )}
          </div>

          {/* Content */}

          {activeTab === "beam section *" ? (
            <BeamSection />
          ) : (
            <div className="mx-3 h-[84%] border border-gray-400">
              <div className="m-2 p-3 border border-gray-400 h-auto">
                {activeTab === "connector" && <Connector />}
                {activeTab === "bolt" && (
                  <div className="flex flex-col gap-4 h-max-full">
                    {/* Inputs */}
                    <div className="flex justify-between w-full gap-10">
                      <div className="flex flex-col w-1/4">
                        <p className="font-semibold text-lg mb-1">Inputs</p>
                        <div className="flex items-center justify-between mb-2">
                          <label className="text-md">Type *</label>
                          <select
                            value={type}
                            onChange={(e) => dispatch(setType(e.target.value))}
                            className="w-[45%] overflow-hidden text-md border border-gray-400 rounded px-1 py-0.5"
                          >
                            <option>Non pre-tension</option>
                            <option>Pre-tension</option>
                          </select>
                        </div>
                        <div className="flex items-center justify-between mb-2">
                          <label className="text-md">Hole Type</label>
                          <select
                            value={holeType}
                            onChange={(e) =>
                              dispatch(setHoleType(e.target.value))
                            }
                            className="w-[45%] overflow-hidden text-md border border-gray-400 rounded px-1 py-0.5"
                          >
                            <option>Standard</option>
                            <option>OverSized</option>
                          </select>
                        </div>
                        <p className="font-semibold text-lg mb-1">HSFG Bolt:</p>
                        <div className="flex items-center justify-between mb-2">
                          <label className="text-md">Slip Factor, (mμ)</label>
                          <select
                            type="number"
                            value={slipFactor}
                            onChange={(e) =>
                              dispatch(setSlipFactor(e.target.value))
                            }
                            className="w-[45%] overflow-hidden text-md border border-gray-400 rounded px-1 py-0.5"
                          >
                            <option>0.2</option>
                            <option>0.5</option>
                            <option>0.1</option>
                            <option>0.25</option>
                            <option>0.3</option>
                            <option>0.33</option>
                            <option>0.48</option>
                            <option>0.52</option>
                            <option>0.55</option>
                          </select>
                        </div>
                      </div>

                      {/* Description */}
                      <div className="w-3/4">
                        <h3 className="text-lg mb-1">Description</h3>
                        <textarea
                          rows="30"
                          className="w-full border border-blue-400 leading-[1] text-base overflow-y-scroll custom-scrollbar focus:outline-none p-2"
                          readOnly
                          value={`IS 800 Table 20 Typical Average Values for Coefficient of Friction (µf)\n\n
    Treatment of Surfaces \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t µ_f\n             
i) \t\tSurfaces not treated \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t 0.2\n
ii)\t\tSurfaces blasted with short or grit with any loose rust removed, \t\t 0.5\n\t\tno pitting \n
iii)\tSurfaces blasted with short or grit and hot-dip galvanized \t\t\t\t 0.1\n
iv)\tSurfaces blasted with short or grit and spray - metallized with zinc \t 0.25\n\t\t(thickness 50-70 µm)\n
v)\t\tSurfaces blasted with shot or grit and painted with ethylzinc \t\t\t\t 0.3\n\t\tsilicate coat (thickness 30-60 µm)\n
vi)\tSand blasted surface, after light rusting \t\t\t\t\t\t\t\t\t\t\t\t 0.52\n
vii)\tSurfaces blasted with shot or grit and painted with ethylzinc\t\t\t\t 0.3\n\t\tsilicate coat (thickness 60-80 µm)\n
viii)\tSurfaces blasted with shot or grit and painted with alcalizinc\t\t\t\t 0.3\n\t\tsilicate coat (thickness 60-80 µm)\n
ix)\tSurfaces blasted with shot or grit and spray metallized with\t\t\t\t 0.5\n\t\taluminium (thickness >50 µm)\n
x)\t\tClean mill scale \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t 0.33\n
xi)\tSand blasted surface \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t 0.48\n
xii)\tRed lead painted surface \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t 0.1`}
                        />
                      </div>
                    </div>

                    {/* Note */}
                    <p className="mt-2 text-base font-bold border-t border-black pt-2">
                      NOTE: If slip is permitted under the design load, design
                      the bolt <br />
                      as a bearing bolt and select corresponding bolt grade.
                    </p>
                  </div>
                )}
                {activeTab === "detailing" && <Detailing />}
                {activeTab === "design" && <Design />}
              </div>
            </div>
          )}

          {/* Footer Buttons */}
          <div className="w-full cursor-default flex justify-around items-center p-4 bg-gray-100">
            <button
              onClick={() => dispatch(resetInputs())}
              className="w-[14%] greenGrade font-thin px-3 py-1 bg-gray-300 border border-yellow-200 rounded-md"
            >
              Defaults
            </button>
            <button className="w-[14%] greenGrade font-thin px-3 py-1 bg-gray-300 border border-yellow-200 rounded-md">
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BoltDesign;
