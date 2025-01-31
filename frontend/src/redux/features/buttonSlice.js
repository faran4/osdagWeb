import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    inputDockVisible: true,
    outputDockVisible: true,
  };

const dockSlice = createSlice({
    name: "dock",
    initialState,
    reducers: {
        toggleInputDock: (state) => { 
            state.inputDockVisible = !state.inputDockVisible;
        },
        toggleOutputDock: (state) => {
            state.outputDockVisible = !state.outputDockVisible;
        }
    }
})

export const { toggleInputDock, toggleOutputDock } = dockSlice.actions;
export default dockSlice.reducer;