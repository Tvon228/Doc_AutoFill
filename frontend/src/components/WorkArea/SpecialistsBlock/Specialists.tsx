

import { createSignal, For } from "solid-js";
import AddButton from "../../ui/buttons/WorkArea/Add/addButton"
import classes from "./Specialists.module.sass"

export default function SpecialistsBlock() {
	const [specialists, ] = createSignal([
		{ id: 1, role: "Программист" },
		{ id: 2, role: "Тестировщик" },
		{ id: 3, role: "Программист" },
		{ id: 4, role: "Программист" },
	])

	const handleAddSpecialist = () => {
		alert("Функция добавления специалиста!"); // Заглушка
	};

	return (
		<div class={classes.content}>
			<div class={classes.header}>
				<div class={classes.text}>Специалисты:</div>
				<AddButton />
			</div>
			<ol class={classes.items}>
				<div class={classes.information}>
					<For each={specialists()}>
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
