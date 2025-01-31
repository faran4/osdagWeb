import React from 'react'

const Help = () => {
  return (
    <div className="absolute cursor-default top-4 left-[84%] w-[10vw] bg-white mt-2 border border-black shadow-2xl z-1000">
      <ul className="m-2">
        <li className="pt-1 greenGrade">Video Tutorials</li>
        <li className="pt-1 greenGrade border-b border-b-gray-400">
          Design Examples
        </li>
        <li className="pt-1 greenGrade">Ask Us a Question</li>
        <li className="pt-1 greenGrade border-b border-b-gray-400">
          About Osdag
        </li>
        <li className="pt-1 greenGrade">Check For Update</li>
      </ul>
    </div>
  )
}

export default Help