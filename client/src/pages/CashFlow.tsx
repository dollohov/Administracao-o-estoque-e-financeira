import { trpc } from "@/lib/trpc";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, ArrowUp, ArrowDown, Download } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { format } from "date-fns";

interface TransactionForm {
  type: "entrada" | "saida";
  category: string;
  value: number;
  description: string;
}

const CATEGORIES = {
  entrada: ["Venda", "Devolução de Cliente", "Empréstimo", "Outro"],
  saida: ["Compra de Estoque", "Salário", "Aluguel", "Conta de Luz", "Internet", "Outro"],
};

export default function CashFlow() {
  const [isOpen, setIsOpen] = useState(false);
  const [form, setForm] = useState<TransactionForm>({
    type: "entrada",
    category: "",
    value: 0,
    description: "",
  });
  const [filterType, setFilterType] = useState<"all" | "entrada" | "saida">("all");

  // Queries
  const transactions = trpc.financialTransactions.list.useQuery();
  const currentBalance = trpc.dashboard.getCurrentBalance.useQuery();

  // Mutations
  const createTransaction = trpc.financialTransactions.create.useMutation({
    onSuccess: () => {
      transactions.refetch();
      currentBalance.refetch();
      setForm({ type: "entrada", category: "", value: 0, description: "" });
      setIsOpen(false);
      toast.success("Transação registrada com sucesso!");
    },
    onError: () => {
      toast.error("Erro ao registrar transação");
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.category || !form.value) {
      toast.error("Preencha todos os campos obrigatórios");
      return;
    }

    createTransaction.mutate({
      type: form.type,
      category: form.category,
      value: Math.round(form.value * 100),
      description: form.description || undefined,
    });
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value / 100);
  };

  const handleCloseDialog = () => {
    setIsOpen(false);
    setForm({ type: "entrada", category: "", value: 0, description: "" });
  };

  const filteredTransactions = transactions.data?.filter((t) => {
    if (filterType === "all") return true;
    return t.type === filterType;
  }) || [];

  const totalEntrada = filteredTransactions
    .filter((t) => t.type === "entrada")
    .reduce((acc, t) => acc + t.value, 0);

  const totalSaida = filteredTransactions
    .filter((t) => t.type === "saida")
    .reduce((acc, t) => acc + t.value, 0);

  const handleExportCSV = () => {
    if (!transactions.data || transactions.data.length === 0) {
      toast.error("Nenhuma transação para exportar");
      return;
    }

    const csv = [
      ["Data", "Tipo", "Categoria", "Valor", "Descrição"],
      ...transactions.data.map((t) => [
        format(new Date(t.date), "dd/MM/yyyy HH:mm"),
        t.type === "entrada" ? "Entrada" : "Saída",
        t.category,
        formatCurrency(t.value),
        t.description || "",
      ]),
    ]
      .map((row) => row.map((cell) => `"${cell}"`).join(","))
      .join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `fluxo-caixa-${format(new Date(), "dd-MM-yyyy")}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
    toast.success("Arquivo exportado com sucesso!");
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Fluxo de Caixa</h1>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleExportCSV} className="gap-2">
            <Download className="h-4 w-4" />
            Exportar CSV
          </Button>
          <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <DialogTrigger asChild>
              <Button className="gap-2">
                <Plus className="h-4 w-4" />
                Nova Transação
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Registrar Transação</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="type">Tipo *</Label>
                  <Select
                    value={form.type}
                    onValueChange={(value) => {
                      setForm({ ...form, type: value as "entrada" | "saida", category: "" });
                    }}
                  >
                    <SelectTrigger id="type">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="entrada">📥 Entrada (Receita)</SelectItem>
                      <SelectItem value="saida">📤 Saída (Despesa)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="category">Categoria *</Label>
                  <Select value={form.category} onValueChange={(value) => setForm({ ...form, category: value })}>
                    <SelectTrigger id="category">
                      <SelectValue placeholder="Selecione uma categoria" />
                    </SelectTrigger>
                    <SelectContent>
                      {CATEGORIES[form.type].map((cat) => (
                        <SelectItem key={cat} value={cat}>
                          {cat}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="value">Valor (R$) *</Label>
                  <Input
                    id="value"
                    type="number"
                    step="0.01"
                    min="0.01"
                    value={form.value}
                    onChange={(e) => setForm({ ...form, value: parseFloat(e.target.value) || 0 })}
                    placeholder="0.00"
                  />
                </div>

                <div>
                  <Label htmlFor="description">Descrição</Label>
                  <Input
                    id="description"
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                    placeholder="Ex: Venda para cliente X"
                  />
                </div>

                <div className="flex gap-2 justify-end">
                  <Button type="button" variant="outline" onClick={handleCloseDialog}>
                    Cancelar
                  </Button>
                  <Button type="submit" disabled={createTransaction.isPending}>
                    Registrar
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Saldo Atual</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {currentBalance.isLoading ? "..." : formatCurrency(currentBalance.data ?? 0)}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Entradas</CardTitle>
            <ArrowUp className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{formatCurrency(totalEntrada)}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Saídas</CardTitle>
            <ArrowDown className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{formatCurrency(totalSaida)}</div>
          </CardContent>
        </Card>
      </div>

      {/* Filter */}
      <div className="flex gap-2">
        <Button
          variant={filterType === "all" ? "default" : "outline"}
          onClick={() => setFilterType("all")}
        >
          Todas
        </Button>
        <Button
          variant={filterType === "entrada" ? "default" : "outline"}
          onClick={() => setFilterType("entrada")}
          className="gap-2"
        >
          <ArrowUp className="h-4 w-4" />
          Entradas
        </Button>
        <Button
          variant={filterType === "saida" ? "default" : "outline"}
          onClick={() => setFilterType("saida")}
          className="gap-2"
        >
          <ArrowDown className="h-4 w-4" />
          Saídas
        </Button>
      </div>

      {/* Transactions Table */}
      <Card>
        <CardHeader>
          <CardTitle>Transações</CardTitle>
        </CardHeader>
        <CardContent>
          {transactions.isLoading ? (
            <div className="text-center py-8 text-muted-foreground">Carregando transações...</div>
          ) : filteredTransactions.length > 0 ? (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Data</TableHead>
                    <TableHead>Tipo</TableHead>
                    <TableHead>Categoria</TableHead>
                    <TableHead className="text-right">Valor</TableHead>
                    <TableHead>Descrição</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredTransactions.map((transaction) => (
                    <TableRow key={transaction.id}>
                      <TableCell>{format(new Date(transaction.date), "dd/MM/yyyy HH:mm")}</TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {transaction.type === "entrada" ? (
                            <>
                              <ArrowUp className="h-4 w-4 text-green-600" />
                              <span className="text-green-600 font-semibold">Entrada</span>
                            </>
                          ) : (
                            <>
                              <ArrowDown className="h-4 w-4 text-red-600" />
                              <span className="text-red-600 font-semibold">Saída</span>
                            </>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>{transaction.category}</TableCell>
                      <TableCell className="text-right font-semibold">
                        <span className={transaction.type === "entrada" ? "text-green-600" : "text-red-600"}>
                          {transaction.type === "entrada" ? "+" : "-"}
                          {formatCurrency(transaction.value)}
                        </span>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">{transaction.description || "-"}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          ) : (
            <div className="text-center py-8 text-muted-foreground">Nenhuma transação registrada</div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
