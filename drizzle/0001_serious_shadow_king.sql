CREATE TABLE `financialTransactions` (
	`id` int AUTO_INCREMENT NOT NULL,
	`type` enum('entrada','saida') NOT NULL,
	`category` varchar(100) NOT NULL,
	`value` int NOT NULL,
	`date` timestamp NOT NULL DEFAULT (now()),
	`description` text,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `financialTransactions_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `products` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`category` varchar(100) NOT NULL,
	`quantity` int NOT NULL DEFAULT 0,
	`purchasePrice` int NOT NULL,
	`salePrice` int NOT NULL,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `products_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `stockMovements` (
	`id` int AUTO_INCREMENT NOT NULL,
	`productId` int NOT NULL,
	`type` enum('entrada','saida') NOT NULL,
	`quantity` int NOT NULL,
	`date` timestamp NOT NULL DEFAULT (now()),
	`observation` text,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `stockMovements_id` PRIMARY KEY(`id`)
);
