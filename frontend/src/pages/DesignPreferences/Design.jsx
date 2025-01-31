import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setDesignMethod } from '../../redux/features/defaultSlice';

const Design = () => {
  const dispatch = useDispatch();
  const { designMethod } = useSelector((state) => state.default); 
  return (
    <div className="flex flex-col gap-4 h-[66vh] mb-1">
    {/* Inputs */}
    <div className="flex justify-between w-full gap-10">
      <div className="flex flex-col w-1/4">
        <p className="font-semibold text-lg mb-1">Inputs</p>
        <div className="flex items-center justify-between mb-2">
          <label className="text-md">Design Method</label>
          <select 
          value={designMethod}
          onChange={(e) => dispatch(setDesignMethod(e.target.value))}
          className="w-[45%] overflow-hidden text-md border border-gray-400 rounded px-1 py-0.5 mr-10">
            <option>Limit State Design</option>
            <option disabled>Limit State {"(ca...y based)"} Design</option>
            <option disabled>Working Stress Design</option>
          </select>
        </div>
      </div>
    </div>
  </div>
  )
}

export default Design