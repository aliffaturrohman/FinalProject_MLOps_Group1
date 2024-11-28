import Image from "next/image";

export default function LoginForm() {
  return (
    <div className="flex min-h-screen flex-col justify-center bg-gradient-to-r from-green-400 to-green-600 px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm bg-white rounded-lg p-6 shadow-lg">
        <h1 className="text-center text-4xl font-extrabold tracking-tight text-gray-900">
          Optimize News Data
        </h1>
        <h2 className="mt-4 text-center text-lg font-medium tracking-tight text-gray-700">
          Get Accurate News Predictions Category in Seconds
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form className="space-y-6" action="#" method="POST">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-900">
              Title
            </label>
            <div className="mt-2">
              <input
                id="title"
                name="title"
                type="text"
                autoComplete="title"
                required
                className="block w-full rounded-md border border-gray-300 bg-white py-1.5 text-gray-900 shadow-sm placeholder-gray-400 focus:ring-2 focus:ring-green-600 sm:text-sm"
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
                autoComplete="description"
                required
                className="block w-full rounded-md border border-gray-300 bg-white py-1.5 text-gray-900 shadow-sm placeholder-gray-400 focus:ring-2 focus:ring-green-600 sm:text-sm"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="flex w-auto justify-center rounded-md bg-black px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-black"
            >
              Predict Category
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
