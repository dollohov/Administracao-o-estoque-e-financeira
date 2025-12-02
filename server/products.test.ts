import { describe, it, expect, beforeEach, vi } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

// Mock context for authenticated user
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

describe("Products Router", () => {
  let caller: ReturnType<typeof appRouter.createCaller>;

  beforeEach(() => {
    const ctx = createMockContext();
    caller = appRouter.createCaller(ctx);
  });

  it("should create a product", async () => {
    const result = await caller.products.create({
      name: "Test Product",
      category: "Electronics",
      quantity: 10,
      purchasePrice: 10000, // R$ 100.00
      salePrice: 15000, // R$ 150.00
    });

    expect(result).toBeDefined();
    expect(result.name).toBe("Test Product");
    expect(result.category).toBe("Electronics");
    expect(result.quantity).toBe(10);
    expect(result.purchasePrice).toBe(10000);
    expect(result.salePrice).toBe(15000);
  });

  it("should list products", async () => {
    // Create a product first
    await caller.products.create({
      name: "Product 1",
      category: "Electronics",
      quantity: 5,
      purchasePrice: 5000,
      salePrice: 7500,
    });

    const products = await caller.products.list();

    expect(Array.isArray(products)).toBe(true);
    expect(products.length).toBeGreaterThan(0);
  });

  it("should get product by id", async () => {
    const created = await caller.products.create({
      name: "Product to Find",
      category: "Electronics",
      quantity: 3,
      purchasePrice: 3000,
      salePrice: 4500,
    });

    const found = await caller.products.getById({ id: created.id });

    expect(found).toBeDefined();
    expect(found?.name).toBe("Product to Find");
  });

  it("should update a product", async () => {
    const created = await caller.products.create({
      name: "Original Name",
      category: "Electronics",
      quantity: 10,
      purchasePrice: 10000,
      salePrice: 15000,
    });

    const updated = await caller.products.update({
      id: created.id,
      name: "Updated Name",
      quantity: 20,
    });

    expect(updated.name).toBe("Updated Name");
    expect(updated.quantity).toBe(20);
  });

  it("should delete a product", async () => {
    const created = await caller.products.create({
      name: "Product to Delete",
      category: "Electronics",
      quantity: 5,
      purchasePrice: 5000,
      salePrice: 7500,
    });

    const deleted = await caller.products.delete({ id: created.id });

    expect(deleted).toBe(true);
  });

  it("should get total inventory value", async () => {
    // Create products with known values
    await caller.products.create({
      name: "Item 1",
      category: "Electronics",
      quantity: 10,
      purchasePrice: 1000, // R$ 10.00
      salePrice: 1500,
    });

    await caller.products.create({
      name: "Item 2",
      category: "Electronics",
      quantity: 5,
      purchasePrice: 2000, // R$ 20.00
      salePrice: 3000,
    });

    const totalValue = await caller.products.getTotalInventoryValue();

    // 10 * 1000 + 5 * 2000 = 10000 + 10000 = 20000
    expect(totalValue).toBeGreaterThanOrEqual(20000);
  });

  it("should get low stock products", async () => {
    await caller.products.create({
      name: "Low Stock Item",
      category: "Electronics",
      quantity: 5,
      purchasePrice: 5000,
      salePrice: 7500,
    });

    const lowStock = await caller.products.getLowStock({ threshold: 10 });

    expect(Array.isArray(lowStock)).toBe(true);
  });
});
