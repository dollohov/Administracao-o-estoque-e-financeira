import { describe, it, expect, beforeEach } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

function createMockContext(): TrpcContext {
  return {
    user: {
      id: 1,
      openId: "test-user",
      email: "test@example.com",
      name: "Test User",
      loginMethod: "manus",
      role: "user",
      createdAt: new Date(),
      updatedAt: new Date(),
      lastSignedIn: new Date(),
    },
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {} as TrpcContext["res"],
  };
}

describe("Stock Movements Router", () => {
  let caller: ReturnType<typeof appRouter.createCaller>;

  beforeEach(() => {
    const ctx = createMockContext();
    caller = appRouter.createCaller(ctx);
  });

  it("should create a stock movement (entrada)", async () => {
    // Create a product first
    const product = await caller.products.create({
      name: "Test Product",
      category: "Electronics",
      quantity: 0,
      purchasePrice: 5000,
      salePrice: 7500,
    });

    // Create stock movement
    const movement = await caller.stockMovements.create({
      productId: product.id,
      type: "entrada",
      quantity: 10,
      observation: "Initial stock",
    });

    expect(movement).toBeDefined();
    expect(movement.productId).toBe(product.id);
    expect(movement.type).toBe("entrada");
    expect(movement.quantity).toBe(10);
  });

  it("should create a stock movement (saida)", async () => {
    // Create a product with stock
    const product = await caller.products.create({
      name: "Test Product",
      category: "Electronics",
      quantity: 20,
      purchasePrice: 5000,
      salePrice: 7500,
    });

    // Create stock movement (saida)
    const movement = await caller.stockMovements.create({
      productId: product.id,
      type: "saida",
      quantity: 5,
      observation: "Sale",
    });

    expect(movement).toBeDefined();
    expect(movement.type).toBe("saida");
    expect(movement.quantity).toBe(5);
  });

  it("should update product quantity on entrada", async () => {
    const product = await caller.products.create({
      name: "Test Product Entrada",
      category: "Electronics",
      quantity: 10,
      purchasePrice: 5000,
      salePrice: 7500,
    });

    await caller.stockMovements.create({
      productId: product.id,
      type: "entrada",
      quantity: 5,
    });

    // Small delay to ensure update is complete
    await new Promise(resolve => setTimeout(resolve, 100));

    const updated = await caller.products.getById({ id: product.id });
    expect(updated?.quantity).toBe(15); // 10 + 5
  });

  it("should update product quantity on saida", async () => {
    const product = await caller.products.create({
      name: "Test Product Saida",
      category: "Electronics",
      quantity: 20,
      purchasePrice: 5000,
      salePrice: 7500,
    });

    await caller.stockMovements.create({
      productId: product.id,
      type: "saida",
      quantity: 5,
    });

    // Small delay to ensure update is complete
    await new Promise(resolve => setTimeout(resolve, 100));

    const updated = await caller.products.getById({ id: product.id });
    expect(updated?.quantity).toBe(15); // 20 - 5
  });

  it("should list stock movements", async () => {
    const product = await caller.products.create({
      name: "Test Product",
      category: "Electronics",
      quantity: 0,
      purchasePrice: 5000,
      salePrice: 7500,
    });

    await caller.stockMovements.create({
      productId: product.id,
      type: "entrada",
      quantity: 10,
    });

    const movements = await caller.stockMovements.list({});

    expect(Array.isArray(movements)).toBe(true);
    expect(movements.length).toBeGreaterThan(0);
  });

  it("should filter movements by product id", async () => {
    const product1 = await caller.products.create({
      name: "Product 1",
      category: "Electronics",
      quantity: 0,
      purchasePrice: 5000,
      salePrice: 7500,
    });

    const product2 = await caller.products.create({
      name: "Product 2",
      category: "Electronics",
      quantity: 0,
      purchasePrice: 5000,
      salePrice: 7500,
    });

    await caller.stockMovements.create({
      productId: product1.id,
      type: "entrada",
      quantity: 10,
    });

    await caller.stockMovements.create({
      productId: product2.id,
      type: "entrada",
      quantity: 5,
    });

    const movements = await caller.stockMovements.list({ productId: product1.id });

    expect(movements.every((m) => m.productId === product1.id)).toBe(true);
  });
});
