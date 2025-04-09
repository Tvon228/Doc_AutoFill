import { createStore } from "solid-js/store"

export interface AuthState {
	isAuthenticated: boolean
	user: null | {
		login: string
	}
}

export const [auth, setAuth] = createStore<AuthState>({
	isAuthenticated: false,
	user: null,
})
