import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { clearResetFlag, setCorrosiveInfluence, setEdgeMethod, setGapBetweenBeamAndSupport } from "../../redux/features/defaultSlice";

const Detailing = () => {
  const dispatch = useDispatch();
  const {
    edgeMethod,
    corrosiveInfluence,
    resetFlag,
  } = useSelector((state) => state.default);

  const [inputValue, setInputValue] = useState("10");

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    dispatch(setGapBetweenBeamAndSupport(e.target.value));
  }

  useEffect(() => {
    if(resetFlag) {
      setInputValue(10); //UI resets to default
      dispatch(clearResetFlag()); //clear reset flage after handling
    }
  }, [resetFlag])

  return (
    <div className="flex flex-col gap-4 h-max-full">
      {/* Inputs */}
      <div className="flex justify-between w-full gap-10">
        <div className="flex flex-col w-1/3">
          <p className="font-semibold text-lg mb-1">Inputs</p>
          <div className="flex items-center justify-between mb-2">
            <label className="text-md">Edge Preparation Method</label>
            <select className="w-[40%] overflow-hidden text-md border border-gray-400 rounded px-1 py-0.5"
            value={edgeMethod}
            onChange={(e) => dispatch(setEdgeMethod(e.target.value))}>
              <option>Sheared or hand flame cut</option>
              <option>Rolled, machine-fla...ut, sawn and planed</option>
            </select>
          </div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-md">
              Gap between Beam and <br /> Support (mm)
            </label>
            <input
              type="number"
              value={inputValue}
              onChange={handleInputChange}
              className="w-[40%] text-md border border-blue-400 focus:outline-none rounded px-1 py-0.5"></input>
          </div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-md">
              Are the Members Exposed to <br /> Corrosive Influences?
            </label>
            <select 
            value={corrosiveInfluence}
            onChange={(e) => dispatch(setCorrosiveInfluence(e.target.value))}
            className="w-[40%] overflow-hidden text-md border border-gray-400 rounded px-1 py-0.5">
              <option>No</option>
              <option>Yes</option>
            </select>
          </div>
        </div>

        {/* Description */}
        <div className="w-2/3">
          <h3 className="text-lg mb-1">Description</h3>
          <textarea
            rows="35"
            className="w-full border border-blue-400 leading-[1] text-base overflow-y-scroll custom-scrollbar focus:outline-none p-2"
            readOnly
            value={`The minimum edge and end distances from the centre of any hole to the nearest edge of a plate shall not be less than 1.7 times the hole diameter in case of [sheared or hand flame cut edges] and 1.5 times the hole diameter in case of [Rolled, machine-flame cut, sawn and planed edges] (IS 800 - cl. 10. 2. 4. 2).

This gap should include the tolerance value of 5mm or 1.5mm. So if the assumed clearance is 5mm, then the gap should be = 10mm (= 5mm {clearance} + 5mm {tolerance}) or if the assumed clearance is 1.5mm, then the gap should be = 3mm (= 1.5mm {clearance} + 1.5mm {tolerance}). These are the default gap values based on the site practice for convenience of erection and IS 7215, Clause 2.3.1. The gap value can also be zero based on the nature of connection where clearance is not required.

Specifying whether the members are exposed to corrosive influences, here, only affects the calculation of the maximum edge distance as per cl. 10.2.4.3.`}
          />
        </div>
      </div>
    </div>
  );
};

export default Detailing;
