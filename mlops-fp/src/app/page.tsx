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
  const [isModalOpen, setIsModalOpen] = useState(false); // State untuk kontrol modal

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

  const handleFilePrediction = async () => {
    if (!uploadedFile) return;
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", uploadedFile);

      const response = await fetch("https://news-backend-pso-c3c2dsfycrdubzd6.southeastasia-01.azurewebsites.net/predict", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setFileData(data.predictions);
        setIsModalOpen(true); // Buka modal setelah data berhasil diambil
      } else {
        console.error("Failed to fetch prediction for the file");
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (uploadedFile) {
      handleFilePrediction();
    }
  }, [uploadedFile]);

  const handleSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      // Jika file tidak diunggah, gunakan prediksi berdasarkan teks
      if (!uploadedFile) {
        if (!title || !description) {
          console.error("Title and description are required.");
          setIsLoading(false);
          return;
        }
  
        const formData = new FormData();
        formData.append("title", title);
        formData.append("description", description);
  
        const response = await fetch("https://news-backend-pso-c3c2dsfycrdubzd6.southeastasia-01.azurewebsites.net/predict", {
          method: "POST",
          body: formData,
        });
  
        if (response.ok) {
          const data = await response.json();
          setPredictedCategory(data.predicted_category); // Set hasil prediksi
        } else {
          console.error("Failed to fetch prediction for the text");
        }
      } else {
        console.error("Please use the file upload section to upload a CSV file.");
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

          <div className="flex items-center justify-center w-full">
            <label
              htmlFor="dropzone-file"
              className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-white hover:bg-gray-100"
            >
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

              {/* Prediction Result for Text Submission */}
      {isLoading ? (
        <p className="mt-4 text-center text-sm text-gray-500">Loading...</p>
      ) : (
        predictedCategory && !fileData.length && (
          <div className="mt-4 text-center text-lg font-medium text-gray-900">
            <p className="font-semibold">Your news category is:</p>
            <div>{Array.isArray(predictedCategory) ? predictedCategory.join(", ") : predictedCategory}</div>
          </div>
        )
      )}


        {/* Modal for Displaying File Data */}
        {isModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg shadow-lg w-11/12 max-w-4xl overflow-hidden">
              <div className="p-4 border-b flex justify-between items-center">
                <h2 className="text-lg font-medium text-gray-900">Your prediction file result is ready! Review the details below:</h2>
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  &times;
                </button>
              </div>
              <div className="p-4 overflow-auto max-h-96">
                <table className="min-w-full divide-y divide-gray-200 text-sm text-gray-800">
                  <thead className="bg-gray-100 sticky top-0">
                    <tr>
                      <th className="px-6 py-3 text-left font-medium text-gray-700 uppercase tracking-wider">
                        No
                      </th>
                      <th className="px-6 py-3 text-left font-medium text-gray-700 uppercase tracking-wider">
                        Title
                      </th>
                      <th className="px-6 py-3 text-left font-medium text-gray-700 uppercase tracking-wider">
                        Description
                      </th>
                      <th className="px-6 py-3 text-left font-medium text-gray-700 uppercase tracking-wider">
                        Predicted Category
                      </th>
                      <th className="px-6 py-3 text-left font-medium text-gray-700 uppercase tracking-wider">
                        Probability
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {fileData.map((item, index) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap">{index + 1}</td>
                        <td className="px-6 py-4 whitespace-nowrap">{item.title}</td>
                        <td className="px-6 py-4 whitespace-nowrap">{item.description}</td>
                        <td className="px-6 py-4 whitespace-nowrap">{item.predicted_category}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {(item.probability * 100).toFixed(2)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="p-4 border-t">
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 bg-gray-800 text-white rounded hover:bg-gray-700"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
