import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import List from "./components/Deal/List";
import ProtectedLayout from "./components/Layout";
import { useSelector } from "react-redux";
import { RootState } from "./redux/store";

function App() {
  const token = useSelector((state: RootState) => state.auth.token);
  console.log("Token from Redux:", token);
  return (
    <Router>
      <Routes>

        {/* Public route */}
        <Route path="/" element={<Login />} />

        {/* Protected routes */}
        <Route element={<ProtectedLayout />}>
        <Route path="/deals" element={token ? <List /> : <Navigate to="/" />} />
          {/* <Route path="/deals" element={<List />} /> */}
        </Route>

      </Routes>
    </Router>
  );
}

export default App;