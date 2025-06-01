import classes from "./WorkArea.module.sass"

function WorkAreaButton() {
	return (
		<div class={classes.container} role="button">
			<span class={classes.nameButton}>Сгенерировать документ</span>
		</div>
	)
}

export default WorkAreaButton
