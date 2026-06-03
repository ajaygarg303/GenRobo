import { Navigate, Route, Routes } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import { slugFromHostname, tenantBaseDomain } from "./tenantSlug";

function RootRoute() {
  const base = tenantBaseDomain();
  if (base && typeof window !== "undefined") {
    const fromHost = slugFromHostname(window.location.hostname, base);
    if (fromHost) return <ChatPage />;
  }
  return <Navigate to="/b/demo" replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<RootRoute />} />
      <Route path="/b/:slug" element={<ChatPage />} />
    </Routes>
  );
}
