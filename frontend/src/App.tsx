import { Navigate, Route, Routes } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import HomePage from "./pages/HomePage";
import TryDemoPage from "./pages/TryDemoPage";
import { isMarketingHost } from "./marketingHost";
import { slugFromHostname, tenantBaseDomain } from "./tenantSlug";

function RootRoute() {
  const base = tenantBaseDomain();
  if (base && typeof window !== "undefined") {
    const fromHost = slugFromHostname(window.location.hostname, base);
    if (fromHost) return <ChatPage />;
  }
  if (isMarketingHost()) return <HomePage />;
  return <Navigate to="/b/demo" replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<RootRoute />} />
      <Route path="/try" element={<TryDemoPage />} />
      <Route path="/try/chat" element={<ChatPage forcedSlug="demo" demoMode />} />
      <Route path="/b/:slug" element={<ChatPage />} />
    </Routes>
  );
}
