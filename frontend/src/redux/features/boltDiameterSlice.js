import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// Async thunk to fetch bolt diameters from the API
export const fetchBoltDiameters = createAsyncThunk(
  "boltDiameter/fetchBoltDiameters",
  async (_, thunkAPI) => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/bolt-diameters/"
      );
      return response.data.bolt_diameters;
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response?.data || "Unknown error");
    }
  }
);

const initialState = {
  data: [], // All fetched diameters from the API
  selectedDiameters: [], // User-selected diameters
  availableDiameters: [], // Available diameters
  selectValue: "All", // Store dropdown selection in Redux
  loading: false,
  error: null,
};

const boltDiameterSlice = createSlice({
  name: "boltDiameters",
  initialState,
  reducers: {
    setSelectedDiameters: (state, action) => {
      state.selectedDiameters = action.payload;
    },
    setAvailableDiameters: (state, action) => {
      state.availableDiameters = action.payload;
    },
    setSelectValue: (state, action) => {
      state.selectValue = action.payload
    },
    resetDiameters: (state) => {
      if (state.data.length > 0) {
        const selectedValues = ["16", "20"];
        state.selectedDiameters = state.data
          .filter((d) => selectedValues.includes(d))
          .sort((a, b) => a - b);
        state.availableDiameters = state.data
          .filter((d) => !selectedValues.includes(d))
          .sort((a, b) => a - b);
        state.selectValue = "All";
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchBoltDiameters.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchBoltDiameters.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;

        // Initialize selectedDiameters and availableDiameters when data is first fetched
        const selectedValues = ["16", "20"];
        state.selectedDiameters = action.payload
          .filter((d) => selectedValues.includes(d))
          .sort((a, b) => a - b);
        state.availableDiameters = action.payload
          .filter((d) => !selectedValues.includes(d))
          .sort((a, b) => a - b);
      })
      .addCase(fetchBoltDiameters.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Failed to fetch bolt diameters";
      });
  },
});

export const { setSelectedDiameters, setAvailableDiameters, setSelectValue, resetDiameters } =
  boltDiameterSlice.actions;
export default boltDiameterSlice.reducer;
