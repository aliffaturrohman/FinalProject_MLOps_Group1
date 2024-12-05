'use client';
import { useState } from "react";

export default function LoginForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [predictedCategory, setPredictedCategory] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false); // Tambahkan state isLoading

  // Fungsi untuk mengirim data ke backend Flask
  const handleSubmit = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    setIsLoading(true);  // Set loading saat submit form

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: title,
          description: description,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setPredictedCategory(data.predicted_category);  // Menyimpan hasil prediksi
      } else {
        console.error("Failed to fetch prediction");
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false); // Set loading selesai
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
                autoComplete="title"
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
                autoComplete="description"
                placeholder="Enter news description here..."
                required
                className="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-gray-900 shadow-sm placeholder-gray-400 focus:ring-2 focus:ring-black sm:text-sm"
              />
            </div>
          </div>

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
