import { and, eq, gte, lte, sum, desc } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { InsertUser, users, products, stockMovements, financialTransactions, Product, InsertProduct, StockMovement, InsertStockMovement, FinancialTransaction, InsertFinancialTransaction } from "../drizzle/schema";
import { ENV } from './_core/env';

let _db: ReturnType<typeof drizzle> | null = null;

// Lazily create the drizzle instance so local tooling can run without a DB.
export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) {
    throw new Error("User openId is required for upsert");
  }

  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot upsert user: database not available");
    return;
  }

  try {
    const values: InsertUser = {
      openId: user.openId,
    };
    const updateSet: Record<string, unknown> = {};

    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];

    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };

    textFields.forEach(assignNullable);

    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    }

    if (!values.lastSignedIn) {
      values.lastSignedIn = new Date();
    }

    if (Object.keys(updateSet).length === 0) {
      updateSet.lastSignedIn = new Date();
    }

    await db.insert(users).values(values).onDuplicateKeyUpdate({
      set: updateSet,
    });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get user: database not available");
    return undefined;
  }

  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);

  return result.length > 0 ? result[0] : undefined;
}

// ============================================
// PRODUCT QUERIES
// ============================================

export async function createProduct(product: InsertProduct): Promise<Product> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  await db.insert(products).values(product);
  // Get the last inserted product
  const created = await db.select().from(products).orderBy(desc(products.createdAt)).limit(1);
  return created[0]!;
}

export async function getProducts(): Promise<Product[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  return db.select().from(products).orderBy(desc(products.createdAt));
}

export async function getProductById(id: number): Promise<Product | undefined> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  const result = await db.select().from(products).where(eq(products.id, id)).limit(1);
  return result[0];
}

export async function updateProduct(id: number, updates: Partial<InsertProduct>): Promise<Product> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  await db.update(products).set(updates).where(eq(products.id, id));
  const updated = await db.select().from(products).where(eq(products.id, id)).limit(1);
  return updated[0]!;
}

export async function deleteProduct(id: number): Promise<boolean> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  const result = await db.delete(products).where(eq(products.id, id));
  return (result as any).affectedRows > 0;
}

export async function getTotalInventoryValue(): Promise<number> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  const allProducts = await db.select().from(products);
  const total = allProducts.reduce((acc, p) => acc + (p.quantity * p.purchasePrice), 0);
  return total;
}

export async function getLowStockProducts(threshold: number = 10): Promise<Product[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  const allProducts = await db.select().from(products);
  return allProducts.filter(p => p.quantity <= threshold);
}

// ============================================
// STOCK MOVEMENT QUERIES
// ============================================

export async function createStockMovement(movement: InsertStockMovement): Promise<StockMovement> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  await db.insert(stockMovements).values(movement);
  // Get the last inserted movement
  const created = await db.select().from(stockMovements).orderBy(desc(stockMovements.createdAt)).limit(1);
  return created[0]!;
}

export async function getStockMovements(productId?: number): Promise<StockMovement[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  if (productId) {
    return db.select().from(stockMovements).where(eq(stockMovements.productId, productId)).orderBy(desc(stockMovements.date));
  }
  
  return db.select().from(stockMovements).orderBy(desc(stockMovements.date));
}

export async function getStockMovementsByDateRange(startDate: Date, endDate: Date): Promise<StockMovement[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  return db.select().from(stockMovements).where(
    and(
      gte(stockMovements.date, startDate),
      lte(stockMovements.date, endDate)
    )
  ).orderBy(desc(stockMovements.date));
}

// ============================================
// FINANCIAL TRANSACTION QUERIES
// ============================================

export async function createFinancialTransaction(transaction: InsertFinancialTransaction): Promise<FinancialTransaction> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  await db.insert(financialTransactions).values(transaction);
  // Get the last inserted transaction
  const created = await db.select().from(financialTransactions).orderBy(desc(financialTransactions.createdAt)).limit(1);
  return created[0]!;
}

export async function getFinancialTransactions(): Promise<FinancialTransaction[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  return db.select().from(financialTransactions).orderBy(desc(financialTransactions.date));
}

export async function getFinancialTransactionsByDateRange(startDate: Date, endDate: Date): Promise<FinancialTransaction[]> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  return db.select().from(financialTransactions).where(
    and(
      gte(financialTransactions.date, startDate),
      lte(financialTransactions.date, endDate)
    )
  ).orderBy(desc(financialTransactions.date));
}

export async function getCurrentBalance(): Promise<number> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  const transactions = await db.select().from(financialTransactions);
  const entrada = transactions.filter(t => t.type === 'entrada').reduce((acc, t) => acc + t.value, 0);
  const saida = transactions.filter(t => t.type === 'saida').reduce((acc, t) => acc + t.value, 0);
  
  return entrada - saida;
}

export async function getMonthlyBalance(year: number, month: number): Promise<{ entrada: number; saida: number; balance: number }> {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  
  const startDate = new Date(year, month - 1, 1);
  const endDate = new Date(year, month, 0);
  
  const transactions = await db.select().from(financialTransactions).where(
    and(
      gte(financialTransactions.date, startDate),
      lte(financialTransactions.date, endDate)
    )
  );
  
  const entrada = transactions.filter(t => t.type === 'entrada').reduce((acc, t) => acc + t.value, 0);
  const saida = transactions.filter(t => t.type === 'saida').reduce((acc, t) => acc + t.value, 0);
  
  return {
    entrada,
    saida,
    balance: entrada - saida,
  };
}
