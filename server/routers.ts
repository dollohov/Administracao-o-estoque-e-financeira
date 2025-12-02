import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, protectedProcedure, router } from "./_core/trpc";
import { z } from "zod";
import {
  createProduct,
  getProducts,
  getProductById,
  updateProduct,
  deleteProduct,
  getTotalInventoryValue,
  getLowStockProducts,
  createStockMovement,
  getStockMovements,
  getStockMovementsByDateRange,
  createFinancialTransaction,
  getFinancialTransactions,
  getFinancialTransactionsByDateRange,
  getCurrentBalance,
  getMonthlyBalance,
} from "./db";

export const appRouter = router({
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  // ============================================
  // PRODUCTS ROUTER
  // ============================================
  products: router({
    list: protectedProcedure.query(async () => {
      return getProducts();
    }),

    getById: protectedProcedure
      .input(z.object({ id: z.number() }))
      .query(async ({ input }) => {
        return getProductById(input.id);
      }),

    create: protectedProcedure
      .input(
        z.object({
          name: z.string().min(1),
          category: z.string().min(1),
          quantity: z.number().int().min(0),
          purchasePrice: z.number().int().min(0),
          salePrice: z.number().int().min(0),
        })
      )
      .mutation(async ({ input }) => {
        return createProduct({
          name: input.name,
          category: input.category,
          quantity: input.quantity,
          purchasePrice: input.purchasePrice,
          salePrice: input.salePrice,
        });
      }),

    update: protectedProcedure
      .input(
        z.object({
          id: z.number(),
          name: z.string().optional(),
          category: z.string().optional(),
          quantity: z.number().int().optional(),
          purchasePrice: z.number().int().optional(),
          salePrice: z.number().int().optional(),
        })
      )
      .mutation(async ({ input }) => {
        const { id, ...updates } = input;
        return updateProduct(id, updates);
      }),

    delete: protectedProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input }) => {
        return deleteProduct(input.id);
      }),

    getTotalInventoryValue: protectedProcedure.query(async () => {
      return getTotalInventoryValue();
    }),

    getLowStock: protectedProcedure
      .input(z.object({ threshold: z.number().int().optional() }))
      .query(async ({ input }) => {
        return getLowStockProducts(input.threshold);
      }),
  }),

  // ============================================
  // STOCK MOVEMENTS ROUTER
  // ============================================
  stockMovements: router({
    list: protectedProcedure
      .input(z.object({ productId: z.number().optional() }))
      .query(async ({ input }) => {
        return getStockMovements(input.productId);
      }),

    getByDateRange: protectedProcedure
      .input(
        z.object({
          startDate: z.date(),
          endDate: z.date(),
        })
      )
      .query(async ({ input }) => {
        return getStockMovementsByDateRange(input.startDate, input.endDate);
      }),

    create: protectedProcedure
      .input(
        z.object({
          productId: z.number(),
          type: z.enum(["entrada", "saida"]),
          quantity: z.number().int().min(1),
          observation: z.string().optional(),
        })
      )
      .mutation(async ({ input }) => {
        const movement = await createStockMovement({
          productId: input.productId,
          type: input.type,
          quantity: input.quantity,
          observation: input.observation,
          date: new Date(),
        });

        // Update product quantity
        const product = await getProductById(input.productId);
        if (product) {
          const newQuantity =
            input.type === "entrada"
              ? product.quantity + input.quantity
              : product.quantity - input.quantity;

          await updateProduct(input.productId, { quantity: newQuantity });
        }

        return movement;
      }),
  }),

  // ============================================
  // FINANCIAL TRANSACTIONS ROUTER
  // ============================================
  financialTransactions: router({
    list: protectedProcedure.query(async () => {
      return getFinancialTransactions();
    }),

    getByDateRange: protectedProcedure
      .input(
        z.object({
          startDate: z.date(),
          endDate: z.date(),
        })
      )
      .query(async ({ input }) => {
        return getFinancialTransactionsByDateRange(input.startDate, input.endDate);
      }),

    create: protectedProcedure
      .input(
        z.object({
          type: z.enum(["entrada", "saida"]),
          category: z.string().min(1),
          value: z.number().int().min(1),
          description: z.string().optional(),
        })
      )
      .mutation(async ({ input }) => {
        return createFinancialTransaction({
          type: input.type,
          category: input.category,
          value: input.value,
          description: input.description,
          date: new Date(),
        });
      }),
  }),

  // ============================================
  // DASHBOARD ROUTER
  // ============================================
  dashboard: router({
    getCurrentBalance: protectedProcedure.query(async () => {
      return getCurrentBalance();
    }),

    getTotalInventoryValue: protectedProcedure.query(async () => {
      return getTotalInventoryValue();
    }),

    getMonthlyBalance: protectedProcedure
      .input(
        z.object({
          year: z.number().int(),
          month: z.number().int().min(1).max(12),
        })
      )
      .query(async ({ input }) => {
        return getMonthlyBalance(input.year, input.month);
      }),

    getLowStockAlerts: protectedProcedure.query(async () => {
      return getLowStockProducts(10);
    }),
  }),
});

export type AppRouter = typeof appRouter;
