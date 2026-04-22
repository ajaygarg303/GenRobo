import { Navigate, Route, Routes } from "react-router-dom";
import ChatPage from "./pages/ChatPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/b/demo" replace />} />
      <Route path="/b/:slug" element={<ChatPage />} />
    </Routes>
  );
}
