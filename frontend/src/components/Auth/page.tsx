import classes from "./Auth.module.sass"

import { createSignal } from "solid-js"
import { AiOutlineUser } from 'solid-icons/ai'
import { RiSystemLockPasswordLine } from 'solid-icons/ri'
import { AiOutlineEye } from 'solid-icons/ai'
import { AiOutlineEyeInvisible } from 'solid-icons/ai'

import { login } from "../../stores/authStore"
import { useNavigate } from "@solidjs/router"

export default function AuthPage() {
	const [credentials, setCredentials] = createSignal({ login: "", password: "" });
	const [showPassword, setShowPassword] = createSignal(false);

	const [_, setError] = createSignal("");
	const navigate = useNavigate();

	const handleSubmit = async (e: Event) => {
		e.preventDefault();
		setError("");

		try {
			const response = await fetch("/auth/login", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					login: credentials().login,
					password: credentials().password,
				}),
			});

			if (!response.ok) {
				const errorData = await response.json();
				setError(errorData.message || "Неверный логин или пароль");
				return;
			}

			const data = await response.json();
			login(
				{
					id: data.id,
					login: data.login,
					role: data.role,
					registered_at: data.registered_at,
					added_by_user_id: data.added_by_user_id,
					email: data.email,
					phone: data.phone,
				},
				data.token || ""
			);
			navigate("/app");
		} catch (err) {
			setError("Ошибка подключения к серверу");
			console.error(err);
		}
	};


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
									placeholder="main@admin.com"
									class={classes.Input}
									value={credentials().login}
									onInput={(e) => setCredentials({ ...credentials(), login: e.currentTarget.value })}
									required
								/>
							</div>
						</div>
						<div class={classes.items}>
							<span class={classes.nameInput}>Пароль:</span>
							<div class={classes.inputs}>
								<RiSystemLockPasswordLine class={classes.inputIcon} size={24} color={"#a3a9b4"} />
								<input
									type={showPassword() ? "text" : "password"} // Используем сигнал showPassword
									placeholder="Введите пароль"
									class={classes.Input}
									value={credentials().password}
									onInput={(e) => setCredentials({ ...credentials(), password: e.currentTarget.value })}
									required
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
				<footer class={classes.footer}>
					© {new Date().getFullYear()} Document AutoFill. Все права защищены.
				</footer>
			</form>
		</div>
	)
}
