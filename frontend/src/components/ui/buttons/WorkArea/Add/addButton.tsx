import classes from "./addButton.module.sass"

import { FiPlus } from "solid-icons/fi"

export default function AddButton() {
	return (
		<div class={classes.container}>
			<FiPlus size={16} color="#2C60F0" />
			<span class={classes.text}>Добавить</span>
		</div>
	)
}
