import React, { useState } from 'react'
import Navbar from '../../components/Navbar'
import { bbcoverplatebolted } from '../../assets/assets'
import { useNavigate } from 'react-router-dom'

const Connection = () => {

  const [checked, setChecked] = useState(false)
  const navigate = useNavigate();

  const handleStart = () => {
    if(checked) {
      navigate('/bbcoverplate'); // Navigate to the next page if the label is clicked
    } else {
      alert('Please select a connection type') // Show an alert if not clicked
    }
  }

  return (
    <div className='w-full h-full border border-black flex flex-col items-center'>
      <Navbar />
      <div className='flex flex-grow flex-col items-center justify-center'>
        <p className='font-bold text-lg mb-4'>Cover Plate Bolted</p>
          <label className='flex items-center cursor-pointer gap-2'>
          <input type="radio" onChange={() => setChecked(true)}/>
          <img className='max-w-md' src={bbcoverplatebolted} alt="" />
          </label>
      </div>
      <button
        className='start-button mb-4'
        onClick={handleStart} // Check label click status on button click
      >
        Start
      </button>
    </div>
  )
}

export default Connection