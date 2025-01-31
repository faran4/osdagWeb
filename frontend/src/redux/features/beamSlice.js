import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// Async thunk to fetch beams data from the API
export const fetchBeams = createAsyncThunk(
  "beams/fetchBeams",
  async (_, thunkAPI) => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/beams/"); // Change this URL to the correct API endpoint
      return response.data;
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response.data);
    }
  }
);

const beamSlice = createSlice({
  name: "beams",
  initialState: {
    data: [], // Array to hold the beams data
    loading: false, // Loading state while fetching
    error: null, // Error state for handling any issues during fetch
    selectedBeam: "", // The selected beam designation, initially empty
    beamProperties: {
      source: "",
      D: "",
      B: "",
      T: "",
      tw: "",
      FlangeSlope: "",
      R1: "",
      R2: "",
      Mass: "",
      Area: "",
      Iz: "",
      Iy: "",
      rz: "",
      ry: "",
      Zz: "",
      Zy: "",
      Zpz: "",
      Zpy: "",
      It: "",
      Iw: "",
    }, // Object to hold the properties of the selected beam
    modulusOfElasticity: 200, // Default value for Modulus of Elasticity (GPa)
    modulusOfRigidity: 76.9, // Default value for Modulus of Rigidity (GPa)
    poissonsRatio: 0.3, // Default value for Poisson's Ratio
    thermalExpansionCoefficient: 12, // Default value for Thermal Expansion Coefficient
    typeBeam: "Rolled", // Default value for Type (select option)
  },
  reducers: {
    // Action to set the selected beam in the state
    setSelectedBeam: (state, action) => {
      state.selectedBeam = action.payload;
      const beam = state.data.find((beam) => beam.Designation === action.payload);
      if (beam) {
        state.beamProperties = {
          source: beam.Source,
          D: beam.D,
          B: beam.B,
          T: beam.T,
          tw: beam.tw,
          FlangeSlope: beam.FlangeSlope,
          R1: beam.R1,
          R2: beam.R2,
          Mass: beam.Mass,
          Area: beam.Area,
          Iz: beam.Iz,
          Iy: beam.Iy,
          rz: beam.rz,
          ry: beam.ry,
          Zz: beam.Zz,
          Zy: beam.Zy,
          Zpz: beam.Zpz,
          Zpy: beam.Zpy,
          It: beam.It,
          Iw: beam.Iw,
        };
      }
    },
    setTypeBeam: (state, action) => {
      state.typeBeam = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      // Handles the start of the fetch action, sets loading to true
      .addCase(fetchBeams.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      // Handles the successful fetch action, updates data and loading state
      .addCase(fetchBeams.fulfilled, (state, action) => {
        state.data = action.payload; // Updates beams data with the fetched response
        state.loading = false; // Stop loading once data is fetched
      })
      // Handles any errors that occur during the fetch action
      .addCase(fetchBeams.rejected, (state, action) => {
        state.error = action.payload;
        state.loading = false; // Stop loading even if there's an error
      });
  },
});

export const { setSelectedBeam, setTypeBeam } = beamSlice.actions;

export default beamSlice.reducer;
