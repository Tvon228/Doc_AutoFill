import { createStore } from "solid-js/store"

export interface User {
	id: number
	login: string
	role: string
	registered_at: string
	added_by_user_id: number
	email?: string | null
	phone?: string | null
}

export interface AuthState {
	isAuthenticated: boolean
	user: User | null
	token: string | null
}

export const [auth, setAuth] = createStore<AuthState>({
	isAuthenticated: false,
	user: null,
	token: null,
})

// Вспомогательные функции
export const login = (user: User, token: string) => {
	setAuth({
		isAuthenticated: true,
		user,
		token,
	})
}

export const logout = () => {
	setAuth({
		isAuthenticated: false,
		user: null,
		token: null,
	})
}

export const updateUser = (user: Partial<User>) => {
	if (auth.user) {
		setAuth("user", { ...auth.user, ...user })
	}
}
