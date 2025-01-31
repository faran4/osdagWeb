import React from "react";
import DesignReportSummary from "../../report/designReportSummary";
import { useSelector } from "react-redux";
import MemberCapacity from "../../popUps/outputDockPops/MemberCapacity";
import FlangeBoltCapacity from "../../popUps/outputDockPops/FlangeBoltCapacity";
import WebBoltCapacity from "../../popUps/outputDockPops/WebBoltCapacity";
import WebSpacingDetails from "../../popUps/outputDockPops/WebSpacingDetails";
import WebCapacity from "../../popUps/outputDockPops/WebCapacity";
import FlangeSpacingDetails from "../../popUps/outputDockPops/FlangeSpacingDetails";
import FlangeCapacityDetails from "../../popUps/outputDockPops/FlangeCapacityDetails";

const OutputDock = () => {

  const showOuterPlate = useSelector(
    (state) => state.preference.showOuterPlate
  );

  const isDesignActive = useSelector(
    (state) => state.preference.isDesignActive
  );

  return (
    <>
      <div
        className={`output-container
        ${
          showOuterPlate
            ? "overflow-y-scroll custom-scrollbar"
            : "hide-scrollbar"
        } 
        `}
      >
        <h2 className="output-heading">Output Dock</h2>

        {/* Member Capacity Section */}
        <div
          className={`w-full h-full ${
            !isDesignActive ? "pointer-events-none" : ""
          } `}
        >
          <div className="output-section">
            <h3 className="output-subheading">Member Capacity</h3>
            <MemberCapacity />
          </div>

          {/* Bolt Section */}
          <div className="output-section">
            <h3 className="output-subheading">Bolt</h3>
            <label className="output-label">
              Diameter (mm)
              <input type="text" className="output-input" />
            </label>
            <label className="output-label">
              Property Class *
              <input type="text" className="output-input" />
            </label>
          </div>

          {/* Bolt Capacities Section */}
          <div className="output-section">
            <h3 className="output-subheading">Bolt Capacities</h3>
            <FlangeBoltCapacity />
            <WebBoltCapacity />
          </div>

          {/* Web Splice Plate Section */}
          <div className="output-section">
            <h3 className="output-subheading">Web Splice Plate</h3>
            <label className="output-label">
              Height (mm)
              <input type="text" className="output-input" />
            </label>
            <label className="output-label">
              Width (mm)
              <input type="text" className="output-input" />
            </label>
            <label className="output-label">
              Thickness (mm) *
              <input type="text" className="output-input" />
            </label>
            <WebSpacingDetails />
            <WebCapacity />
          </div>

          {/* Flange Splice Plate Section */}
          <div className="output-section">
            <h3 className="output-subheading">Flange Splice Plate</h3>
            <h4 className="output-subheading">Outer Plate</h4>
            <label className="output-label">
              Width (mm)
              <input type="text" className="output-input" />
            </label>
            <label className="output-label">
              Length (mm)
              <input type="text" className="output-input" />
            </label>
            <label className="output-label">
              Thickness (mm) *
              <input type="text" className="output-input" />
            </label>
            <FlangeSpacingDetails />
            <FlangeCapacityDetails />
          </div>
          {showOuterPlate && (
            <div className="output-section">
              <h4 className="output-subheading">Outer Plate</h4>
              <label className="output-label">
                Width (mm)
                <input type="text" className="output-input" />
              </label>
              <label className="output-label">
                Length (mm)
                <input type="text" className="output-input" />
              </label>
              <label className="output-label">
                Thickness (mm) *
                <input type="text" className="output-input" />
              </label>
            </div>
          )}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col justify-center items-center mt-4">
        <DesignReportSummary />
        <button className="main-button outbutton">Save Output</button>
      </div>
    </>
  );
};

export default OutputDock;
