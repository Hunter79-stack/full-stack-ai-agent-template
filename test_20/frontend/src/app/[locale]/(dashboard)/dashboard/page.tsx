"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardHeader, CardTitle, CardContent, Button } from "@/components/ui";
import { apiClient } from "@/lib/api-client";
import { useAuth } from "@/hooks";
import { ROUTES } from "@/lib/constants";
import type { HealthResponse } from "@/types";
import {
  CheckCircle,
  XCircle,
  Loader2,
  User,
  ArrowRight,
  MessageSquare,
  Database,
  Settings,
  Activity,
} from "lucide-react";
import { listCollections, getCollectionInfo } from "@/lib/rag-api";

export default function DashboardPage() {
  const { user } = useAuth();
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState(true);
  const [healthError, setHealthError] = useState(false);
  const [ragStats, setRagStats] = useState<{ collections: number; vectors: number } | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await apiClient.get<HealthResponse>("/health");
        setHealth(data);
        setHealthError(false);
      } catch {
        setHealthError(true);
      } finally {
        setHealthLoading(false);
      }
    };

    checkHealth();
    const loadRagStats = async () => {
      try {
        const data = await listCollections();
        let totalVectors = 0;
        for (const name of data.items) {
          try {
            const info = await getCollectionInfo(name);
            totalVectors += info.total_vectors;
          } catch {
            /* ignore */
          }
        }
        setRagStats({ collections: data.items.length, vectors: totalVectors });
      } catch {
        /* ignore */
      }
    };
    loadRagStats();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold sm:text-3xl">Dashboard</h1>
        <p className="text-muted-foreground text-sm sm:text-base">
          Welcome back{user?.name ? `, ${user.name}` : ""}!
        </p>
      </div>

      {/* Stats cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-muted-foreground text-sm font-medium">API Status</CardTitle>
            {healthLoading ? (
              <Loader2 className="text-muted-foreground h-4 w-4 animate-spin" />
            ) : healthError ? (
              <XCircle className="text-destructive h-4 w-4" />
            ) : (
              <CheckCircle className="h-4 w-4 text-green-500" />
            )}
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">
              {healthLoading ? "..." : healthError ? "Offline" : health?.status || "OK"}
            </p>
            {health?.version && <p className="text-muted-foreground text-xs">v{health.version}</p>}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-muted-foreground text-sm font-medium">Account</CardTitle>
            <User className="text-muted-foreground h-4 w-4" />
          </CardHeader>
          <CardContent>
            <p className="truncate text-sm font-medium">{user?.email || "..."}</p>
            <p className="text-muted-foreground text-xs">
              {user?.is_superuser ? "Admin" : "User"}
              {user?.created_at && ` · Since ${new Date(user.created_at).toLocaleDateString()}`}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-muted-foreground text-sm font-medium">AI Agent</CardTitle>
            <Activity className="text-muted-foreground h-4 w-4" />
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">pydantic_ai</p>
            <p className="text-muted-foreground text-xs">openrouter provider</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-muted-foreground text-sm font-medium">
              Knowledge Base
            </CardTitle>
            <Database className="text-muted-foreground h-4 w-4" />
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{ragStats?.vectors?.toLocaleString() ?? "..."}</p>
            <p className="text-muted-foreground text-xs">
              vectors in {ragStats?.collections ?? "..."} collection
              {ragStats?.collections !== 1 ? "s" : ""}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Quick actions */}
      <div>
        <h2 className="mb-3 text-lg font-semibold">Quick Actions</h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <Link href={ROUTES.CHAT}>
            <Card className="hover:bg-accent cursor-pointer transition-colors">
              <CardContent className="flex items-center gap-3 p-4">
                <MessageSquare className="text-primary h-5 w-5" />
                <div className="flex-1">
                  <p className="text-sm font-medium">Start a Chat</p>
                  <p className="text-muted-foreground text-xs">Talk to the AI agent</p>
                </div>
                <ArrowRight className="text-muted-foreground h-4 w-4" />
              </CardContent>
            </Card>
          </Link>
          <Link href={ROUTES.RAG}>
            <Card className="hover:bg-accent cursor-pointer transition-colors">
              <CardContent className="flex items-center gap-3 p-4">
                <Database className="text-primary h-5 w-5" />
                <div className="flex-1">
                  <p className="text-sm font-medium">Knowledge Base</p>
                  <p className="text-muted-foreground text-xs">Manage collections & search</p>
                </div>
                <ArrowRight className="text-muted-foreground h-4 w-4" />
              </CardContent>
            </Card>
          </Link>

          <Link href={ROUTES.PROFILE}>
            <Card className="hover:bg-accent cursor-pointer transition-colors">
              <CardContent className="flex items-center gap-3 p-4">
                <Settings className="text-primary h-5 w-5" />
                <div className="flex-1">
                  <p className="text-sm font-medium">Profile & Settings</p>
                  <p className="text-muted-foreground text-xs">Manage your account</p>
                </div>
                <ArrowRight className="text-muted-foreground h-4 w-4" />
              </CardContent>
            </Card>
          </Link>
        </div>
      </div>
    </div>
  );
}
