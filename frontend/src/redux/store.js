import { configureStore } from "@reduxjs/toolkit";
import dataReducer from "./features/dataSlice";
import preferenceReducer from "./features/preferenceSlice";
import boltDiameterReducer from "./features/boltDiameterSlice";
import materialsReducer from "./features/materialSlice";
import beamsReducer from "./features/beamSlice";
import dockReducer from "./features/buttonSlice";
import defaultReducer from "./features/defaultSlice";
import commonInputReducer from "./features/CommonInputSlice";

const store = configureStore({
  reducer: {
    data: dataReducer,
    dock: dockReducer,
    preference: preferenceReducer,
    boltDiameters: boltDiameterReducer,
    materials: materialsReducer,
    beams: beamsReducer,
    default: defaultReducer,
    commonInputs: commonInputReducer,
  },
});

export default store;