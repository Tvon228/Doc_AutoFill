import { createSignal, For } from "solid-js";
import classes from "./TasksBlock.module.sass"
import AddButton from "../../ui/buttons/WorkArea/Add/addButton";

export default function TasksBlock(){

    const [tasks, ] = createSignal([
		{ id: 1, role: "Дизайн" },
		{ id: 2, role: "Верстка" },
		{ id: 3, role: "Тестировка" },
		{ id: 4, role: "PR" },
	])

    const handleAddSpecialist = () => {
		alert("Функция добавления специалиста!")
	};

    return(
        <div class={classes.content}>
			<div class={classes.header}>
				<div class={classes.text}>Задачи:</div>
				<AddButton />
			</div>
			<ol class={classes.items}>
				<div class={classes.information}>
					<For each={tasks()}>
						{(item) => (
							<li class={classes.marker}>
								<div class={classes.specialistWrapper}>
									<span>{item.role}</span>
								</div>
							</li>
						)}
					</For>
				</div>
			</ol>
			<div class={classes.btn} onClick={handleAddSpecialist}>
				<span>Показать всех</span>
			</div>
		</div>
    )
}