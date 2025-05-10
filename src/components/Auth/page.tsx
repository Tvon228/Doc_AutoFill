import classes from "./Auth.module.sass"
import { setAuth } from "../../stores/authStore"
import { createSignal } from "solid-js"
import { AiOutlineUser } from 'solid-icons/ai'
import { RiSystemLockPasswordLine } from 'solid-icons/ri'
import { AiOutlineEye } from 'solid-icons/ai'
import { AiOutlineEyeInvisible } from 'solid-icons/ai'

export default function AuthPage() {
	const [credentials, setCredentials] = createSignal({
		login: "",
		password: "",
	})

	const [showPassword, setShowPassword] = createSignal(false)

	const handleSubmit = async (e: Event) => {
		e.preventDefault()

		try {
			const response = await fetch("/api/auth", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(credentials()),
			})

			const data = await response.json()

			if (data.success) {
				setAuth({
					isAuthenticated: true,
					user: {
						login: data.user.login,
						role: data.user.role,
						name: data.user.name,
						position: data.user.position,
						phone: data.user.phone,
						email: data.user.email,
					},
				})
			} else {
				alert(data.error || "Ошибка авторизации")
				setCredentials({ login: "", password: "" })
			}
		} catch (error) {
			alert("Сервер недоступен")
		}
	}

	return (
		<div class={classes.container}>
			<form class={classes.content} onSubmit={handleSubmit}>
				<div class={classes.headerText}>
					<div>
						<span class={classes.documentAuto}>Document Auto</span>
						<span class={classes.fill}>Fill</span>
					</div>
					<div>
						<span class={classes.subHeader}>Система автоматического заполнения документов</span>
					</div>
				</div>

				<div class={classes.mainBlock}>
					<span class={classes.header}>Войти</span>
					<div class={classes.divider}></div>
					<div class={classes.subMain}>
						<div class={classes.items}>
							<span class={classes.nameInput}>Логин:</span>
							<div class={classes.inputs}>
								<AiOutlineUser class={classes.inputIcon} size={24} color={"#a3a9b4"} />
								<input
									type="text"
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
						</div>
						<div class={classes.items}>
							<span class={classes.nameInput}>Пароль:</span>
							<div class={classes.inputs}>
								<RiSystemLockPasswordLine class={classes.inputIcon} size={24} color={"#a3a9b4"} />
								<input
									type={showPassword() ? "text" : "password"}
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
								<button type="button"
									class={classes.eyeBtn}
									onClick={() => setShowPassword(!showPassword())}
									aria-label={showPassword() ? "Скрыть пароль" : "Показать пароль"}>
									{showPassword() ? (
										<AiOutlineEye size={24} color="#a3a9b4" />
									) : (
										<AiOutlineEyeInvisible size={24} color="#a3a9b4" />
									)}
								</button>

							</div>
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
