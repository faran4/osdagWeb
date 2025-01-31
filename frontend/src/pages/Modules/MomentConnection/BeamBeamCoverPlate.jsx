import React from "react";
import Header from "../../../components/Header";
import InputDock from "./InputDock";
import Model from "../../ShowModel/Model";
import MessageBox from "../../ShowModel/MessageBox";
import OutputDock from "./OutputDock";
import ModelButtons from "../../ShowModel/ModelButtons";
import { useSelector } from "react-redux";

const BeamBeamCoverPlate = () => {
  const inputDockVisible = useSelector((state) => state.dock.inputDockVisible);
  const outputDockVisible = useSelector(
    (state) => state.dock.outputDockVisible
  );

  return (
    <div className="w-full h-full flex flex-col">
      {/* Header Section */}
      <div className="w-full">
        <Header />
      </div>

      {/* Main Content Section */}
      <div className="w-full flex flex-grow">
        {/* Left Sidebar (InputDock) */}
        {inputDockVisible && (
          <div className="w-[25rem] h-[92vh] mt-2 flex-shrink-0 ml-2">
            <InputDock />
          </div>
        )}

        {/* Center Portion (Model + MessageBox) */}
        <div className="h-[95vh] flex flex-col flex-grow">
          {/* Model ButtonSection Section */}
          <div className="w-full flex-grow h-[5%]">
            <ModelButtons />
          </div>
          {/* Model Section */}
          <div className="w-full flex-grow h-[65%]">
            <Model />
          </div>
          {/* MessageBox Section */}
          <div className="w-full flex-grow h-[30%] mt-2">
            <MessageBox />
          </div>
        </div>

        {/* Right Sidebar (OutputDock) */}
        {outputDockVisible && (
          <div className="w-[25rem] h-[92vh] mt-2 flex-shrink-0 mr-2">
            <OutputDock />
          </div>
        )}
      </div>
    </div>
  );
};

export default BeamBeamCoverPlate;
