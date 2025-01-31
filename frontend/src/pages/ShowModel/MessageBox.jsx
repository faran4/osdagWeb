import React from "react";

const MessageBox = () => {
  return (
    <div className="h-full m-2 border border-blue-400 overflow-y-scroll custom-scrollbar pointer-events-none">
      <textarea rows="40" className="w-full h-full p-2 focus:outline-none" name="" id="">

      </textarea>
    </div>
  );
};

export default MessageBox;
