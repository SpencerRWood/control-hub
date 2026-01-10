import { createBrowserRouter, Navigate } from "react-router-dom";
import { AppShell } from "./AppShell";
// import { ApprovalsPage } from "@/features/approvals/ApprovalsPage";
import { ApprovalsListPage } from "@/features/approvals/ApprovalsListPage";
import { ApprovalDetailPage } from "@/features/approvals/ApprovalDetailPage";
import { ChatPage } from "@/features/chat/ChatPage.tsx";

export const router = createBrowserRouter([
  {
    element: <AppShell />,
    children: [
      { path: "/", element: <Navigate to="/approvals" replace /> },
      // { path: "/approvals", element: <ApprovalsPage /> },
      { path: "/approvals", element: <ApprovalsListPage /> },
      { path: "/approvals/:id", element: <ApprovalDetailPage /> },
      { path: "/chat", element: <ChatPage /> },
      
    ],
  },
]);
