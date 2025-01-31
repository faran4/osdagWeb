import React from "react";

const File = () => {
  return (
    <div className="absolute cursor-default top-4 left-0 w-[10vw] bg-white mt-2 border border-black shadow-2xl z-1000">
      <ul className="m-2">
        <li className="greenGrade border-b border-b-gray-400">
          Load input
        </li>
        <li className="pt-1 greenGrade">Save input</li>
        <li className="pt-1 greenGrade">Save log messages</li>
        <li className="pt-1 greenGrade border-b border-b-gray-400">
          Create design report
        </li>
        <li className="pt-1 greenGrade">Save 3D model</li>
        <li className="pt-1 greenGrade">Save CAD image</li>
      </ul>
    </div>
  );
};

export default File;
