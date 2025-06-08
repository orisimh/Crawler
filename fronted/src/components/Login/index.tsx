import { useDispatch, useSelector } from "react-redux";
import { setUsername, setPassword, setWebsite, loginUser } from "../../redux/auth/authSlice";
import { RootState } from "../../redux/store";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Loader from "../Shared/Loader/";

export default function Login() {

  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { username, password, website, loading, error, token } = useSelector((state: RootState) => state.auth);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    dispatch<any>(loginUser());
  };

  useEffect(() => {
    if (token) {
      
      navigate("/deals");
    }
  }, [token, navigate]);


  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-100 to-blue-300">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-xl shadow-xl w-full max-w-md space-y-6"
      >
        <h2 className="text-2xl font-bold text-center text-gray-800">Site Crawler Login</h2>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Website</label>
          <select
            value={website}
            onChange={(e) => dispatch(setWebsite(e.target.value))}
            className="w-full border border-gray-300 rounded px-3 py-2"
            required
          >
            <option value="">Select Website</option>
            <option value="fo1.altius.finance">fo1.altius.finance</option>
            <option value="fo2.altius.finance">fo2.altius.finance</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            type="email"
            value={username}
            onChange={(e) => dispatch(setUsername(e.target.value))}
            className="w-full border border-gray-300 rounded px-3 py-2"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => dispatch(setPassword(e.target.value))}
            className="w-full border border-gray-300 rounded px-3 py-2"
            required
          />
        </div>

        {error && <p className="text-red-500 text-sm text-center">{error}</p>}

        <button
          type="submit"
          className="w-full h-[40px] bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          disabled={loading}
        >
          {loading ? <Loader /> : "Login"}
        </button>
      </form>
    </div>
  );
}