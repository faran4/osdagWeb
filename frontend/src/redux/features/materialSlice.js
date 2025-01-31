import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// Async thunk to fetch materials from the API
export const fetchMaterials = createAsyncThunk(
  "materials/fetchMaterials",
  async (_, thunkAPI) => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/materials/");
      return response.data; // Return the response data (the material data)
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response.data); // Reject with error data
    }
  }
);

const materialSlice = createSlice({
  name: "materials",
  initialState: {
    data: [], // Material data
    loading: false, // Loading state
    error: null, // Error state
    selectedGrade: "", // Selected grade state
    selectedConnector: "", // Selected connector state
    selectedBeamGrade: "", // Selected beam grade state
    ultimateStrength: "",
    yieldStrength20mm: "",
    yieldStrength40mm: "",
    yieldStrengthGreater40mm: "",
    ultimateStrengthMaterial: "", // Global state for ultimate strength material
    yieldStrength20mmMaterial: "", // Global state for yield strength 20mm material
  },
  reducers: {
    setSelectedGrade: (state, action) => {
      state.selectedGrade = action.payload; // Set the selected grade
    },
    setSelectedConnector: (state, action) => {
      state.selectedConnector = action.payload;
      const selectedMaterial = state.data.find(
        (material) => material.Grade === action.payload
      );
      if (selectedMaterial) {
        state.ultimateStrength = selectedMaterial.Ultimate_Tensile_Stress || "";
        state.yieldStrength20mm = selectedMaterial.Yield_Stress_lt_20 || "";
        state.yieldStrength40mm = selectedMaterial.Yield_Stress_20_40 || "";
        state.yieldStrengthGreater40mm = selectedMaterial.Yield_Stress_gt_40 || "";
      } else {
        state.ultimateStrength = "";
        state.yieldStrength20mm = "";
        state.yieldStrength40mm = "";
        state.yieldStrengthGreater40mm = "";
      }
    },
    setSelectedBeamGrade: (state, action) => {
      state.selectedBeamGrade = action.payload;
      const selectedMaterial = state.data.find(
        (material) => material.Grade === action.payload
      );
      if (selectedMaterial) {
        state.ultimateStrengthMaterial = selectedMaterial.Ultimate_Tensile_Stress || "";
        state.yieldStrength20mmMaterial = selectedMaterial.Yield_Stress_lt_20 || "";
      } else {
        state.ultimateStrengthMaterial = "";
        state.yieldStrength20mmMaterial = "";
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchMaterials.pending, (state) => {
        state.loading = true; // Set loading state when the request is pending
      })
      .addCase(fetchMaterials.fulfilled, (state, action) => {
        state.data = action.payload; // Set data when the request is fulfilled
        state.loading = false; // Reset loading state
      })
      .addCase(fetchMaterials.rejected, (state, action) => {
        state.error = action.payload; // Set error state when the request is rejected
        state.loading = false; // Reset loading state
      });
  },
});

export const {
  setSelectedGrade,
  setSelectedConnector,
  setSelectedBeamGrade,
} = materialSlice.actions;

export default materialSlice.reducer;
