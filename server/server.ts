import express, { Request, Response } from "express"
import bodyParser from "body-parser"
import { readFileSync, writeFileSync } from "fs"
import path from "path"
import multer from "multer"

type User = {
	login: string
	password: string
}

const app = express()
app.use(bodyParser.json())

const dbPath = path.resolve(__dirname, "db.json")

const storage = multer.diskStorage({
	destination: (req, file, cb) => {
		cb(null, "uploads/")
	},
	filename: (req, file, cb) => {
		cb(null, Date.now() + "-" + file.originalname)
	},
})

const upload = multer({ storage })

app.post("/api/auth", (req: Request, res: Response) => {
	try {
		const db = JSON.parse(readFileSync(dbPath, "utf-8"))
		const { login, password } = req.body

		const user = db.users.find(
			(u: User) => u.login === login && u.password === password
		)

		if (user) {
			res.json({
				success: true,
				user: {
					login: user.login,
					role: user.role,
					name: user.name,
					position: user.position,
					phone: user.phone,
					email: user.email,
				},
			})
		} else {
			res.status(401).json({ success: false, error: "Неверные данные" })
		}
	} catch (error) {
		res.status(500).json({ success: false, error: "Ошибка сервера" })
	}
})

app.put("/api/profile", (req: Request, res: Response) => {
	try {
		const { login, ...updatedData } = req.body // Получаем логин из запроса
		const db = JSON.parse(readFileSync(dbPath, "utf-8"))

		// Находим пользователя по логину
		const userIndex = db.users.findIndex((u: User) => u.login === login)

		if (userIndex === -1) {
			return res.status(404).json({
				success: false,
				error: "Пользователь не найден",
			})
		}

		// Обновляем данные
		db.users[userIndex] = {
			...db.users[userIndex],
			...updatedData,
		}

		writeFileSync(dbPath, JSON.stringify(db, null, 2))
		res.json({ success: true })
	} catch (error) {
		res.status(500).json({
			success: false,
			error: "Ошибка сервера",
		})
	}
})

const PORT = 3001
app.listen(PORT, () => {
	console.log(`✅ Сервер запущен: http://localhost:${PORT}`)
})
