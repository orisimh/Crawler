import { useSelector } from "react-redux";
import { Navigate, Outlet } from "react-router-dom";
import { RootState } from "../../redux/store";

export default function ProtectedLayout() {

  const token = useSelector((state: RootState) => state.auth.token);

//   if (!token) {
//     return <Navigate to="/" replace />;
//   }

  return <Outlet />;
}