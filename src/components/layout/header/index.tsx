import { useNavigate } from "@solidjs/router"

import classes from "./Header.module.sass"

import { BsQuestionCircleFill } from "solid-icons/bs"
import { FiSearch } from "solid-icons/fi"
import { AiOutlineUser } from "solid-icons/ai"

import { auth } from "../../../stores/authStore"

function Header() {
	const navigate = useNavigate()

	const getInitials = (name: string | undefined): string => {
		if (!name) return "??"

		const parts = name.split(" ")

		const surname = parts[0]
		const initials = parts
			.slice(1)
			.map((part) => part[0]?.toUpperCase() + ".")
			.join("")

		return `${surname} ${initials}`.trim()
	}

	return (
		<div class={classes.container}>
			<div class={classes.content}>
				<div class={classes.documentControls}>
					<div class={classes.nameProject}>
						<h1>
							<span class={classes.documentAuto}>
								Document Auto
							</span>
							<span class={classes.fill}>Fill</span>
						</h1>
					</div>
					<div class={classes.search}>
						<input
							class={classes.searchInput}
							placeholder="Поиск шаблонов"
						/>
						<FiSearch
							size={20}
							color="#3B3B3B"
							class={classes.searchIcon}
						/>
					</div>
				</div>
				<div class={classes.info}>
					<div
						class={classes.account}
						onClick={() => navigate("/profile")}
					>
						<AiOutlineUser size={27} class={classes.userIcon} />
						<div class={classes.userName}>
							{getInitials(auth.user?.name)}
						</div>
					</div>
					<div class={classes.questionMark}>
						<BsQuestionCircleFill size={27} color="#2C60F0" />
					</div>
				</div>
			</div>
		</div>
	)
}

export default Header
