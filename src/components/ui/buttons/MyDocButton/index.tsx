import classes from "./MyDocButton.module.sass"

import { createSignal } from "solid-js"
import { AiOutlineFileAdd } from "solid-icons/ai"

function MyDocsButton(props: { onClick?: () => void }) {
	const [isActive, setIsActive] = createSignal(false)

	const handleClick = () => {
		setIsActive(!isActive())
		props.onClick?.()
	}
	return (
		<div
			classList={{
				[classes.container]: true,
				[classes.active]: isActive(),
			}}
			onClick={handleClick}
			role="button"
		>
			<AiOutlineFileAdd size={20} color={isActive() ? "#2C60F0" : "#fff"}/>
			<span class={classes.nameButton}>Добавить шаблон</span>
		</div>
	)
}

export default MyDocsButton
