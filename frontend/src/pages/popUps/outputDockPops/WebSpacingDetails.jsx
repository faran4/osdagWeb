import React, { useState } from "react";
import { useSelector } from "react-redux";
import { spacingweb, window_close } from "../../../assets/assets";

const WebSpacingDetails = () => {
  const [isWebSpacingOpen, setIsWebSpacingOpen] = useState(false);

  const isDesignActive = useSelector(
    (state) => state.preference.isDesignActive
  );

  const wSpacingDetails = [
    { label: "Pitch Distance (mm)", value: "45" },
    { label: "End Distance (mm)", value: "35" },
    { label: "Gauge Distance (mm)", value: "50" },
    { label: "Edge Distance (mm)", value: "35" },
  ];

  return (
    <>
      <div className="output-set">
        <label className="output-label">Spacing (mm)</label>
        <button
          className={`${
            !isDesignActive ? "outputInactive-button" : "output-button grade"
          }`}
          onClick={() => setIsWebSpacingOpen((prev) => !prev)}
        >
          Web Spacing Details
        </button>

        {isWebSpacingOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-75 z-[1000] transition-opacity">
            <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[80%] md:w-[40%] lg:w-[45%] h-[50%] bg-white rounded-lg shadow-lg">
              <div className="p-4 flex flex-col h-full">
                {/* Header */}
                <div className="flex justify-between items-center mb-8 border-b pb-2">
                  <h4 className="text-xl font-thin">Web Spacing Details</h4>
                  <button onClick={() => setIsWebSpacingOpen(false)}>
                    <img
                      src={window_close}
                      alt="Close"
                      className="w-5 cursor-pointer"
                    />
                  </button>
                </div>

                {/* Note */}
                <div className="mb-8">
                  <p className="text-lg">
                    Note: Representative Image for Spacing Details - 3 x 3
                    pattern considered
                  </p>
                </div>

                {/* Details Section */}
                <div className="flex justify-between overflow-y-auto items-center border border-gray-500 h-full p-4 custom-scrollbar">
                  <div className="flex flex-col overflow-y-auto">
                    <p className="font-bold text-lg mb-4">Spacing Details</p>
                    {wSpacingDetails.map((detail, index) => (
                      <div
                        key={index}
                        className="flex justify-between items-center p-2 mt-2 mb-2"
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
                  <img src={spacingweb} alt="Spacing Details" className="w-1/2 object-fill" />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default WebSpacingDetails;
