import React, { useState } from "react";
import { useSelector } from "react-redux";
import { blockShear, window_close } from "../../../assets/assets";

const FlangeCapacityDetails = () => {
  const [isFlangeCapacityOpen, setIsFlangeCapacityOpen] = useState(false);

  const isDesignActive = useSelector(
    (state) => state.preference.isDesignActive
  );

  const flangeCapacityDetails = [
    { label: "Flange Tension Capacity (kN)", value: "930.11" },
    { label: "Flange Plate Tension Capacity (kN)", value: "1145.45" },
  ];

  return (
    <>
      <div className="output-set">
        <label className="output-label">Capacity (mm)</label>
        <button
          className={`mb-2 ${
            !isDesignActive
              ? "outputInactive-button"
              : "output-button grade"
          }`}
          onClick={() => setIsFlangeCapacityOpen((prev) => !prev)}
        >
          Flange Capacity
        </button>

        {isFlangeCapacityOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-75 z-[1000] transition-opacity">
            <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[80%] md:w-[40%] lg:w-[50%] h-[45%] bg-white rounded-lg shadow-lg">
              <div className="p-4 flex flex-col h-full">
                {/* Modal Header */}
                <div className="flex justify-between items-center mb-4 border-b pb-2">
                  <h4 className="text-xl font-thin">Flange Capacity</h4>
                  <button onClick={() => setIsFlangeCapacityOpen(false)}>
                    <img
                      src={window_close}
                      alt="Close"
                      className="w-5 cursor-pointer"
                    />
                  </button>
                </div>

                {/* Modal Content */}
                <div className="mb-10">
                  <p className="text-lg">
                    Note: Representative image for Failure Pattern (Half Pattern) - 2 x 3 pattern
                    considered
                  </p>
                </div>

                <div className="flex justify-between overflow-y-auto border border-gray-500 h-full p-4 custom-scrollbar">
                  {/* Details Section */}
                  <div className="flex flex-col overflow-y-auto">
                    <p className="font-bold text-lg mb-8">
                      Failure Pattern due to Tension in Plate and Member
                    </p>
                    {flangeCapacityDetails.map((detail, index) => (
                      <div
                        key={index}
                        className="flex justify-between items-center p-2 mt-3 mb-3"
                      >
                        <span className="text-base font-medium">{detail.label}:</span>
                        <input
                          type="text"
                          value={detail.value}
                          readOnly
                          className="text-left text-base border border-blue-400 focus:outline-none rounded p-1 w-1/3"
                        />
                      </div>
                    ))}
                  </div>

                  {/* Image Section */}
                  <div className="flex flex-col w-1/2">
                    <img src={blockShear} alt="" className="w-full object-fill" />
                    <p className="text-center text-lg pt-2">Block Shear Pattern</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default FlangeCapacityDetails;
