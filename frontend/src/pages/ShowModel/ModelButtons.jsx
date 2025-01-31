import { useEffect, useState } from "react";
import { leftSquare, rightSquare, yx, zx, zy } from "../../assets/assets";
import { useDispatch, useSelector } from "react-redux";
import {
  toggleInputDock,
  toggleOutputDock,
} from "../../redux/features/buttonSlice";
import { use } from "react";

const ModelButtons = () => {
  const dispatch = useDispatch();
  const [selected, setSelected] = useState("");

  const isDesignActive = useSelector(
    (state) => state.preference.isDesignActive
  );

  const handleClick = (name) => {
    setSelected((prev) => (prev === name ? "" : name));
  };

  useEffect(() => {
    if(!isDesignActive) {
      setSelected("");
    }
  }, [isDesignActive])

  return (
    <div className="flex items-center gap-8 p-3 border rounded-lg shadow-md bg-gray-100">
      {/* Blue Rectangle Buttons */}
      <div className="flex gap-1">
        <button
          className="w-8 h-8 p-1 rounded border border-gray-300"
          onClick={() => dispatch(toggleInputDock())}
        >
          <img src={leftSquare} alt="" />
        </button>
        <button
          className="w-8 h-8 p-1 rounded border border-gray-300"
          onClick={() => dispatch(toggleOutputDock())}
        >
          <img src={rightSquare} alt="" />
        </button>
      </div>

      {/* Coordinate System Icons */}
      <div className="flex gap-1">
        <img
          src={zx}
          alt="Coord 1"
          className="w-8 h-8 p-1 rounded border border-gray-300"
        />
        <img
          src={zy}
          alt="Coord 2"
          className="w-8 h-8 p-1 rounded border border-gray-300"
        />
        <img
          src={yx}
          alt="Coord 3"
          className="w-8 h-8 p-1 rounded border border-gray-300"
        />
      </div>

      {/* Checkboxes */}
      <div className={`flex gap-4 ${
            !isDesignActive ? "pointer-events-none" : ""
          } `}>
        <button
          className="flex justify-center items-center gap-1"
          onClick={() => handleClick("model")}
        >
          <div
            className={`p-1.5 border border-blue-500 ${
              selected === "model" ? "bg-blue-500" : "bg-transparent"
            }`}
          ></div>
          Model
        </button>
        <button
          className="flex justify-center items-center gap-1"
          onClick={() => handleClick("beam")}
        >
          <div
            className={`p-1.5 border border-blue-500 ${
              selected === "beam" ? "bg-blue-500" : "bg-transparent"
            }`}
          ></div>
          Beam
        </button>
        <button
          className="flex justify-center items-center gap-1"
          onClick={() => handleClick("coverPlate")}
        >
          <div
            className={`p-1.5 border border-blue-500 ${
              selected === "coverPlate" ? "bg-blue-500" : "bg-transparent"
            }`}
          ></div>
          CoverPlate
        </button>
      </div>
    </div>
  );
};

export default ModelButtons;
