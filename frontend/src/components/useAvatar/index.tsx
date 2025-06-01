import classes from "./UseAvatar.module.sass"

import { AiOutlineUser } from "solid-icons/ai"


export default function Avatar() {
	return (
		<>
			<div class={classes.imageUser}>
				<AiOutlineUser size={76} color="#2C60F0" />
			</div>
		</>
	)
}
