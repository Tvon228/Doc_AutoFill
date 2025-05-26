import classes from "./WorkArea.module.sass"

import WorkAreaButton from "../ui/buttons/WorkArea"
import SpecialistsBlock from "./SpecialistsBlock/Specialists"
import TasksBlock from "./TasksBlock/TasksBlock"
import ContractForm from "./ContractForm/ContractForm"
import PeriodForm from "./PeriodForm/PeriodForm"


export default function WorkArea() {

	return (
		<div class={classes.container}>
			<div class={classes.content}>
				<div class={classes.header}>
					<h2 class={classes.title}>Рабочая область</h2>
				</div>
				<div class={classes.main}>
					<SpecialistsBlock />
					<TasksBlock />
					<ContractForm />
					<PeriodForm />
				</div>
				<div class={classes.footer}>
					<WorkAreaButton />
				</div>
			</div>
		</div>
	)
}
