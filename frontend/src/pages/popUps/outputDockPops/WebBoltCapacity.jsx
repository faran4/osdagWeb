import React, { useState } from "react";
import { useSelector } from "react-redux";
import { window_close } from "../../../assets/assets";

const WebBoltCapacity = () => {
  const [isWebBoltCapacityOpen, setIsWebBoltCapacityOpen] = useState(false);

  const isDesignActive = useSelector(
    (state) => state.preference.isDesignActive
  );

  const webBoltDetails = [
    { label: "Bolt Lines", value: "6" },
    { label: "Bolts in One Line", value: "9" },
    { label: "Bolts Required", value: "54" },
    { label: "Shear Capacity (kN)", value: "67.09" },
    { label: "Bearing Capacity (kN)", value: "N/a" },
    { label: "Red. Factor", value: "0.96" },
    { label: "Capacity (kN)", value: "64.41" },
    { label: "Bolt Force (kN)", value: "63.28" },
  ];

  return (
    <>
      <div className="output-set">
        <label className="output-label">Web Bolt Capacity</label>
        <button
          className={`${
            !isDesignActive ? "outputInactive-button" : "output-button grade"
          }`}
          onClick={() => setIsWebBoltCapacityOpen((prev) => !prev)}
        >
          Web Bolt Capacity
        </button>

        {isWebBoltCapacityOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-75 z-[1000] transition-opacity opacity-100">
            <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[80%] md:w-[40%] lg:w-[25%] h-[40%] bg-white rounded-lg shadow-lg">
              <div className="p-4 flex flex-col h-full">
                {/* Header */}
                <div className="flex justify-between items-center mb-4 border-b pb-2">
                  <h4 className="text-xl font-thin">Web Bolt Capacity</h4>
                  <button onClick={() => setIsWebBoltCapacityOpen((prev) => !prev)}>
                    <img
                      src={window_close}
                      alt="Close"
                      className="w-5 cursor-pointer"
                    />
                  </button>
                </div>

                {/* Details Section */}
                <div className="flex flex-col overflow-y-auto h-full border border-gray-500 p-6 custom-scrollbar">
                  {webBoltDetails.map((detail, index) => (
                    <div
                      key={index}
                      className="flex justify-between items-center p-2"
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
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default WebBoltCapacity;
