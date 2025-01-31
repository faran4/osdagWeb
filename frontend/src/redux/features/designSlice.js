import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// Async thunk to send form data to the backend
export const submitDesignData = createAsyncThunk(
  "design/submitDesignData",
  async (formData, thunkAPI) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/submit-design/",  // Django API endpoint
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      return response.data; // Successful response
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response?.data || "An error occurred");
    }
  }
);

// Redux slice
const designSlice = createSlice({
  name: "design",
  initialState: {
    designData: null,
    status: "idle",
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(submitDesignData.pending, (state) => {
        state.status = "loading";
      })
      .addCase(submitDesignData.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.designData = action.payload;
      })
      .addCase(submitDesignData.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      });
  },
});

export default designSlice.reducer;
