import { createStore } from "solid-js/store"

export interface AuthState {
	isAuthenticated: boolean
	user: null | {
		login: string
		role: string
		name: string
		position?: string 
		phone?: string
		email?: string
		avatarUrl?: string;
	}
}

export const [auth, setAuth] = createStore<AuthState>({
	isAuthenticated: false,
	user: null,
})
