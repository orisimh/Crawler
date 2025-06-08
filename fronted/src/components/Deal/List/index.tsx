import { useSelector } from "react-redux";
import { RootState } from "../../../redux/store";
import { useEffect } from "react";
    import axios from "axios";

export default function List() {
  const { deals } = useSelector((state: RootState) => state.auth);


  useEffect(() => {

//   async function  fetchWebsites() {
//     try {
//       const res = await axios.post("http://localhost:8000/api/v1/websites");
//       return res.data;
//     } catch (error: any) {
//       if (axios.isAxiosError(error)) {
//         // ❗ Check for network issues (CORS, unreachable server)

//         // if (!error.response) {
//         //   throw new Error("Network error: server unreachable or CORS issue.");
//         // }

//         // Handle 401 from server
//         if (error.response.status === 401) {
//           throw new Error("Unauthorized: please login again.");
//         }

//         // Handle all other errors
//         throw new Error(error.response.data.detail || "Unexpected error");
//       }

//       throw error;
//     }
//   }
  
//  fetchWebsites();

}, []);
  // This effect can be used to fetch deals or perform any side effects

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-3xl mx-auto bg-white shadow-md rounded-xl p-6">
        <h2 className="text-2xl font-semibold mb-4 text-blue-800 text-center">Available Deals</h2>
        {deals?.length === 0 || !deals ? (
          <p className="text-center text-gray-500">No deals found.</p>
        ) : (
          <ul className="space-y-3">
            {deals?.map((deal, index) => (
              <li
                key={index}
                className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-2 shadow-sm hover:shadow-md transition"
              >
                {deal}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}