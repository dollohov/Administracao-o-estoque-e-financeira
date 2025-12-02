import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { getLoginUrl } from "@/const";
import { useLocation } from "wouter";
import { useEffect } from "react";

export default function Home() {
  const { user, loading, isAuthenticated } = useAuth();
  const [, navigate] = useLocation();

  useEffect(() => {
    if (isAuthenticated && !loading) {
      navigate("/dashboard");
    }
  }, [isAuthenticated, loading, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Carregando...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center space-y-6 max-w-md">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              📦 Inventory & Finance Manager
            </h1>
            <p className="text-lg text-gray-600">
              Gerencie seu estoque e fluxo de caixa de forma simples e eficiente
            </p>
          </div>

          <div className="space-y-3 text-left bg-white rounded-lg p-6 shadow-sm">
            <h2 className="font-semibold text-gray-900 mb-3">Funcionalidades:</h2>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-center gap-2">
                <span className="text-green-600">✓</span> Gestão completa de produtos
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-600">✓</span> Controle de entrada e saída de estoque
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-600">✓</span> Fluxo de caixa detalhado
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-600">✓</span> Dashboard com gráficos
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-600">✓</span> Alertas de estoque baixo
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-600">✓</span> Exportação em CSV
              </li>
            </ul>
          </div>

          <Button
            size="lg"
            onClick={() => window.location.href = getLoginUrl()}
            className="w-full bg-blue-600 hover:bg-blue-700"
          >
            Fazer Login
          </Button>
        </div>
      </div>
    );
  }

  return null;
}
