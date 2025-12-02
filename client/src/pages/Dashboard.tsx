import { trpc } from "@/lib/trpc";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { AlertCircle, TrendingUp, Package, DollarSign } from "lucide-react";
import { useState, useMemo } from "react";
import { format } from "date-fns";

export default function Dashboard() {
  const [selectedMonth, setSelectedMonth] = useState(new Date());

  // Fetch dashboard data
  const currentBalance = trpc.dashboard.getCurrentBalance.useQuery();
  const inventoryValue = trpc.dashboard.getTotalInventoryValue.useQuery();
  const monthlyBalance = trpc.dashboard.getMonthlyBalance.useQuery({
    year: selectedMonth.getFullYear(),
    month: selectedMonth.getMonth() + 1,
  });
  const lowStockAlerts = trpc.dashboard.getLowStockAlerts.useQuery();
  const allTransactions = trpc.financialTransactions.list.useQuery();
  const allProducts = trpc.products.list.useQuery();

  // Format currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value / 100);
  };

  // Prepare monthly data for chart
  const monthlyChartData = useMemo(() => {
    if (!allTransactions.data) return [];
    
    const months: Record<string, { entrada: number; saida: number; balance: number }> = {};
    
    allTransactions.data.forEach((transaction) => {
      const date = new Date(transaction.date);
      const monthKey = format(date, "MMM/yy");
      
      if (!months[monthKey]) {
        months[monthKey] = { entrada: 0, saida: 0, balance: 0 };
      }
      
      if (transaction.type === "entrada") {
        months[monthKey].entrada += transaction.value;
      } else {
        months[monthKey].saida += transaction.value;
      }
      
      months[monthKey].balance = months[monthKey].entrada - months[monthKey].saida;
    });

    return Object.entries(months).map(([month, data]) => ({
      month,
      entrada: data.entrada / 100,
      saida: data.saida / 100,
      balance: data.balance / 100,
    }));
  }, [allTransactions.data]);

  // Prepare product sales data
  const productSalesData = useMemo(() => {
    if (!allProducts.data) return [];
    
    return allProducts.data
      .sort((a, b) => b.quantity - a.quantity)
      .slice(0, 5)
      .map((product) => ({
        name: product.name,
        quantidade: product.quantity,
      }));
  }, [allProducts.data]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Dashboard</h1>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Current Balance */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Saldo Atual</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {currentBalance.isLoading ? "..." : formatCurrency(currentBalance.data ?? 0)}
            </div>
            <p className="text-xs text-muted-foreground">Fluxo de caixa total</p>
          </CardContent>
        </Card>

        {/* Inventory Value */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Valor do Estoque</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {inventoryValue.isLoading ? "..." : formatCurrency(inventoryValue.data ?? 0)}
            </div>
            <p className="text-xs text-muted-foreground">Valor total de compra</p>
          </CardContent>
        </Card>

        {/* Monthly Balance */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Saldo do Mês</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {monthlyBalance.isLoading ? "..." : formatCurrency(monthlyBalance.data?.balance ?? 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              Entrada: {monthlyBalance.isLoading ? "..." : formatCurrency(monthlyBalance.data?.entrada ?? 0)}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Low Stock Alerts */}
      {lowStockAlerts.data && lowStockAlerts.data.length > 0 && (
        <Card className="border-orange-200 bg-orange-50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">⚠️ Alertas de Estoque Baixo</CardTitle>
            <AlertCircle className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {lowStockAlerts.data.map((product) => (
                <div key={product.id} className="flex justify-between items-center text-sm">
                  <span>{product.name}</span>
                  <span className="font-semibold text-orange-600">{product.quantity} unidades</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Monthly Balance Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Saldo Mensal</CardTitle>
          </CardHeader>
          <CardContent>
            {monthlyChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={monthlyChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip formatter={(value: any) => formatCurrency(Number(value) * 100)} />
                  <Legend />
                  <Line type="monotone" dataKey="balance" stroke="#3b82f6" name="Saldo" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                Sem dados de transações
              </div>
            )}
          </CardContent>
        </Card>

        {/* Top Products Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Produtos Mais Movimentados</CardTitle>
          </CardHeader>
          <CardContent>
            {productSalesData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={productSalesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="quantidade" fill="#10b981" name="Quantidade" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                Sem dados de produtos
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Monthly Details */}
      <Card>
        <CardHeader>
          <CardTitle>Detalhes do Mês</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">Entradas</p>
              <p className="text-2xl font-bold text-green-600">
                {monthlyBalance.isLoading ? "..." : formatCurrency(monthlyBalance.data?.entrada ?? 0)}
              </p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Saídas</p>
              <p className="text-2xl font-bold text-red-600">
                {monthlyBalance.isLoading ? "..." : formatCurrency(monthlyBalance.data?.saida ?? 0)}
              </p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Saldo</p>
              <p className="text-2xl font-bold">
                {monthlyBalance.isLoading ? "..." : formatCurrency(monthlyBalance.data?.balance ?? 0)}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
