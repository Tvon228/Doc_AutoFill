import classes from "./WorkArea.module.sass"

import WorkAreaButton from "../ui/buttons/WorkArea"
import Dropdown from "./ui/Dropdownmenu/Dropdown"
import SpecialistsBlock from "./ui/SpecialistsBlock/Specialists"

export default function WorkArea() {

	return (
		<div class={classes.container}>
			<div class={classes.content}>
				<div class={classes.header}>
					<h2 class={classes.title}>Рабочая область</h2>
				</div>
				<div class={classes.main}>
					<Dropdown/>
					<SpecialistsBlock/>
				</div>
				<div class={classes.footer}>
					<WorkAreaButton />
				</div>
			</div>
		</div>
	)
}
