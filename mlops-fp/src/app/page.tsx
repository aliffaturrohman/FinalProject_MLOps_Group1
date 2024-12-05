'use client';
import { useState } from "react";

export default function LoginForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [predictedCategory, setPredictedCategory] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [fileError, setFileError] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  // Fungsi untuk memvalidasi file yang diunggah
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === "text/csv") {
      setUploadedFile(file);
      setFileError(null);
    } else {
      setUploadedFile(null);
      setFileError("Please upload a valid CSV file.");
    }
  };

  // Fungsi untuk mengirim data ke backend Flask
  const handleSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append("title", title);
      formData.append("description", description);
      if (uploadedFile) {
        formData.append("file", uploadedFile);
      }

      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setPredictedCategory(data.predicted_category);
      } else {
        console.error("Failed to fetch prediction");
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col justify-center bg-gradient-to-r from-green-100 to-green-600 px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-sd">
        <h1 className="mt-10 text-center text-6xl font-bold tracking-tight text-gray-900">
          Optimize News Data
        </h1>
        <h2 className="mt-4 text-center text-2xl font-medium tracking-tight text-gray-700">
          Get Accurate News Predictions Category in Seconds
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form className="space-y-6" onSubmit={handleSubmit}>
          {/* Input Title */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-900">
              Title
            </label>
            <div className="mt-2">
              <input
                id="title"
                name="title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter news title here..."
                required
                className="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-gray-900 shadow-sm placeholder-gray-400 focus:ring-2 focus:ring-black sm:text-sm"
              />
            </div>
          </div>

          {/* Input Description */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-900">
              Description
            </label>
            <div className="mt-2">
              <input
                id="description"
                name="description"
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Enter news description here..."
                required
                className="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-gray-900 shadow-sm placeholder-gray-400 focus:ring-2 focus:ring-black sm:text-sm"
              />
            </div>
          </div>

          {/* Divider with OR */}
          <div className="relative flex items-center justify-center">
            <div className="absolute inset-0 flex items-center" aria-hidden="true">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative bg-white px-3 rounded-md shadow-md">
              <span className="text-sm font-bold text-gray-700">OR</span>
            </div>
          </div>

          {/* Input File Dropzone */}
          <div className="flex items-center justify-center w-full">
            <label
              htmlFor="dropzone-file"
              className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-white hover:bg-gray-100"
            >
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <svg
                  className="w-8 h-8 mb-4 text-gray-500"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 20 16"
                  aria-hidden="true"
                >
                  <path
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                  />
                </svg>
                <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  .CSV
                </p>
              </div>
              <input
                id="dropzone-file"
                type="file"
                accept=".csv"
                className="hidden"
                onChange={handleFileChange}
              />
            </label>
          </div>
          {fileError && <p className="mt-2 text-sm text-red-500">{fileError}</p>}

          {/* Submit Button */}
          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-black px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-black"
            >
              Predict Category
            </button>
          </div>
        </form>

        {/* Loading Spinner */}
        {isLoading && (
          <div className="mt-6 text-center">
            <div className="animate-spin h-8 w-8 border-4 border-t-4 border-gray-200 border-solid rounded-full mx-auto"></div>
            <p className="mt-2 text-sm text-gray-700">Loading...</p>
          </div>
        )}

        {/* Result Section */}
        {predictedCategory && !isLoading && (
          <div className="mt-12 text-center">
            <span className="text-sm font-semibold text-gray-900">Your news prediction is: </span>
            <span className="inline-block bg-gray-200 text-red-600 text-sm font-medium px-2 py-1 rounded-md shadow">
              {predictedCategory}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
