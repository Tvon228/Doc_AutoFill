import classes from "./Auth.module.sass"
import { setAuth } from "../../stores/auth.store"
import { createSignal } from "solid-js"

export default function AuthPage() {
	const [credentials, setCredentials] = createSignal({
		login: "",
		password: "",
	})

	const handleSubmit = (e: Event) => {
		e.preventDefault()
		// Здесь должна быть реальная логика аутентификации
		setAuth("isAuthenticated", true)
	}

	return (
		<div class={classes.container}>
			<form class={classes.content} onSubmit={handleSubmit}>
				<div class={classes.headerText}>
					<h1>
						<span class={classes.documentAuto}>Document Auto</span>
						<span class={classes.fill}>Fill</span>
					</h1>
				</div>

				<div class={classes.mainBlock}>
					<span class={classes.header}>Войти</span>
                    <div class={classes.divider}></div>
					<div class={classes.subMain}>
						<div class={classes.items}>
							<span class={classes.nameInput}>Логин</span>
							<input
								type="name"
								placeholder="Введите логин"
								class={classes.Input}
								value={credentials().login}
								onInput={(e) =>
									setCredentials({
										...credentials(),
										login: e.currentTarget.value,
									})
								}
							/>
						</div>
						<div class={classes.items}>
							<span class={classes.nameInput}>Пароль</span>
							<input
								type="password"
								placeholder="Введите пароль"
								class={classes.Input}
								value={credentials().password}
								onInput={(e) =>
									setCredentials({
										...credentials(),
										password: e.currentTarget.value,
									})
								}
							/>
						</div>
						<button type="submit" class={classes.loginBtn}>
							Войти в систему
						</button>
					</div>
				</div>
			</form>
		</div>
	)
}
