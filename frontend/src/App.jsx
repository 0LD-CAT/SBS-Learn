import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/UserProfile";
import ProtectedRoute from "./components/ProtectedRoute";
import OAuthSuccess from "./pages/OAuthSuccess"
import Onboarding from "./pages/Onboarding"
import Lessons from "./pages/Lessons";


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/lessons" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/oauth-success" element={<OAuthSuccess />} />
        <Route path="/onboarding" element={<Onboarding />} />
        <Route path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/lessons"
          element={
            <ProtectedRoute>
              <Lessons />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
