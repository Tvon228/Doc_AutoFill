import classes from "./Profile.module.sass"
import { auth, setAuth } from "../../stores/authStore"
import { BiRegularEditAlt } from "solid-icons/bi"
import { createSignal } from "solid-js"
import Avatar from "../useAvatar"
import EditProfileModal from "../Modals/EditProfileModal/EditProfileModal"

export default function ProfilePage() {
	const [isModalOpen, setIsModalOpen] = createSignal(false)
	const [formData, setFormData] = createSignal({
		name: auth.user?.login || "",
		password: "",
		role: auth.user?.role || "",
		phone: auth.user?.phone || "",
		email: auth.user?.email || "",
	})

	const handleSubmit = async (e: Event) => {
		e.preventDefault()
		try {
			const response = await fetch("/api/profile", {
				method: "PUT",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					login: auth.user?.login,
					phone: formData().phone,
					email: formData().email
					
				}),
			})

			if (response.ok) {
				setAuth("user", (prev) => ({
					...prev,
					phone: formData().phone,
					email: formData().email
				}))
				setIsModalOpen(false)
			}
		} catch (error) {
			console.error("Ошибка обновления:", error)
		}
	}

	return (
		<div class={classes.container}>
			<div class={classes.content}>
				<div class={classes.header}>
					<h2 class={classes.title}>Аккаунт</h2>
				</div>
				<div class={classes.main}>
					<div class={classes.imageUser}>
						<Avatar />
					</div>
					<div class={classes.infoUser}>
						<div class={classes.mainInfo}>
							<div class={classes.text}>
								<span class={classes.nameUser}>{auth.user?.login}</span>
								
							</div>
						</div>
						<div class={classes.submainInfo}>
							<div class={classes.text}>
								<span>{auth.user?.phone}</span>
								<span>{auth.user?.email}</span>
							</div>
						</div>
					</div>
					<button class={classes.btn} onClick={() => setIsModalOpen(true)}>
						<BiRegularEditAlt size={18} color="#fff" />
						Редактировать профиль
					</button>
				</div>

				<EditProfileModal
					isOpen={isModalOpen()}
					onClose={() => setIsModalOpen(false)}
					formData={formData()}
					setFormData={setFormData}
					onSubmit={handleSubmit}
				/>
			</div>
		</div>
	)
}