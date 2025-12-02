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

describe("Financial Transactions Router", () => {
  let caller: ReturnType<typeof appRouter.createCaller>;

  beforeEach(() => {
    const ctx = createMockContext();
    caller = appRouter.createCaller(ctx);
  });

  it("should create a financial transaction (entrada)", async () => {
    const transaction = await caller.financialTransactions.create({
      type: "entrada",
      category: "Venda",
      value: 50000, // R$ 500.00
      description: "Sale to customer",
    });

    expect(transaction).toBeDefined();
    expect(transaction.type).toBe("entrada");
    expect(transaction.category).toBe("Venda");
    expect(transaction.value).toBe(50000);
  });

  it("should create a financial transaction (saida)", async () => {
    const transaction = await caller.financialTransactions.create({
      type: "saida",
      category: "Aluguel",
      value: 100000, // R$ 1000.00
      description: "Monthly rent",
    });

    expect(transaction).toBeDefined();
    expect(transaction.type).toBe("saida");
    expect(transaction.category).toBe("Aluguel");
    expect(transaction.value).toBe(100000);
  });

  it("should list financial transactions", async () => {
    await caller.financialTransactions.create({
      type: "entrada",
      category: "Venda",
      value: 50000,
    });

    const transactions = await caller.financialTransactions.list();

    expect(Array.isArray(transactions)).toBe(true);
    expect(transactions.length).toBeGreaterThan(0);
  });

  it("should get current balance", async () => {
    // Create entrada
    await caller.financialTransactions.create({
      type: "entrada",
      category: "Venda",
      value: 100000, // R$ 1000.00
    });

    // Create saida
    await caller.financialTransactions.create({
      type: "saida",
      category: "Aluguel",
      value: 30000, // R$ 300.00
    });

    const balance = await caller.dashboard.getCurrentBalance();

    // Balance should be 100000 - 30000 = 70000
    expect(balance).toBe(70000);
  });

  it("should get monthly balance", async () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth() + 1;

    // Create entrada
    await caller.financialTransactions.create({
      type: "entrada",
      category: "Venda",
      value: 100000,
    });

    // Create saida
    await caller.financialTransactions.create({
      type: "saida",
      category: "Aluguel",
      value: 40000,
    });

    const monthlyBalance = await caller.dashboard.getMonthlyBalance({ year, month });

    expect(monthlyBalance.entrada).toBe(100000);
    expect(monthlyBalance.saida).toBe(40000);
    expect(monthlyBalance.balance).toBe(60000);
  });

  it("should handle multiple transactions correctly", async () => {
    // Create multiple transactions
    await caller.financialTransactions.create({
      type: "entrada",
      category: "Venda",
      value: 50000,
    });

    await caller.financialTransactions.create({
      type: "entrada",
      category: "Venda",
      value: 30000,
    });

    await caller.financialTransactions.create({
      type: "saida",
      category: "Aluguel",
      value: 20000,
    });

    const balance = await caller.dashboard.getCurrentBalance();

    // 50000 + 30000 - 20000 = 60000
    expect(balance).toBe(60000);
  });
});
