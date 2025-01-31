import React, { useState } from "react";
import { useSelector } from "react-redux";
import { lShear, uShear, window_close } from "../../../assets/assets";

const WebCapacity = () => {
  const [isWebCapacityOpen, setIsWebCapacityOpen] = useState(false);

  const isDesignActive = useSelector(
    (state) => state.preference.isDesignActive
  );

  const webCapacityDetails = [
    { label: "Web Tension Capacity (kN)", value: "1343.99" },
    { label: "Web Plate Tension Capacity (kN)", value: "2054.59" },
    { label: "Web Plate Shear Capacity (kN)", value: "888.07" },
    { label: "Web Moment Demand (kNm)", value: "110.56" },
  ];

  return (
    <>
      <div className="output-set">
        <label className="output-label">Capacity (mm)</label>
        <button
          className={`${
            !isDesignActive ? "outputInactive-button" : "output-button grade"
          }`}
          onClick={() => setIsWebCapacityOpen((prev) => !prev)}
        >
          Web Capacity
        </button>

        {isWebCapacityOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-75 z-[1000] transition-opacity">
            <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[80%] md:w-[40%] lg:w-[50%] h-[50%] bg-white rounded-lg shadow-lg">
              <div className="p-4 flex flex-col h-full">
                {/* Header */}
                <div className="flex justify-between items-center mb-4 border-b pb-2">
                  <h4 className="text-xl font-thin">Web Capacity</h4>
                  <button onClick={() => setIsWebCapacityOpen(false)}>
                    <img
                      src={window_close}
                      alt="Close"
                      className="w-5 cursor-pointer"
                    />
                  </button>
                </div>

                <div className="mb-10">
                  <p className="text-lg">
                    Note: Representative image for Failure Pattern (Half Pattern) - 2
                    x 3 pattern considered
                  </p>
                </div>

                {/* Details Section */}
                <div className="flex flex-col justify-between overflow-y-auto border border-gray-500 h-full p-4 custom-scrollbar">
                  <div className="flex justify-between h-full p-4 mb-12">
                    <div className="flex flex-col">
                      <p className="font-bold text-lg mb-4">
                        Failure Pattern due to Tension in Plate and Member
                      </p>
                      {webCapacityDetails.slice(0, 2).map((detail, index) => (
                        <div
                          key={index}
                          className="flex justify-between items-center p-2 mt-3 mb-3"
                        >
                          <span className="text-base font-medium">
                            {detail.label}:
                          </span>
                          <input
                            type="text"
                            value={detail.value}
                            readOnly
                            className="text-left text-base border border-blue-400 focus:outline-none rounded p-1 w-1/3"
                          />
                        </div>
                      ))}
                    </div>
                    <div className="flex flex-col w-1/2">
                      <img src={uShear} alt="" className="w-full object-fill" />
                      <p className="text-center text-lg pt-2">Block Shear Pattern</p>
                    </div>
                  </div>

                  <hr className="border border-black mt-4" />

                  <div className="flex justify-between h-full p-4">
                    <div className="flex flex-col">
                      <p className="font-bold text-lg mb-4">
                        Failure Pattern due to Shear in Plate and Member
                      </p>
                      {webCapacityDetails.slice(2, 4).map((detail, index) => (
                        <div
                          key={index}
                          className="flex justify-between items-center p-2 mt-3 mb-3"
                        >
                          <span className="text-base font-medium">
                            {detail.label}:
                          </span>
                          <input
                            type="text"
                            value={detail.value}
                            readOnly
                            className="text-left text-base border border-blue-400 focus:outline-none rounded p-1 w-1/3"
                          />
                        </div>
                      ))}
                    </div>
                    <div className="flex flex-col w-1/2">
                      <img src={lShear} alt="" className="w-full object-fill" />
                      <p className="text-center text-lg pt-2">Block Shear Pattern</p>
                    </div>
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

export default WebCapacity;
