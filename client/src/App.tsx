import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import StockMovements from "./pages/StockMovements";
import CashFlow from "./pages/CashFlow";
import DashboardLayout from "./components/DashboardLayout";
import { useAuth } from "@/_core/hooks/useAuth";

function ProtectedRoute({ component: Component }: { component: React.ComponentType }) {
  const { isAuthenticated, loading } = useAuth();

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
    return <NotFound />;
  }

  return <Component />;
}

function Router() {
  return (
    <Switch>
      <Route path={"/"} component={Home} />
      
      {/* Dashboard Routes */}
      <Route path={"/dashboard"}>
        {() => (
          <DashboardLayout>
            <ProtectedRoute component={Dashboard} />
          </DashboardLayout>
        )}
      </Route>

      <Route path={"/products"}>
        {() => (
          <DashboardLayout>
            <ProtectedRoute component={Products} />
          </DashboardLayout>
        )}
      </Route>

      <Route path={"/stock-movements"}>
        {() => (
          <DashboardLayout>
            <ProtectedRoute component={StockMovements} />
          </DashboardLayout>
        )}
      </Route>

      <Route path={"/cash-flow"}>
        {() => (
          <DashboardLayout>
            <ProtectedRoute component={CashFlow} />
          </DashboardLayout>
        )}
      </Route>

      <Route path={"/404"} component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="light">
        <TooltipProvider>
          <Toaster />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
