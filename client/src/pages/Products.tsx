import { trpc } from "@/lib/trpc";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, Edit2, Trash2, AlertCircle } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

interface ProductForm {
  name: string;
  category: string;
  quantity: number;
  purchasePrice: number;
  salePrice: number;
}

export default function Products() {
  const [isOpen, setIsOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<ProductForm>({
    name: "",
    category: "",
    quantity: 0,
    purchasePrice: 0,
    salePrice: 0,
  });

  // Queries
  const products = trpc.products.list.useQuery();
  const lowStock = trpc.products.getLowStock.useQuery({ threshold: 10 });

  // Mutations
  const createProduct = trpc.products.create.useMutation({
    onSuccess: () => {
      products.refetch();
      setForm({ name: "", category: "", quantity: 0, purchasePrice: 0, salePrice: 0 });
      setIsOpen(false);
      toast.success("Produto criado com sucesso!");
    },
    onError: () => {
      toast.error("Erro ao criar produto");
    },
  });

  const updateProduct = trpc.products.update.useMutation({
    onSuccess: () => {
      products.refetch();
      setForm({ name: "", category: "", quantity: 0, purchasePrice: 0, salePrice: 0 });
      setEditingId(null);
      setIsOpen(false);
      toast.success("Produto atualizado com sucesso!");
    },
    onError: () => {
      toast.error("Erro ao atualizar produto");
    },
  });

  const deleteProduct = trpc.products.delete.useMutation({
    onSuccess: () => {
      products.refetch();
      toast.success("Produto deletado com sucesso!");
    },
    onError: () => {
      toast.error("Erro ao deletar produto");
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.name || !form.category) {
      toast.error("Preencha todos os campos obrigatórios");
      return;
    }

    if (editingId) {
      updateProduct.mutate({
        id: editingId,
        ...form,
      });
    } else {
      createProduct.mutate(form);
    }
  };

  const handleEdit = (product: any) => {
    setEditingId(product.id);
    setForm({
      name: product.name,
      category: product.category,
      quantity: product.quantity,
      purchasePrice: product.purchasePrice,
      salePrice: product.salePrice,
    });
    setIsOpen(true);
  };

  const handleDelete = (id: number) => {
    if (confirm("Tem certeza que deseja deletar este produto?")) {
      deleteProduct.mutate({ id });
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value / 100);
  };

  const handleCloseDialog = () => {
    setIsOpen(false);
    setEditingId(null);
    setForm({ name: "", category: "", quantity: 0, purchasePrice: 0, salePrice: 0 });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Gestão de Produtos</h1>
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button className="gap-2">
              <Plus className="h-4 w-4" />
              Novo Produto
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>{editingId ? "Editar Produto" : "Novo Produto"}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="name">Nome do Produto *</Label>
                <Input
                  id="name"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="Ex: Notebook"
                />
              </div>

              <div>
                <Label htmlFor="category">Categoria *</Label>
                <Input
                  id="category"
                  value={form.category}
                  onChange={(e) => setForm({ ...form, category: e.target.value })}
                  placeholder="Ex: Eletrônicos"
                />
              </div>

              <div>
                <Label htmlFor="quantity">Quantidade</Label>
                <Input
                  id="quantity"
                  type="number"
                  value={form.quantity}
                  onChange={(e) => setForm({ ...form, quantity: parseInt(e.target.value) || 0 })}
                  placeholder="0"
                />
              </div>

              <div>
                <Label htmlFor="purchasePrice">Preço de Compra (R$) *</Label>
                <Input
                  id="purchasePrice"
                  type="number"
                  step="0.01"
                  value={form.purchasePrice / 100}
                  onChange={(e) => setForm({ ...form, purchasePrice: Math.round(parseFloat(e.target.value) * 100) || 0 })}
                  placeholder="0.00"
                />
              </div>

              <div>
                <Label htmlFor="salePrice">Preço de Venda (R$) *</Label>
                <Input
                  id="salePrice"
                  type="number"
                  step="0.01"
                  value={form.salePrice / 100}
                  onChange={(e) => setForm({ ...form, salePrice: Math.round(parseFloat(e.target.value) * 100) || 0 })}
                  placeholder="0.00"
                />
              </div>

              <div className="flex gap-2 justify-end">
                <Button type="button" variant="outline" onClick={handleCloseDialog}>
                  Cancelar
                </Button>
                <Button type="submit" disabled={createProduct.isPending || updateProduct.isPending}>
                  {editingId ? "Atualizar" : "Criar"}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Low Stock Alert */}
      {lowStock.data && lowStock.data.length > 0 && (
        <Card className="border-orange-200 bg-orange-50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">⚠️ Produtos com Estoque Baixo</CardTitle>
            <AlertCircle className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-sm text-orange-800">
              {lowStock.data.length} produto(s) com estoque abaixo de 10 unidades
            </div>
          </CardContent>
        </Card>
      )}

      {/* Products Table */}
      <Card>
        <CardHeader>
          <CardTitle>Produtos Cadastrados</CardTitle>
        </CardHeader>
        <CardContent>
          {products.isLoading ? (
            <div className="text-center py-8 text-muted-foreground">Carregando produtos...</div>
          ) : products.data && products.data.length > 0 ? (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Nome</TableHead>
                    <TableHead>Categoria</TableHead>
                    <TableHead className="text-right">Quantidade</TableHead>
                    <TableHead className="text-right">Preço Compra</TableHead>
                    <TableHead className="text-right">Preço Venda</TableHead>
                    <TableHead className="text-right">Ações</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {products.data.map((product) => (
                    <TableRow key={product.id}>
                      <TableCell className="font-medium">{product.name}</TableCell>
                      <TableCell>{product.category}</TableCell>
                      <TableCell className="text-right">
                        <span
                          className={product.quantity <= 10 ? "text-orange-600 font-semibold" : ""}
                        >
                          {product.quantity}
                        </span>
                      </TableCell>
                      <TableCell className="text-right">{formatCurrency(product.purchasePrice)}</TableCell>
                      <TableCell className="text-right">{formatCurrency(product.salePrice)}</TableCell>
                      <TableCell className="text-right">
                        <div className="flex gap-2 justify-end">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleEdit(product)}
                          >
                            <Edit2 className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDelete(product.id)}
                            className="text-red-600 hover:text-red-700"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          ) : (
            <div className="text-center py-8 text-muted-foreground">Nenhum produto cadastrado</div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
