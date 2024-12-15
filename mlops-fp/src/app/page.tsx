'use client';
import { useState, useEffect } from "react";

export default function LoginForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [predictedCategory, setPredictedCategory] = useState<string | string[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [fileError, setFileError] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [fileData, setFileData] = useState<any[]>([]);

  // Handle file upload validation
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

  // Fetch prediction for file upload
  const handleFilePrediction = async () => {
    if (!uploadedFile) return;
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", uploadedFile);

      const response = await fetch("http://127.0.0.1:5000/predict_file", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setFileData(data.predictions);
      } else {
        console.error("Failed to fetch prediction for the file");
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Trigger prediction on file upload change
  useEffect(() => {
    if (uploadedFile) {
      handleFilePrediction();
    }
  }, [uploadedFile]);

  // Submit form data for prediction
  const handleSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const formData = new FormData();
      if (!uploadedFile) {
        formData.append("title", title);
        formData.append("description", description);
        const response = await fetch("http://127.0.0.1:5000/predict", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          setPredictedCategory(data.predicted_category);
        } else {
          console.error("Failed to fetch prediction for the text");
        }
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
          {/* Input fields */}
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
                required={!uploadedFile}
                className="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-gray-900 shadow-sm placeholder-gray-400 focus:ring-2 focus:ring-black sm:text-sm"
              />
            </div>
          </div>

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
                required={!uploadedFile}
                className="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-gray-900 shadow-sm placeholder-gray-400 focus:ring-2 focus:ring-black sm:text-sm"
              />
            </div>
          </div>

          {/* File Upload */}
          <div className="flex items-center justify-center w-full">
            <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-white hover:bg-gray-100">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <p className="mb-2 text-sm text-gray-500">
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-gray-500">.CSV</p>
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

          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-black px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-black"
            >
              Predict Category
            </button>
          </div>
        </form>

        {/* Prediction Result */}
        {isLoading ? (
          <p className="mt-4 text-center text-sm text-gray-500">Loading...</p>
        ) : (
          predictedCategory && (
            <div className="mt-4 text-center text-lg font-medium text-gray-900">
              <p className="font-semibold">Your news category is:</p>
              <div>{Array.isArray(predictedCategory) ? predictedCategory.join(", ") : predictedCategory}</div>
            </div>
          )
        )}

        {/* Display Table for Uploaded File Data */}
        {fileData.length > 0 && (
          <div className="mt-6 overflow-x-auto">
            <table className="min-w-full table-auto">
              <thead>
                <tr>
                  <th className="px-4 py-2 border">No</th>
                  <th className="px-4 py-2 border">Title</th>
                  <th className="px-4 py-2 border">Description</th>
                  <th className="px-4 py-2 border">Predicted Category</th>
                  <th className="px-4 py-2 border">Probability</th>
                </tr>
              </thead>
              <tbody>
                {fileData.map((item, index) => (
                  <tr key={index}>
                    <td className="px-4 py-2 border">{index + 1}</td>
                    <td className="px-4 py-2 border">{item.title}</td>
                    <td className="px-4 py-2 border">{item.description}</td>
                    <td className="px-4 py-2 border">{item.predicted_category}</td>
                    <td className="px-4 py-2 border">{(item.probability * 100).toFixed(2)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
