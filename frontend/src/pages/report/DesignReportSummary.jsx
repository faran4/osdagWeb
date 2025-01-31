import React, { useState } from "react";
import { window_close } from "../../assets/assets";

const DesignReportSummary = () => {
  const [isDesignReportSummaryOpen, setIsDesignReportSummaryOpen] =
    useState(false);

  return (
    <>
      <button
        className="main-button"
        onClick={() => setIsDesignReportSummaryOpen((prev) => !prev)}
      >
        Create Design Report
      </button>
      {isDesignReportSummaryOpen && (
        <div
          className={`fixed inset-0 bg-black bg-opacity-75 z-[1000] transition-opacity ${
            isDesignReportSummaryOpen ? "opacity-100" : "opacity-0 pointer-events-none"
          }`}
        >
          <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[90%] sm:w-[70%] md:w-[50%] lg:w-[35%] max-h-[75%] bg-white rounded-lg shadow-lg overflow-y-auto custom-scrollbar">
            <div className="flex flex-col h-full">
              <div className="bg-white rounded-lg shadow-lg p-4">
                <div className="flex justify-between items-center mb-4 border-b pb-1">
                  <h2 className="text-lg font-thin">Design Report Summary</h2>
                  <button onClick={() => setIsDesignReportSummaryOpen(false)}>
                    <img
                      src={window_close}
                      alt="Close"
                      className="w-4 cursor-pointer"
                    />
                  </button>
                </div>
                <form className="space-y-2">
                  <div className="form-label">
                    <label className="text-md font-medium">Company Name:</label>
                    <input type="text" className="report-style" />
                  </div>

                  <div className="w-full flex items-center ">
                    <label className="w-[25%] text-md font-medium">
                      Company Logo:
                    </label>
                    <button type="button" className="report-button grade">
                      Browse...
                    </button>
                  </div>

                  <div className="form-label">
                    <label className="text-md font-medium">
                      Group/Team Name:
                    </label>
                    <input type="text" className="report-style" />
                  </div>

                  <div className="form-label">
                    <label className="text-md font-medium">Designer:</label>
                    <input type="text" className="report-style" />
                  </div>

                  <div className="w-[100%] relative flex">
                    <div className="w-[25%]"></div>
                    <button type="button" className="report-button grade">
                      Use Profile
                    </button>
                    <button type="button" className="report-button grade">
                      Save Profile
                    </button>
                  </div>

                  <div className="form-label">
                    <label className="text-md font-medium">Project Title:</label>
                    <input type="text" className="report-style" />
                  </div>

                  <div className="form-label">
                    <label className="block text-md font-medium">Subtitle:</label>
                    <input
                      type="text"
                      placeholder="(Optional)"
                      className="report-style"
                    />
                  </div>

                  <div className="form-label">
                    <label className="block text-md font-medium">
                      Job Number:
                    </label>
                    <input type="text" className="report-style" />
                  </div>

                  <div className="form-label">
                    <label className="block text-md font-medium">Client:</label>
                    <input type="text" className="report-style" />
                  </div>

                  <div className="form-label">
                    <label className="block text-md font-medium">
                      Additional Comments:
                    </label>
                    <textarea rows="5" className="report-style"></textarea>
                  </div>

                  <div className="flex justify-end space-x-1">
                    <button type="button" className="report-button grade">
                      Ok
                    </button>
                    <button type="submit" className="report-button grade">
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default DesignReportSummary;
