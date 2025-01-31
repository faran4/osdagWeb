import React, { useState } from "react";
import { window_close } from "../../../assets/assets";
import { useSelector } from "react-redux";

const MemberCapacity = () => {
  const [isMemberCapacityOpen, setIsMemberCapacityOpen] = useState(false);

  const memberDetails = [
    { label: "Moment Capacity Member (kNm)", value: "752.73" },
    { label: "Shear Capacity Member (kN)", value: "507.36" },
    { label: "Axial Capacity Member (kN)", value: "3360.0" },
  ];

  const isDesignActive = useSelector(
    (state) => state.preference.isDesignActive
  );

  return (
    <>
      <div className="output-set">
        <label className="output-label">Member Capacity</label>
        <button
          className={`${
            !isDesignActive ? "outputInactive-button" : "output-button grade"
          }`}
          onClick={() => setIsMemberCapacityOpen((prev) => !prev)}
        >
          Member Capacity
        </button>

        {isMemberCapacityOpen && (
          <div className="popup-overlay opacity-100">
            {/* Popup Content */}
            <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[30%] h-[35%] bg-white rounded-lg shadow-lg">
              <div className="p-4 h-full">
                {/* Header */}
                <div className="flex justify-between items-center mb-8 border-b overflow-y-auto custom-scrollbar">
                  <h4 className="text-xl font-thin">Member Capacity</h4>
                  <button onClick={() => setIsMemberCapacityOpen(false)}>
                    <img
                      src={window_close}
                      alt="Close"
                      className="w-5 cursor-pointer"
                    />
                  </button>
                </div>

                {/* Details */}
                <div className="popup-details h-[80%]">
                  {memberDetails.map((detail, index) => (
                    <div key={index} className="popup-detail">
                      <span>{detail.label}</span>
                      <input type="text" value={detail.value} readOnly />
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

export default MemberCapacity;
