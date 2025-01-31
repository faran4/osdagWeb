import React from "react";

const Graphics = () => {
  return (
    <div className="absolute cursor-default top-4 left-[28%] w-[10vw] bg-white mt-2 border border-black shadow-2xl z-1000">
      <ul className="m-2">
        <li className="greenGrade">Zoom In</li>
        <li className="pt-1 greenGrade">Zoom Out</li>
        <li className="pt-1 greenGrade">Pan</li>
        <li className="pt-1 greenGrade border-b border-b-gray-400">
          Rotate 3D model
        </li>
        <li className="pt-1 greenGrade">Show front view</li>
        <li className="pt-1 greenGrade">Show top view</li>
        <li className="pt-1 greenGrade border-b border-b-gray-400">Show side view</li>
        <li className="pt-1 greenGrade">Model</li>
        <li className="pt-1 greenGrade">Beam</li>
        <li className="pt-1 greenGrade border-b border-b-gray-400">Cover Plate</li>
        <li className="pt-1 greenGrade">Change Background</li>
      </ul>
    </div>
  );
};

export default Graphics;
