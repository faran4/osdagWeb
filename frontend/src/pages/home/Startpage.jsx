import React from 'react';
import { Fossee_logo, iit_logo, osdagHeader } from '../../assets/assets';

const Startpage = () => {
  return (
    <div className="relative flex justify-center items-center h-full">
      <img src={osdagHeader} alt="Osdag Header" className="max-w-2xl w-full h-auto" />
      <img src={iit_logo} alt="IITBombay" className="w-24 sm:w-32 md:w-36 lg:w-40 absolute bottom-0 left-0 m-4" />
      <img src={Fossee_logo} alt="Fossee" className="w-32 sm:w-40 md:w-48 lg:w-56 absolute bottom-0 right-0 m-4" />
    </div>
  );
}

export default Startpage;