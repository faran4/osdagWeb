import React, { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  setShowOuterPlate,
  setDesignActive,
  resetOuterPlate,
  setOuterPlateValue,
} from "../../../redux/features/preferenceSlice";
import Materials from "./Materials";
import SectionDesignation from "./SectionDesignation";
import BoltDiameter from "../../popUps/inputDockPops/BoltDiameter";
import BoltPropertyClass from "../../popUps/inputDockPops/BoltPropertyClass";
import FlangeThickness from "../../popUps/inputDockPops/FlangeThickness";
import WebSpliceThickness from "../../popUps/inputDockPops/WebSpliceThickness";
import {
  resetInputs,
  setBoltType,
  setType,
} from "../../../redux/features/defaultSlice";
import { setSelectedGrade } from "../../../redux/features/materialSlice";
import {
  setSelectedBeam,
  setTypeBeam,
} from "../../../redux/features/beamSlice";
import { resetDiameters } from "../../../redux/features/boltDiameterSlice";
import {
  resetFlangeThickness,
  resetPropertyClasses,
  resetWebThickness,
} from "../../../redux/features/CommonInputSlice";
import { submitDesignData } from "../../../redux/features/designSlice";

const InputDock = () => {
  const dispatch = useDispatch();
  const {
    boltType,
    type,
    holeType,
    slipFactor,
    edgeMethod,
    gapBetweenBeamAndSupport,
    corrosiveInfluence,
    designMethod,
  } = useSelector((state) => state.default);
  const { selectedDiameters } = useSelector((state) => state.boltDiameters);
  const { outerPlateValue } = useSelector((state) => state.preference);
  const {
    propertyClassSelected,
    webThicknessSelected,
    flangeThicknessSelected,
  } = useSelector((state) => state.commonInputs);
  const {
    selectedGrade,
    selectedConnector,
    selectedBeamGrade,
    ultimateStrengthMaterial,
    yieldStrength20mmMaterial,
    ultimateStrength,
    yieldStrength20mm,
    yieldStrength40mm,
    yieldStrengthGreater40mm,
  } = useSelector((state) => state.materials);
  const {
    selectedBeam,
    beamProperties,
    modulusOfElasticity,
    modulusOfRigidity,
    poissonsRatio,
    thermalExpansionCoefficient,
    typeBeam,
  } = useSelector((state) => state.beams);
  // Local States for Factored Loads (Bending Moment, Shear Force, etc.)
  const [bendingMoment, setBendingMoment] = useState(null);
  const [shearForce, setShearForce] = useState(null);
  const [axialForce, setAxialForce] = useState(null);
  const formRef = useRef(null);

  const handleReset = () => {
    dispatch(setDesignActive(false)); //set the state to false
    dispatch(setSelectedBeam(""));
    dispatch(setSelectedGrade(""));
    setBendingMoment(null);
    setShearForce(null);
    setAxialForce(null);
    dispatch(setBoltType("Bearing Bolt"));
    dispatch(resetDiameters());
    dispatch(resetPropertyClasses());
    dispatch(resetOuterPlate());
    dispatch(resetFlangeThickness());
    dispatch(resetWebThickness());
    dispatch(resetInputs());
    dispatch(setTypeBeam("Rolled"));
    alert("Reset Done");
  };

  // Collect all data here
  const handleSubmit = (event) => {
    if(event) event.preventDefault();

    //  Validate Required Inputs
    if (!shearForce || shearForce === "") {
      alert("Shear Force is required!");
      return;
    }
    if (!selectedBeam || selectedBeam === "") {
      alert("Please select a Beam!");
      return;
    }
    if (!boltType || boltType === "") {
      alert("Please select a Bolt Type!");
      return;
    }

    const formData = {
      bendingMoment,
      shearForce,
      axialForce,
      selectedDiameters,
      boltType,
      propertyClassSelected,
      outerPlateValue,
      flangeThicknessSelected,
      webThicknessSelected,
      ultimateStrengthMaterial,
      yieldStrength20mmMaterial,
      selectedBeam,
      beamProperties,
      selectedGrade,
      selectedConnector,
      selectedBeamGrade,
      ultimateStrength,
      yieldStrength20mm,
      yieldStrength40mm,
      yieldStrengthGreater40mm,
      type,
      holeType,
      slipFactor,
      edgeMethod,
      gapBetweenBeamAndSupport,
      corrosiveInfluence,
      designMethod,
      modulusOfElasticity,
      modulusOfRigidity,
      poissonsRatio,
      thermalExpansionCoefficient,
      typeBeam,
    };

    //dispatch API Call
    dispatch(submitDesignData(formData))
      .unwrap()
      .then((response) => {
        console.log("Success", response);
        alert("Data submitted successfully");
      })
      .catch((error) => {
        console.error("Error", error);
        alert("An error occurred");
      });

    dispatch(setDesignActive(true)); //set the state to true
    alert("Design Done");
  };

  const handlePreferenceChange = (event) => {
    const value = event.target.value;
    dispatch(setOuterPlateValue(value)); // Update the state based on the value
    if (value === "Outside + Inside") {
      dispatch(setShowOuterPlate(true)); // Update the state based on the value
    }
    if (value === "Outside") {
      dispatch(setShowOuterPlate(false)); // Update the state based on the value
    }
  };

  return (
    <>
      <div className="container-box">
        <h2 className="text-xl font-bold mb-2">Input Dock</h2>

        {/* Form starts here */}
        <form onSubmit={handleSubmit} ref={formRef}>
          {/* Connecting Members */}
          <div className="section-container">
            <h3 className="heading">Connecting Members</h3>
            <label className="form-label">
              Section Designation*
              <SectionDesignation />
            </label>
            <label className="form-label">
              Material *
              <Materials />
            </label>
          </div>

          {/* Factored Loads */}
          <div className="section-container">
            <h3 className="heading">Factored Loads</h3>
            <label className="form-label">
              Bending Moment (kNm)
              <input
                type="number"
                className="form-input around mb-1"
                value={bendingMoment || ""}
                onChange={(e) => setBendingMoment(e.target.value)}
              />
            </label>
            <label className="form-label">
              Shear Force (kN) *
              <input
                type="number"
                className="form-input around mb-1"
                value={shearForce || ""}
                onChange={(e) => setShearForce(e.target.value)}
                required
              />
            </label>
            <label className="form-label">
              Axial Force (kN)
              <input
                type="number"
                className="form-input around mb-1"
                value={axialForce || ""}
                onChange={(e) => setAxialForce(e.target.value)}
              />
            </label>
          </div>

          {/* Bolt */}
          <div className="section-container">
            <h3 className="heading">Bolt</h3>
            <BoltDiameter />
            <label className="form-label">
              Type *
              <select
                value={boltType}
                onChange={(e) => dispatch(setBoltType(e.target.value))}
                className="form-input"
              >
                <option>Bearing Bolt</option>
                <option>Friction Grip Bolt</option>
              </select>
            </label>
            <BoltPropertyClass />
          </div>

          {/* Flange Splice Plate */}
          <div className="section-container">
            <h3 className="heading">Flange Splice Plate</h3>
            <label className="form-label">
              Preference
              <select
                className="form-input"
                value={outerPlateValue}
                onChange={handlePreferenceChange}
              >
                <option>Outside</option>
                <option>Outside + Inside</option>
              </select>
            </label>
            <FlangeThickness />
          </div>

          {/* Web Splice Plate */}
          <div className="section-container">
            <h3 className="font-semibold">Web Splice Plate</h3>
            <WebSpliceThickness />
          </div>
        </form>
      </div>

      {/* Buttons */}
      <div className="flex justify-around mt-4">
        <button type="reset" onClick={handleReset} className="main-button">
          Reset
        </button>
        <button
          type="button"
          onClick={handleSubmit}
          className="main-button"
        >
          Design
        </button>
      </div>
    </>
  );
};

export default InputDock;
