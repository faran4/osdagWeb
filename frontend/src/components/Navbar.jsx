import React from 'react'
import { home } from '../assets/assets'
import { Link } from 'react-router-dom'

const Navbar = () => {
return (
    <div className='w-full h-16 flex items-center justify-center border border-b-black relative'>
        <ul className='list-none'>
            <li className='Grad text-center text-xl text-white bg-[#925a5b] p-3'>Beam-to-Beam Splice</li>
        </ul>
        <Link to='/'><img className='homeimg' src={home} alt="" /> </Link>
    </div>
)
}

export default Navbar