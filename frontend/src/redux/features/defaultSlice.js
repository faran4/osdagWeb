import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  holeType: "Standard",
  slipFactor: 0.3,
  edgeMethod: "Sheared or hand flame cut",
  gapBetweenBeamAndSupport: 10, // Default stored value is 3
  corrosiveInfluence: "No",
  designMethod: "Limit State Design",
  resetFlag: false,
  boltType: "Bearing Bolt", // Default Bolt Type
  type: "Non pre-tension",
};

const defaultSlice = createSlice({
  name: "default",
  initialState,
  reducers: {
    setHoleType: (state, action) => {
      state.holeType = action.payload;
    },
    setSlipFactor: (state, action) => {
      state.slipFactor = action.payload;
    },
    setEdgeMethod: (state, action) => {
      state.edgeMethod = action.payload;
    },
    setGapBetweenBeamAndSupport: (state, action) => {
      state.gapBetweenBeamAndSupport = action.payload;
    },
    setCorrosiveInfluence: (state, action) => {
      state.corrosiveInfluence = action.payload;
    },
    setDesignMethod: (state, action) => {
      state.designMethod = action.payload;
    },
    setBoltType: (state, action) => {
      state.boltType = action.payload;
      state.type =
        action.payload === "Bearing Bolt" ? "Non pre-tension" : "Pre-tension";
    },

    setType: (state, action) => {
      state.type = action.payload;
    },

    //reset function
    resetInputs: (state) => {
      Object.assign(state, initialState);
      state.resetFlag = true;
    },

    //after reset is handled, turn off reset flag
    clearResetFlag: (state) => {
      state.resetFlag = false;
    },
  },
});

export const {
  setHoleType,
  setSlipFactor,
  setEdgeMethod,
  setGapBetweenBeamAndSupport,
  setCorrosiveInfluence,
  setDesignMethod,
  resetInputs,
  clearResetFlag,
  setType,
  setBoltType,
} = defaultSlice.actions;
export default defaultSlice.reducer;
