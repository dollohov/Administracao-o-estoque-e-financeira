import express, { Request, Response } from "express";
import cors from "cors";
import dotenv from "dotenv";
import crypto from "crypto";
import axios from "axios";

dotenv.config();

const app: express.Application = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Tipos
interface EncryptedMessage {
  encrypted: string;
  iv: string;
  key: string;
}

interface TelegramResponse {
  success: boolean;
  messageId?: string;
  error?: string;
}

// Variáveis de ambiente
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;
const AES_KEY = process.env.AES_ENCRYPTION_KEY || crypto.randomBytes(32).toString("hex");
const AES_IV = process.env.AES_IV || crypto.randomBytes(16).toString("hex");

console.log("🔐 Configuração de Segurança:");
console.log(`✓ Telegram Bot: ${TELEGRAM_BOT_TOKEN ? "Configurado" : "❌ Não configurado"}`);
console.log(`✓ Chat ID: ${TELEGRAM_CHAT_ID || "❌ Não configurado"}`);
console.log(`✓ Chave AES-256: ${AES_KEY ? "Configurada" : "Gerada automaticamente"}`);

/**
 * Criptografa uma mensagem usando AES-256-CBC
 */
function encryptMessage(message: string): EncryptedMessage {
  const key = Buffer.from(AES_KEY, "hex");
  const iv = Buffer.from(AES_IV, "hex");

  const cipher = crypto.createCipheriv("aes-256-cbc", key, iv);
  let encrypted = cipher.update(message, "utf8", "hex");
  encrypted += cipher.final("hex");

  return {
    encrypted,
    iv: AES_IV,
    key: AES_KEY,
  };
}

/**
 * Descriptografa uma mensagem usando AES-256-CBC
 */
function decryptMessage(encryptedMessage: string, iv: string, key: string): string {
  const keyBuffer = Buffer.from(key, "hex");
  const ivBuffer = Buffer.from(iv, "hex");

  const decipher = crypto.createDecipheriv("aes-256-cbc", keyBuffer, ivBuffer);
  let decrypted = decipher.update(encryptedMessage, "hex", "utf8");
  decrypted += decipher.final("utf8");

  return decrypted;
}

/**
 * Envia uma mensagem para o Telegram
 */
async function sendTelegramMessage(
  message: string,
  encrypted: boolean = true
): Promise<TelegramResponse> {
  try {
    if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) {
      return {
        success: false,
        error: "Telegram credentials not configured",
      };
    }

    let finalMessage = message;

    if (encrypted) {
      const { encrypted: encryptedText, iv, key } = encryptMessage(message);
      finalMessage = `🔐 **MENSAGEM CRIPTOGRAFADA**\n\n📝 Conteúdo:\n\`\`\`\n${encryptedText}\n\`\`\`\n\n🔑 IV:\n\`\`\`\n${iv}\n\`\`\`\n\n🔐 Chave (guarde com segurança):\n\`\`\`\n${key}\n\`\`\`\n\n📖 Para descriptografar, use a chave fornecida acima.`;
    }

    const response = await axios.post(
      `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
      {
        chat_id: TELEGRAM_CHAT_ID,
        text: finalMessage,
        parse_mode: "Markdown",
      }
    );

    if (response.data.ok) {
      return {
        success: true,
        messageId: response.data.result.message_id,
      };
    }

    return {
      success: false,
      error: response.data.description,
    };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return {
      success: false,
      error: errorMessage,
    };
  }
}

// Rotas

/**
 * Health check
 */
app.get("/health", (req: Request, res: Response) => {
  res.json({
    status: "ok",
    timestamp: new Date().toISOString(),
    telegram: TELEGRAM_BOT_TOKEN ? "configured" : "not_configured",
  });
});

/**
 * Enviar mensagem criptografada para Telegram
 */
app.post("/api/telegram/send", async (req: Request, res: Response) => {
  try {
    const { message, encrypted = true } = req.body;

    if (!message) {
      return res.status(400).json({ error: "Message is required" });
    }

    const result = await sendTelegramMessage(message, encrypted);

    if (result.success) {
      return res.json({
        success: true,
        messageId: result.messageId,
        message: "Mensagem enviada com sucesso para o Telegram",
      });
    }

    return res.status(500).json({
      success: false,
      error: result.error,
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return res.status(500).json({ error: errorMessage });
  }
});

/**
 * Criptografar mensagem
 */
app.post("/api/encrypt", (req: Request, res: Response) => {
  try {
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: "Message is required" });
    }

    const encrypted = encryptMessage(message);

    return res.json({
      success: true,
      encrypted: encrypted.encrypted,
      iv: encrypted.iv,
      key: encrypted.key,
      message: "Mensagem criptografada com sucesso",
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return res.status(500).json({ error: errorMessage });
  }
});

/**
 * Descriptografar mensagem
 */
app.post("/api/decrypt", (req: Request, res: Response) => {
  try {
    const { encrypted, iv, key } = req.body;

    if (!encrypted || !iv || !key) {
      return res.status(400).json({ error: "Encrypted message, IV, and key are required" });
    }

    const decrypted = decryptMessage(encrypted, iv, key);

    return res.json({
      success: true,
      message: decrypted,
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return res.status(500).json({ error: errorMessage });
  }
});

/**
 * Enviar relatório para Telegram
 */
app.post("/api/telegram/report", async (req: Request, res: Response) => {
  try {
    const { title, data } = req.body;

    if (!title || !data) {
      return res.status(400).json({ error: "Title and data are required" });
    }

    const reportMessage = `📊 **${title}**\n\n${JSON.stringify(data, null, 2)}`;
    const result = await sendTelegramMessage(reportMessage, true);

    if (result.success) {
      return res.json({
        success: true,
        messageId: result.messageId,
        message: "Relatório enviado com sucesso",
      });
    }

    return res.status(500).json({
      success: false,
      error: result.error,
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return res.status(500).json({ error: errorMessage });
  }
});

/**
 * Enviar alerta para Telegram
 */
app.post("/api/telegram/alert", async (req: Request, res: Response) => {
  try {
    const { type, message } = req.body;

    if (!type || !message) {
      return res.status(400).json({ error: "Type and message are required" });
    }

    const alertMessage = `⚠️ **ALERTA: ${type}**\n\n${message}`;
    const result = await sendTelegramMessage(alertMessage, true);

    if (result.success) {
      return res.json({
        success: true,
        messageId: result.messageId,
        message: "Alerta enviado com sucesso",
      });
    }

    return res.status(500).json({
      success: false,
      error: result.error,
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return res.status(500).json({ error: errorMessage });
  }
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`\n🚀 Servidor rodando em http://localhost:${PORT}`);
  console.log(`📡 API Telegram: http://localhost:${PORT}/api/telegram/send`);
  console.log(`🔐 Encrypt: http://localhost:${PORT}/api/encrypt`);
  console.log(`🔓 Decrypt: http://localhost:${PORT}/api/decrypt`);
  console.log(`\n✅ Sistema pronto para receber mensagens criptografadas!\n`);
});

export default app;
