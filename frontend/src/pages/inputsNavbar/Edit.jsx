import React from "react";

const Edit = ({ onOpenPopup }) => {
  return (
    <div className="absolute cursor-default top-4 left-[14%] w-[10vw] bg-white mt-2 border border-black shadow-2xl z-1000">
      <ul className="m-2">
        <li
          className="pr-2 greenGrade"
          onClick={onOpenPopup} // Open the popup
        >
          Design Preferences
        </li>
      </ul>
    </div>
  );
};

export default Edit;
