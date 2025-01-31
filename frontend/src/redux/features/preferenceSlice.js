import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    showOuterPlate: false,
    outerPlateValue: "Outside",
    isDesignActive: false,
};

const preferenceSlice = createSlice({
    name: "preference",
    initialState,
    reducers: {
        setShowOuterPlate: (state, action) => {
            state.showOuterPlate = action.payload;// Update state based on payload
        },
        setOuterPlateValue: (state, action) => {
            state.outerPlateValue = action.payload; // Update state based on payload
        },
        setDesignActive: (state, action) => { 
            state.isDesignActive = action.payload; // Update state based on payload
        },
        resetOuterPlate: (state) => {
            state.showOuterPlate = initialState.showOuterPlate;
            state.outerPlateValue = "Outside";
        }
    },
});

export const {setShowOuterPlate, setDesignActive, resetOuterPlate, setOuterPlateValue} = preferenceSlice.actions;
export default preferenceSlice.reducer;