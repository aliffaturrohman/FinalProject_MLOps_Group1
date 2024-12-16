'use client'; // Pastikan ini ditambahkan di bagian atas
import { useRouter } from "next/router";
import { useEffect, useState } from "react";

export default function TablePage() {
  const router = useRouter(); // Pastikan router digunakan setelah client-side mounting
  const [fileData, setFileData] = useState<any[]>([]);

  useEffect(() => {
    if (router.query.data) {
      try {
        setFileData(JSON.parse(router.query.data as string));
      } catch (error) {
        console.error("Failed to parse data:", error);
      }
    }
  }, [router.query]);

  if (!router.isReady) {
    return <p>Loading...</p>; // Hindari akses router sebelum siap
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Uploaded File Data</h1>
      {fileData.length > 0 ? (
        <div className="mt-6 overflow-auto border border-gray-300 rounded-lg shadow-sm">
          <table className="min-w-full divide-y divide-gray-200 text-sm text-gray-800">
            <thead className="bg-gray-100 sticky top-0">
              <tr>
                <th className="px-6 py-3 text-left font-medium text-gray-700 uppercase tracking-wider">No</th>
                <th className="px-6 py-3 text-left font-medium text-gray-700 uppercase tracking-wider">Title</th>
                <th className="px-6 py-3 text-left font-medium text-gray-700 uppercase tracking-wider">Description</th>
                <th className="px-6 py-3 text-left font-medium text-gray-700 uppercase tracking-wider">Predicted Category</th>
                <th className="px-6 py-3 text-left font-medium text-gray-700 uppercase tracking-wider">Probability</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {fileData.map((item, index) => (
                <tr key={index} className={index % 2 === 0 ? "bg-gray-50" : ""}>
                  <td className="px-6 py-4 whitespace-nowrap">{index + 1}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{item.title}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{item.description}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{item.predicted_category}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{(item.probability * 100).toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-gray-500">No data available to display.</p>
      )}
    </div>
  );
}
