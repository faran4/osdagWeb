import { createSlice } from "@reduxjs/toolkit";

// Initial state values for all components
const initialState = {
  // Property Class States
  propertyClassAvailable: [5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9],
  propertyClassSelected: [3.6, 4.6, 4.8],
  selectPropertyValue: "All",

  // Flange Thickness States
  flangeThicknessAvailable: [
    8, 10, 12, 14, 18, 20, 22, 25, 28, 32, 36, 40, 45, 50, 56, 63, 75, 80, 90,
    100, 110, 120,
  ],
  flangeThicknessSelected: [16],
  selectFlangeThicknessValue: "All",

  // Web Splice Thickness States
  webThicknessAvailable: [
    8, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 45, 50, 56, 63, 75, 80, 90, 100,
    110, 120,
  ],
  webThicknessSelected: [10, 12],
  selectWebThicknessValue: "All",
};

const CommonInputSlice = createSlice({
  name: "commonInputs",
  initialState,
  reducers: {
    setAvailablePropertyClasses: (state, action) => {
      state.propertyClassAvailable = action.payload;
    },
    setSelectedPropertyClasses: (state, action) => {
      state.propertyClassSelected = action.payload;
    },
    setSelectPropertyValue: (state, action) => {
      state.selectPropertyValue = action.payload;
    },
    resetPropertyClasses: (state) => {
      state.propertyClassSelected = initialState.propertyClassSelected;
      state.propertyClassAvailable = initialState.propertyClassAvailable;
      state.selectPropertyValue = "All";
    },

    setAvailableFlangeThickness: (state, action) => {
      state.flangeThicknessAvailable = action.payload;
    },
    setSelectedFlangeThickness: (state, action) => {
      state.flangeThicknessSelected = action.payload;
    },
    setSelectFlangeThicknessValue: (state, action) => {
      state.selectFlangeThicknessValue = action.payload;
    },
    resetFlangeThickness: (state) => {
      state.flangeThicknessSelected = initialState.flangeThicknessSelected;
      state.flangeThicknessAvailable = initialState.flangeThicknessAvailable;
      state.selectFlangeThicknessValue = "All";
    },

    setAvailableWebThickness: (state, action) => {
      state.webThicknessAvailable = action.payload;
    },
    setSelectedWebThickness: (state, action) => {
      state.webThicknessSelected = action.payload;
    },
    setSelectWebThicknessValue: (state, action) => {
      state.selectWebThicknessValue = action.payload;
    },
    resetWebThickness: (state) => {
      state.webThicknessSelected = initialState.webThicknessSelected;
      state.webThicknessAvailable = initialState.webThicknessAvailable;
      state.selectWebThicknessValue = "All";
    },
  },
});

export const {
  // Property Class Actions
  setAvailablePropertyClasses,
  setSelectedPropertyClasses,
  setSelectPropertyValue,
  resetPropertyClasses,

  // Flange Thickness Actions
  setAvailableFlangeThickness,
  setSelectedFlangeThickness,
  setSelectFlangeThicknessValue,
  resetFlangeThickness,

  // Web Splice Thickness Actions
  setAvailableWebThickness,
  setSelectedWebThickness,
  setSelectWebThicknessValue,
  resetWebThickness,
} = CommonInputSlice.actions;

export default CommonInputSlice.reducer;
