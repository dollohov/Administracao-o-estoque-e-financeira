import { trpc } from "@/lib/trpc";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, ArrowUp, ArrowDown } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { format } from "date-fns";

interface MovementForm {
  productId: number;
  type: "entrada" | "saida";
  quantity: number;
  observation: string;
}

export default function StockMovements() {
  const [isOpen, setIsOpen] = useState(false);
  const [form, setForm] = useState<MovementForm>({
    productId: 0,
    type: "entrada",
    quantity: 0,
    observation: "",
  });

  // Queries
  const movements = trpc.stockMovements.list.useQuery({});
  const products = trpc.products.list.useQuery();

  // Mutations
  const createMovement = trpc.stockMovements.create.useMutation({
    onSuccess: () => {
      movements.refetch();
      setForm({ productId: 0, type: "entrada", quantity: 0, observation: "" });
      setIsOpen(false);
      toast.success("Movimentação registrada com sucesso!");
    },
    onError: () => {
      toast.error("Erro ao registrar movimentação");
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.productId || !form.quantity) {
      toast.error("Preencha todos os campos obrigatórios");
      return;
    }

    createMovement.mutate({
      productId: form.productId,
      type: form.type,
      quantity: form.quantity,
      observation: form.observation || undefined,
    });
  };

  const getProductName = (productId: number) => {
    return products.data?.find((p) => p.id === productId)?.name || "Produto desconhecido";
  };

  const handleCloseDialog = () => {
    setIsOpen(false);
    setForm({ productId: 0, type: "entrada", quantity: 0, observation: "" });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Movimentação de Estoque</h1>
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button className="gap-2">
              <Plus className="h-4 w-4" />
              Nova Movimentação
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Registrar Movimentação de Estoque</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="product">Produto *</Label>
                <Select
                  value={form.productId.toString()}
                  onValueChange={(value) => setForm({ ...form, productId: parseInt(value) })}
                >
                  <SelectTrigger id="product">
                    <SelectValue placeholder="Selecione um produto" />
                  </SelectTrigger>
                  <SelectContent>
                    {products.data?.map((product) => (
                      <SelectItem key={product.id} value={product.id.toString()}>
                        {product.name} (Estoque: {product.quantity})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="type">Tipo de Movimentação *</Label>
                <Select
                  value={form.type}
                  onValueChange={(value) => setForm({ ...form, type: value as "entrada" | "saida" })}
                >
                  <SelectTrigger id="type">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="entrada">📥 Entrada (Compra/Devolução)</SelectItem>
                    <SelectItem value="saida">📤 Saída (Venda/Ajuste)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="quantity">Quantidade *</Label>
                <Input
                  id="quantity"
                  type="number"
                  min="1"
                  value={form.quantity}
                  onChange={(e) => setForm({ ...form, quantity: parseInt(e.target.value) || 0 })}
                  placeholder="0"
                />
              </div>

              <div>
                <Label htmlFor="observation">Observação</Label>
                <Input
                  id="observation"
                  value={form.observation}
                  onChange={(e) => setForm({ ...form, observation: e.target.value })}
                  placeholder="Ex: Compra do fornecedor X"
                />
              </div>

              <div className="flex gap-2 justify-end">
                <Button type="button" variant="outline" onClick={handleCloseDialog}>
                  Cancelar
                </Button>
                <Button type="submit" disabled={createMovement.isPending}>
                  Registrar
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Movements Table */}
      <Card>
        <CardHeader>
          <CardTitle>Histórico de Movimentações</CardTitle>
        </CardHeader>
        <CardContent>
          {movements.isLoading ? (
            <div className="text-center py-8 text-muted-foreground">Carregando movimentações...</div>
          ) : movements.data && movements.data.length > 0 ? (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Data</TableHead>
                    <TableHead>Produto</TableHead>
                    <TableHead>Tipo</TableHead>
                    <TableHead className="text-right">Quantidade</TableHead>
                    <TableHead>Observação</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {movements.data.map((movement) => (
                    <TableRow key={movement.id}>
                      <TableCell>{format(new Date(movement.date), "dd/MM/yyyy HH:mm")}</TableCell>
                      <TableCell className="font-medium">{getProductName(movement.productId)}</TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {movement.type === "entrada" ? (
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
                      <TableCell className="text-right font-semibold">{movement.quantity}</TableCell>
                      <TableCell className="text-sm text-muted-foreground">{movement.observation || "-"}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          ) : (
            <div className="text-center py-8 text-muted-foreground">Nenhuma movimentação registrada</div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
